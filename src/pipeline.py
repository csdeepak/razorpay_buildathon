"""Orchestrates one scenario through every layer:

    reason -> decide -> safety gate -> act (mocked, only if allowed) -> verify -> audit

As of Day 8 (docs/decisions/0006-safety-layer.md), the safety gate runs
before act, so a blocked action never reaches the mock rail. verify still
runs regardless -- it doesn't depend on execution, and having it agree
independently with a block is itself useful evidence (defense in depth,
not redundancy: see src/safety/policy_gateway.py's module docstring).
"""

from __future__ import annotations

from typing import Any

from src.agent.reasoner import Reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore
from src.safety.policy_gateway import PolicyGateway
from src.tool.razorpay_api import DestinationNotExpressible
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
) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_name]
    order = order_store.get(scenario.order_id)

    ledger.append("SCENARIO_START", {"scenario": scenario.name, "order_id": scenario.order_id})

    # reason + decide
    action = reasoner.reason(order, scenario.inbound_message)
    ledger.append("AGENT_PROPOSED", action.model_dump())
    ledger.append("DECIDED", action.model_dump())  # trivial pass-through for now

    # safety gate -- runs before act, can block it
    policy_verdict = safety_gate.check(order, action)
    ledger.append("SAFETY_CHECK", policy_verdict.model_dump())

    exec_result = None
    inexpressible = None
    if policy_verdict.allowed:
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
    else:
        ledger.append(
            "ACTION_BLOCKED",
            {"rule_fired": policy_verdict.rule_fired, "reason": policy_verdict.reason},
        )

    # verify -- runs regardless of whether act ran; doesn't depend on execution
    verdict = verifier.check(order, action)
    ledger.append("VERIFICATION_RESULT", verdict.model_dump())

    ledger.append(
        "SCENARIO_END",
        {"scenario": scenario.name, "blocked": not policy_verdict.allowed, "consistent": verdict.consistent},
    )

    return {
        "scenario": scenario.name,
        "action": action,
        "policy_verdict": policy_verdict,
        "execution": exec_result,
        "inexpressible": inexpressible,
        "verdict": verdict,
    }
