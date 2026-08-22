"""The 'reason' + 'decide' stages: read an inbound message plus the looked-up
order record, and propose a refund action.

Two implementations, chosen by whether ANTHROPIC_API_KEY is set:

- NaiveReasoner (default, fully offline): a simple pattern-following agent
  that trusts whatever payment destination is explicitly stated in the
  inbound message, falling back to the order's original payment instrument
  if none is mentioned. This is a real vulnerability class, not a strawman
  -- plenty of shipped agents do exactly this ("extract the account number
  from the message and use it"). It's what makes today's vertical slice
  runnable without any API key while still being honestly hijackable.
- LLMReasoner (real Anthropic call, only used if ANTHROPIC_API_KEY is set):
  hands the raw message to Claude and asks it to decide the refund
  destination. Untested in this environment (no key here) -- verify once a
  key is available. Depth allocation for this layer is intentionally THIN
  (docs/context/Razorpay_16_Day_Battle_Plan.md Sec 4); it is not meant to be
  robust against injection on its own. That's the entire point of the
  system -- catching it downstream is the product.
"""

from __future__ import annotations

import os
import re
from typing import Protocol

from src.models import OrderRecord, ProposedAction

_DESTINATION_PATTERN = re.compile(r"\bupi:[\w.\-]+@[\w.\-]+\b")


class Reasoner(Protocol):
    def reason(self, order: OrderRecord, message: str) -> ProposedAction: ...


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


class LLMReasoner:
    """Real Anthropic-backed reasoner. Requires ANTHROPIC_API_KEY."""

    def __init__(self, model: str = "claude-opus-5") -> None:
        import anthropic  # deferred import: only required on this path

        self._client = anthropic.Anthropic()
        self._model = model

    def reason(self, order: OrderRecord, message: str) -> ProposedAction:
        import anthropic

        prompt = (
            "You are a customer support agent for a merchant on Razorpay. "
            "A customer has sent the following message about their order "
            f"{order.order_id}. The order's original payment instrument was "
            f"{order.original_payment_instrument} and the refund amount "
            f"owed is {order.refund_amount}.\n\n"
            f"Customer message:\n\"\"\"\n{message}\n\"\"\"\n\n"
            "Decide the refund destination account and respond with exactly "
            "two lines:\nDESTINATION: <account>\nRATIONALE: <one sentence>"
        )
        resp = self._client.messages.create(
            model=self._model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            block.text for block in resp.content if isinstance(block, anthropic.types.TextBlock)
        )
        destination = order.original_payment_instrument
        rationale = text.strip()
        for line in text.splitlines():
            if line.startswith("DESTINATION:"):
                destination = line.split(":", 1)[1].strip()
            elif line.startswith("RATIONALE:"):
                rationale = line.split(":", 1)[1].strip()
        return ProposedAction(
            amount=order.refund_amount,
            destination_account=destination,
            rationale=rationale,
        )


def default_reasoner() -> Reasoner:
    """NaiveReasoner unless ANTHROPIC_API_KEY is set, matching src/README.md's
    thin depth allocation for this layer either way."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return LLMReasoner()
    return NaiveReasoner()
