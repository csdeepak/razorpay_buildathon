"""Orchestrates one scenario through every layer:

    reason -> decide -> safety gate -> act (only if allowed) -> verify
           -> completeness audit -> audit log

As of Day 8 (docs/decisions/0006-safety-layer.md), the safety gate runs
before act, so a blocked action never reaches the rail. verify still
runs regardless -- it doesn't depend on execution, and having it agree
independently with a block is itself useful evidence (defense in depth,
not redundancy: see src/safety/policy_gateway.py's module docstring).

THE COMPLETENESS STAGE (docs/decisions/0015-one-agent.md)
---------------------------------------------------------
Added late, and its absence was a real defect rather than a missing nicety.
The detective control (src/verification/completeness.py) is the project's
headline result -- the class no preventive gate can address -- and until now
it existed only inside the evaluation harness. `make demo` ran the pipeline
without it, which meant the one control the pitch leans hardest on was the
one thing a reviewer could not see running.

It runs LAST and unconditionally, including when the agent proposed nothing
at all. That is the entire point: a denial attack leaves no action to gate,
no execution to verify and nothing for any earlier stage to notice.

`action` may be None. That is not an error path -- it is what a successful
denial attack looks like from inside the pipeline.
"""

from __future__ import annotations

from typing import Any

from src.agent.reasoner import Reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore
from src.safety.policy_gateway import PolicyGateway
from src.tool.razorpay_api import DestinationNotExpressible
from src.verification.completeness import CompletenessChecker, CompletenessVerdict
from src.verification.verifier import Verifier
from src.scenarios import SCENARIOS


def run_scenario(
    scenario_name: str,
    *,
    reasoner: Reasoner,
    safety_gate: PolicyGateway,
    tool_client: Any,
    verifier: Verifier,
    ledger: AuditLedger,
    order_store: OrderStore,
    completeness: CompletenessChecker | None = None,
) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_name]
    order = order_store.get(scenario.order_id)

    ledger.append("SCENARIO_START", {"scenario": scenario.name, "order_id": scenario.order_id})

    # reason + decide. `action` is None when the agent proposed no money
    # movement at all -- the denial signature.
    action = reasoner.reason(order, scenario.inbound_message)

    policy_verdict = None
    if action is None:
        ledger.append("AGENT_PROPOSED_NOTHING", {"order_id": order.order_id})
    else:
        ledger.append("AGENT_PROPOSED", action.model_dump())
        ledger.append("DECIDED", action.model_dump())  # trivial pass-through for now

    # safety gate -- runs before act, can block it. Nothing proposed means
    # nothing to gate, which is exactly why this layer cannot cover denial.
    if action is not None:
        policy_verdict = safety_gate.check(order, action)
        ledger.append("SAFETY_CHECK", policy_verdict.model_dump())

    exec_result = None
    inexpressible = None
    if action is not None and policy_verdict is not None and policy_verdict.allowed:
        try:
            exec_result = tool_client.create_refund(action, order)
            ledger.append("ACTION_EXECUTED", exec_result.model_dump(mode="json"))
        except DestinationNotExpressible as exc:
            # The gate passed something the rail has no way to encode. On the
            # real Razorpay API a refund carries no payee, so this is the
            # structural backstop firing rather than a policy decision --
            # worth its own audit event, not a generic block.
            inexpressible = exc
            ledger.append(
                "ACTION_INEXPRESSIBLE",
                {"proposed": exc.proposed, "original": exc.original, "reason": str(exc)},
            )
    elif action is not None and policy_verdict is not None:
        ledger.append(
            "ACTION_BLOCKED",
            {"rule_fired": policy_verdict.rule_fired, "reason": policy_verdict.reason},
        )

    # verify -- runs regardless of whether act ran; doesn't depend on execution
    verdict = None
    if action is not None:
        verdict = verifier.check(order, action)
        ledger.append("VERIFICATION_RESULT", verdict.model_dump())

    # completeness -- runs LAST and ALWAYS, including when nothing was proposed.
    # Reads trusted state only: the case record and what actually executed,
    # never scenario.order_notes and never the agent's rationale.
    checker = completeness or CompletenessChecker()
    paid = float(exec_result.action.amount) if exec_result is not None else 0.0
    completeness_verdict: CompletenessVerdict = checker.check(
        order,
        refund_request_open=scenario.refund_request_open,
        refund_paid_total=paid,
        hold=scenario.hold,
    )
    ledger.append("COMPLETENESS_AUDIT", completeness_verdict.model_dump())

    ledger.append(
        "SCENARIO_END",
        {
            "scenario": scenario.name,
            "proposed": action is not None,
            "blocked": bool(policy_verdict is not None and not policy_verdict.allowed),
            "consistent": verdict.consistent if verdict is not None else None,
            "obligation": completeness_verdict.status,
        },
    )

    return {
        "scenario": scenario.name,
        "action": action,
        "policy_verdict": policy_verdict,
        "execution": exec_result,
        "inexpressible": inexpressible,
        "verdict": verdict,
        "completeness": completeness_verdict,
    }
