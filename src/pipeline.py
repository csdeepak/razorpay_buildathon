"""Orchestrates one scenario through every layer, in the exact order named
in docs/context/Razorpay_16_Day_Battle_Plan.md's Day 6-7 line:

    reason -> decide -> act (mocked) -> verify -> audit

No safety gate yet -- see src/models.py's module docstring. That means this
pipeline can, and for the attack scenario will, execute a bad action before
verify catches it. That gap is the whole justification for Day 8.
"""

from __future__ import annotations

from typing import Any

from src.agent.reasoner import Reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier
from src.scenarios import SCENARIOS


def run_scenario(
    scenario_name: str,
    *,
    reasoner: Reasoner,
    tool_client: MockRazorpayClient,
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

    # act (mocked)
    exec_result = tool_client.create_refund(action)
    ledger.append("ACTION_EXECUTED", exec_result.model_dump(mode="json"))

    # verify
    verdict = verifier.check(order, action)
    ledger.append("VERIFICATION_RESULT", verdict.model_dump())

    ledger.append("SCENARIO_END", {"scenario": scenario.name, "consistent": verdict.consistent})

    return {
        "scenario": scenario.name,
        "action": action,
        "execution": exec_result,
        "verdict": verdict,
    }
