"""What the audit chain actually proves, signed and unsigned (ADR 0016).

The test that matters here is `test_a_rechained_log_defeats_an_unsigned_chain`.
It performs the attack the word "tamper-evident" was previously papering over:
edit a past entry, then recompute every hash after it. An unsigned chain
verifies perfectly afterwards. That is not a bug in the hash chain -- it is
what a hash chain is -- and the repo now says so in the code, in the verify
message, and here.
"""

from __future__ import annotations

import hashlib
import json

import pytest

from src.audit.ledger import AuditLedger, _canonical

KEY = "audit-test-key"


def _rechain(path, *, at_seq: int, new_payload: dict, key: str | None = None) -> None:
    """Rewrite one entry and repair every hash after it -- the attack."""
    import hmac

    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in lines:
        if row["seq"] == at_seq:
            row["payload"] = new_payload
    prev = "0" * 64
    for row in lines:
        row["prev_hash"] = prev
        row["hash"] = hashlib.sha256(
            _canonical(row["seq"], row["timestamp"], row["event"], row["payload"], prev).encode("utf-8")
        ).hexdigest()
        if key is not None:
            row["signature"] = hmac.new(
                key.encode("utf-8"), row["hash"].encode("utf-8"), hashlib.sha256
            ).hexdigest()
        prev = row["hash"]
    path.write_text("\n".join(json.dumps(r) for r in lines) + "\n", encoding="utf-8")


@pytest.fixture
def log_path(tmp_path):
    return tmp_path / "audit.jsonl"


def _write_three(ledger):
    ledger.append("SCENARIO_START", {"scenario": "attack"})
    ledger.append("ACTION_BLOCKED", {"rule_fired": "payee_scope"})
    ledger.append("SCENARIO_END", {"blocked": True})


# ------------------------------------------------------------------ baseline


def test_unsigned_ledger_verifies_and_says_it_is_unsigned(log_path):
    ledger = AuditLedger(log_path, key=None)
    _write_three(ledger)
    ok, message = ledger.verify_chain()
    assert ok
    assert "UNSIGNED" in message, "an unsigned log must not report the same guarantee as a signed one"


def test_signed_ledger_says_it_is_signed(log_path):
    ledger = AuditLedger(log_path, key=KEY)
    _write_three(ledger)
    ok, message = ledger.verify_chain()
    assert ok and "signed" in message


def test_naive_edit_is_caught_either_way(log_path):
    """Editing a payload without repairing hashes. Both modes catch this."""
    for key in (None, KEY):
        path = log_path.with_name(f"naive-{key}.jsonl")
        ledger = AuditLedger(path, key=key)
        _write_three(ledger)
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        rows[1]["payload"] = {"rule_fired": "none"}
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        ok, message = AuditLedger(path, key=key).verify_chain()
        assert not ok and "tampered" in message


# ------------------------------------------------ the claim signing actually buys


def test_a_rechained_log_defeats_an_unsigned_chain(log_path):
    """The honest limitation, asserted rather than described.

    An attacker with write access edits the block record and recomputes the
    whole chain. Every hash is internally consistent, so verification passes
    and the log now says the attack was never blocked."""
    ledger = AuditLedger(log_path, key=None)
    _write_three(ledger)
    _rechain(log_path, at_seq=2, new_payload={"rule_fired": None, "note": "nothing happened"})

    ok, message = AuditLedger(log_path, key=None).verify_chain()
    assert ok, "a bare hash chain cannot detect a full re-chain -- this is the point"
    assert json.loads(log_path.read_text(encoding="utf-8").splitlines()[1])["payload"]["note"] == "nothing happened"


def test_signing_catches_the_rechain_the_hash_chain_misses(log_path):
    """Same attack, against a keyed ledger, by an attacker who does not hold
    the key. The chain is consistent and every signature is wrong."""
    ledger = AuditLedger(log_path, key=KEY)
    _write_three(ledger)
    _rechain(log_path, at_seq=2, new_payload={"rule_fired": None}, key=None)

    ok, message = AuditLedger(log_path, key=KEY).verify_chain()
    assert not ok
    assert "signature" in message or "unsigned" in message


def test_an_attacker_holding_the_key_still_wins(log_path):
    """Stated as a test so it cannot quietly become a claim. HMAC gives
    integrity against an outsider, not non-repudiation and not an anchor --
    whoever holds the key can rewrite history and re-sign it."""
    ledger = AuditLedger(log_path, key=KEY)
    _write_three(ledger)
    _rechain(log_path, at_seq=2, new_payload={"rule_fired": None}, key=KEY)

    ok, _ = AuditLedger(log_path, key=KEY).verify_chain()
    assert ok, "this is the residual limitation ADR 0016 records, not a passing grade"


# ------------------------------------------------------------------- mechanics


def test_append_does_not_reread_the_log(log_path, monkeypatch):
    """append() used to call read_all() every time, making N writes O(N^2) on
    the audit trail itself. One read at construction, none after."""
    ledger = AuditLedger(log_path, key=None)
    calls = {"n": 0}
    original = AuditLedger.read_all

    def counting(self):
        calls["n"] += 1
        return original(self)

    monkeypatch.setattr(AuditLedger, "read_all", counting)
    for i in range(25):
        ledger.append("EVENT", {"i": i})
    assert calls["n"] == 0
    ok, _ = ledger.verify_chain()
    assert ok
    assert [e.seq for e in ledger.read_all()] == list(range(1, 26))


def test_a_second_ledger_on_the_same_file_continues_the_chain(log_path):
    """The cached head must be re-derived from the file, not assumed empty --
    otherwise a restart silently forks the chain."""
    _write_three(AuditLedger(log_path, key=KEY))
    second = AuditLedger(log_path, key=KEY)
    second.append("SCENARIO_START", {"scenario": "benign"})
    ok, message = second.verify_chain()
    assert ok and "4 entries" in message
