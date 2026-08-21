"""Tests for the vertical slice as of the Day 8 safety layer. Not the Day
11+ adversarial evaluation harness (see eval/README.md) -- this proves the
pipeline runs end-to-end and that the attack is now blocked BEFORE
execution, not just detected after (that was the Day 6-7 behavior; see
docs/decisions/0005-vertical-slice-architecture.md and
docs/decisions/0006-safety-layer.md for what changed and why).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.agent.reasoner import NaiveReasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore, VelocityTracker
from src.models import MerchantPolicy
from src.pipeline import run_scenario
from src.safety.policy_gateway import PolicyGateway
from src.scenarios import ORDERS
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier

PERMISSIVE_POLICY = MerchantPolicy(max_single_amount=50_000.0, max_daily_amount=100_000.0, max_daily_count=5)


@pytest.fixture
def order_store() -> OrderStore:
    store = OrderStore()
    for order in ORDERS:
        store.register(order)
    return store


@pytest.fixture
def ledger(tmp_path: Path) -> AuditLedger:
    return AuditLedger(tmp_path / "audit_log.jsonl")


def _run(scenario_name: str, order_store: OrderStore, ledger: AuditLedger, policy: MerchantPolicy = PERMISSIVE_POLICY):
    safety_gate = PolicyGateway(policy, VelocityTracker())
    return run_scenario(
        scenario_name,
        reasoner=NaiveReasoner(),
        safety_gate=safety_gate,
        tool_client=MockRazorpayClient(),
        verifier=Verifier(),
        ledger=ledger,
        order_store=order_store,
    )


def test_benign_scenario_is_allowed_and_executed(order_store, ledger):
    result = _run("benign", order_store, ledger)
    assert result["policy_verdict"].allowed is True
    assert result["execution"] is not None
    assert result["execution"].status == "executed"
    assert result["verdict"].consistent is True


def test_naive_reasoner_is_still_fooled_by_the_injection(order_store, ledger):
    """The vulnerability itself is unchanged by Day 8 -- the agent still
    proposes the wrong destination. What changes is what happens next."""
    result = _run("attack", order_store, ledger)
    assert result["action"].destination_account == "upi:attacker-payout@fraudbank"


def test_attack_is_blocked_before_execution(order_store, ledger):
    result = _run("attack", order_store, ledger)
    assert result["policy_verdict"].allowed is False
    assert result["policy_verdict"].rule_fired == "payee_scope"
    assert result["execution"] is None, "the mocked payout must never be called for a blocked action"


def test_verification_independently_agrees_with_the_block(order_store, ledger):
    """Defense in depth: two independently-implemented mechanisms should
    agree, not just one of them catching it."""
    result = _run("attack", order_store, ledger)
    assert result["policy_verdict"].allowed is False
    assert result["verdict"].consistent is False


def test_audit_chain_is_intact_and_reflects_the_block(order_store, ledger):
    _run("attack", order_store, ledger)
    ok, message = ledger.verify_chain()
    assert ok, message
    entries = ledger.read_all()
    assert [e.event for e in entries] == [
        "SCENARIO_START",
        "AGENT_PROPOSED",
        "DECIDED",
        "SAFETY_CHECK",
        "ACTION_BLOCKED",
        "VERIFICATION_RESULT",
        "SCENARIO_END",
    ]


def test_audit_chain_for_allowed_action_shows_execution(order_store, ledger):
    _run("benign", order_store, ledger)
    entries = ledger.read_all()
    assert "ACTION_EXECUTED" in [e.event for e in entries]
    assert "ACTION_BLOCKED" not in [e.event for e in entries]


def test_audit_chain_detects_tampering(order_store, ledger):
    _run("benign", order_store, ledger)
    ok, _ = ledger.verify_chain()
    assert ok

    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    import json

    tampered = json.loads(lines[1])
    tampered["payload"]["amount"] = 999999.0
    lines[1] = json.dumps(tampered)
    ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, message = ledger.verify_chain()
    assert not ok
    assert "seq 2" in message
