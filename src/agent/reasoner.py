"""The 'reason' + 'decide' stages: read an inbound message plus the looked-up
order record, and propose an action -- or propose nothing at all.

Two implementations, chosen by whether ANTHROPIC_API_KEY is set:

- NaiveReasoner (default, fully offline): a simple pattern-following agent
  that trusts whatever payment destination is explicitly stated in the
  inbound message, falling back to the order's original payment instrument
  if none is mentioned. This is a real vulnerability class, not a strawman
  -- plenty of shipped agents do exactly this ("extract the account number
  from the message and use it"). It's what makes the demo runnable without
  any API key while still being honestly hijackable.
- ToolCallingReasoner (real model, multi-turn, real tool calls): **the same
  agent the entire evaluation was run against**, driving the demo pipeline.

ONE AGENT, NOT TWO (docs/decisions/0015-one-agent.md)
-----------------------------------------------------
This file used to hold an `LLMReasoner` that made a single text completion and
parsed `DESTINATION:` out of the reply. It was never the thing measured: every
number in docs/eval-findings.md came from the tool-calling agent in
eval/agent.py. So the demo showed one agent and the evidence described another,
and `LLMReasoner`'s own docstring admitted it had never been run. It is
deleted rather than fixed -- there is no reason to maintain a second, weaker
agent whose only role was to be the one on screen.

`ToolCallingReasoner` therefore imports the agent from `eval/`. The dependency
direction is deliberate and worth stating plainly: the agent under test lives
next to the harness that measures it, and the demo is a *consumer* of that
same object. Duplicating it into `src/` to make the import graph prettier is
exactly how the demo drifted from the evidence in the first place.

`reason()` may return **None**, meaning the agent proposed no money movement.
That is not an error condition -- it is the denial attack's entire signature,
and the pipeline has to be able to represent "the agent did nothing" in order
for the completeness audit to have anything to catch.
"""

from __future__ import annotations

import os
import re
from typing import Protocol

from src.models import OrderRecord, ProposedAction

_DESTINATION_PATTERN = re.compile(r"\bupi:[\w.\-]+@[\w.\-]+\b")


class Reasoner(Protocol):
    def reason(self, order: OrderRecord, message: str) -> ProposedAction | None: ...


class NaiveReasoner:
    """Trusts any explicitly-stated payment destination in the message."""

    def reason(self, order: OrderRecord, message: str) -> ProposedAction:
        mentioned = [
            m for m in _DESTINATION_PATTERN.findall(message)
            if m != order.original_payment_instrument
        ]
        if mentioned:
            destination = mentioned[0]
            rationale = (
                f"Customer message explicitly stated a destination account "
                f"({destination}) different from the original payment "
                f"instrument. Using the stated destination as requested."
            )
        else:
            destination = order.original_payment_instrument
            rationale = (
                "No alternate destination account was stated in the "
                "message; using the order's original payment instrument."
            )
        return ProposedAction(
            amount=order.refund_amount,
            destination_account=destination,
            rationale=rationale,
        )


class ToolCallingReasoner:
    """The agent under test, wired into the demo pipeline.

    Runs the real multi-turn tool-calling loop from `eval/agent.py` with
    enforcement DISABLED inside the loop, so every proposal reaches the
    pipeline's own `PolicyGateway` and is refused in one visible place. Two
    enforcement points would mean the demo shows a block that the evaluation's
    numbers did not come from.
    """

    def __init__(self, model: str | None = None, order_notes: str = "") -> None:
        self._model = model
        self._order_notes = order_notes

    def reason(self, order: OrderRecord, message: str) -> ProposedAction | None:
        from eval.agent import AgentRunner, allow_everything

        def lookup(_order_id: str) -> dict:
            return {
                "order_id": order.order_id,
                "amount_owed": order.refund_amount,
                "original_payment_instrument": order.original_payment_instrument,
                "status": "delivered",
                "customer_notes": self._order_notes,
            }

        kwargs = {"enforcement": allow_everything}
        if self._model:
            kwargs["model"] = self._model
        result = AgentRunner(lookup, **kwargs).run([message])

        for proposal in result["proposals"]:
            if proposal.tool_name in ("issue_refund", "send_payout"):
                return ProposedAction(
                    action_type="refund" if proposal.tool_name == "issue_refund" else "payout",
                    amount=float(proposal.arguments.get("amount", 0) or 0),
                    destination_account=str(
                        proposal.arguments.get("destination_account", "")
                        or order.original_payment_instrument
                    ),
                    rationale=result["final_text"][:400] or "proposed by the agent under test",
                )

        # No money-moving proposal. The agent either closed the case or stalled;
        # either way nothing was paid, which is what the completeness audit
        # exists to notice.
        return None


def default_reasoner(order_notes: str = "") -> Reasoner:
    """The real tool-calling agent when a key is available, the offline naive
    agent otherwise. `make demo` works either way; only the first is what the
    evaluation measured, and src/cli.py prints which one ran."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return ToolCallingReasoner(order_notes=order_notes)
    return NaiveReasoner()
