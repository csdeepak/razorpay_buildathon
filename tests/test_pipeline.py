"""Tests for the Day 6-7 vertical slice. Not the Day 11+ adversarial
evaluation harness (see eval/README.md) -- this just proves the pipeline
runs end-to-end and that today's known gap (detective, not preventive) is
real and understood, not accidental.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from src.agent.reasoner import NaiveReasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore
from src.pipeline import run_scenario
from src.scenarios import ORDERS
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier


@pytest.fixture
def order_store() -> OrderStore:
    store = OrderStore()
    for order in ORDERS:
        store.register(order)
    return store


@pytest.fixture
def ledger(tmp_path: Path) -> AuditLedger:
    return AuditLedger(tmp_path / "audit_log.jsonl")


def _run(scenario_name: str, order_store: OrderStore, ledger: AuditLedger):
    return run_scenario(
        scenario_name,
        reasoner=NaiveReasoner(),
        tool_client=MockRazorpayClient(),
        verifier=Verifier(),
        ledger=ledger,
        order_store=order_store,
    )


def test_benign_scenario_is_consistent(order_store, ledger):
    result = _run("benign", order_store, ledger)
    assert result["verdict"].consistent is True
    assert result["action"].destination_account == "upi:customer4521@okhdfcbank"


def test_naive_reasoner_is_fooled_by_the_injection(order_store, ledger):
    """This is the vulnerability the whole project exists to catch -- assert
    it's real, not assumed. If this ever starts failing because someone
    hardened NaiveReasoner, that's a signal the scenario needs a new attack
    variant, not that this test is wrong."""
    result = _run("attack", order_store, ledger)
    assert result["action"].destination_account == "upi:attacker-payout@fraudbank"


def test_verification_catches_the_attack_after_the_fact(order_store, ledger):
    result = _run("attack", order_store, ledger)
    assert result["verdict"].consistent is False
    assert result["verdict"].expected_destination == "upi:customer4521@okhdfcbank"
    assert result["verdict"].actual_destination == "upi:attacker-payout@fraudbank"


def test_action_executes_before_verification_runs(order_store, ledger):
    """Documents today's known gap: the mocked payout executes regardless of
    what verify later finds. This is what Day 8's safety gate is for."""
    result = _run("attack", order_store, ledger)
    assert result["execution"].status == "executed"
    assert result["execution"].action.destination_account == "upi:attacker-payout@fraudbank"
    assert result["verdict"].consistent is False


def test_audit_chain_is_intact_after_a_run(order_store, ledger):
    _run("attack", order_store, ledger)
    ok, message = ledger.verify_chain()
    assert ok, message
    entries = ledger.read_all()
    assert [e.event for e in entries] == [
        "SCENARIO_START",
        "AGENT_PROPOSED",
        "DECIDED",
        "ACTION_EXECUTED",
        "VERIFICATION_RESULT",
        "SCENARIO_END",
    ]


def test_audit_chain_detects_tampering(order_store, ledger):
    _run("benign", order_store, ledger)
    ok, _ = ledger.verify_chain()
    assert ok

    # Tamper with one line's payload directly on disk, bypassing the API.
    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    import json

    tampered = json.loads(lines[1])
    tampered["payload"]["amount"] = 999999.0
    lines[1] = json.dumps(tampered)
    ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, message = ledger.verify_chain()
    assert not ok
    assert "seq 2" in message
