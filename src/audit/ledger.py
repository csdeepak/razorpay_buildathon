"""The 'audit' stage: an append-only, hash-chained, optionally signed log.

Each entry's hash covers its own payload plus the previous entry's hash, so
altering or deleting a past entry breaks every hash after it. `verify_chain()`
recomputes the whole chain and checks exactly that.

WHAT A BARE HASH CHAIN DOES AND DOES NOT PROVE (ADR 0016)
----------------------------------------------------------
A hash chain on its own detects *accidental* corruption and *naive* edits. It
does **not** survive an attacker with write access to the file: recomputing
every hash after an edited entry is ten lines of code, and the result is a
perfectly consistent chain telling a different story. Calling that
"tamper-evident" without qualification is an overclaim, and for a payments
audit trail it is the wrong kind of overclaim.

So entries carry an optional **HMAC-SHA256 signature** over the entry hash,
keyed by `WARDEN_AUDIT_KEY`. An attacker who can write the file but cannot
read the key can still rewrite the chain -- and every signature after the edit
then fails, because they cannot forge one. That is a real integrity property
rather than an asserted one.

**When no key is configured the log is written unsigned**, and both
`verify_chain()` and the CLI say so in as many words. That is deliberate: a
demo that silently degrades to a weaker guarantee while printing the same
reassuring message is exactly the failure this project keeps arguing against.
The honest options were "require a key and break `make demo` for anyone
without one" or "work unsigned and say loudly that it is unsigned"; the second
keeps the repo runnable by a stranger, which `docs/context/` names as a
Gate-5 requirement.

What is still NOT claimed, in either mode:

- **No external anchor.** Whoever holds the key can rewrite history wholesale
  and re-sign it. Defeating that needs the chain head published somewhere the
  writer does not control -- a notary, a second party, a transparency log.
- **No non-repudiation.** HMAC is symmetric: verifier and signer are the same
  role, so a valid signature proves "someone with the key wrote this", never
  "this specific party wrote this". Public-key signing is the upgrade, and is
  the same upgrade `src/safety/mandate.py` defers for the same reason.

APPEND IS O(1), AND USED NOT TO BE (ADR 0016)
----------------------------------------------
`append()` previously called `read_all()` on every write -- re-parsing the
entire log to learn the last hash and sequence number, which made writing N
entries O(N^2) and re-read the whole audit trail once per audited event. The
chain head is now held in memory after a single read at construction. The file
is still the source of truth: `verify_chain()` reads and recomputes from
scratch and never trusts the cached head.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel

GENESIS_HASH = "0" * 64


class AuditEntry(BaseModel):
    seq: int
    timestamp: str
    event: str
    payload: dict[str, Any]
    prev_hash: str
    hash: str
    signature: str = ""
    """HMAC-SHA256 of `hash`, or "" when the ledger was written without a key.
    Defaulted so logs written before ADR 0016 still parse."""


def _canonical(seq: int, timestamp: str, event: str, payload: dict[str, Any], prev_hash: str) -> str:
    body = {"seq": seq, "timestamp": timestamp, "event": event, "payload": payload, "prev_hash": prev_hash}
    return json.dumps(body, sort_keys=True, default=str)


class AuditLedger:
    def __init__(self, path: Path | str = "var/audit_log.jsonl", key: bytes | str | None = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

        configured = key if key is not None else os.environ.get("WARDEN_AUDIT_KEY")
        if isinstance(configured, str):
            configured = configured.encode("utf-8") or None
        self._key: bytes | None = configured or None

        # One read at construction to find the chain head. See the module
        # docstring: the file stays authoritative, this is only a cursor.
        entries = self.read_all()
        self._last_hash = entries[-1].hash if entries else GENESIS_HASH
        self._seq = len(entries)

    @property
    def signed(self) -> bool:
        return self._key is not None

    def _sign(self, digest: str) -> str:
        if self._key is None:
            return ""
        return hmac.new(self._key, digest.encode("utf-8"), hashlib.sha256).hexdigest()

    def append(self, event: str, payload: dict[str, Any]) -> AuditEntry:
        self._seq += 1
        timestamp = datetime.now(timezone.utc).isoformat()
        digest = hashlib.sha256(
            _canonical(self._seq, timestamp, event, payload, self._last_hash).encode("utf-8")
        ).hexdigest()
        entry = AuditEntry(
            seq=self._seq,
            timestamp=timestamp,
            event=event,
            payload=payload,
            prev_hash=self._last_hash,
            hash=digest,
            signature=self._sign(digest),
        )
        with self.path.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")
        self._last_hash = digest
        return entry

    def read_all(self) -> list[AuditEntry]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []
        entries = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(AuditEntry.model_validate_json(line))
        return entries

    def verify_chain(self) -> tuple[bool, str]:
        """Recompute every hash from scratch and confirm the chain holds.

        Returns (ok, message). The message states the guarantee actually
        obtained -- signed or unsigned -- rather than a fixed reassurance,
        because those are different claims and only one of them survives a
        writer with file access."""
        entries = self.read_all()
        expected_prev = GENESIS_HASH
        for entry in entries:
            if entry.prev_hash != expected_prev:
                return False, f"seq {entry.seq}: prev_hash mismatch (broken chain)"
            recomputed = hashlib.sha256(
                _canonical(entry.seq, entry.timestamp, entry.event, entry.payload, entry.prev_hash).encode("utf-8")
            ).hexdigest()
            if recomputed != entry.hash:
                return False, f"seq {entry.seq}: hash does not match its own recorded content (tampered)"
            if self._key is not None:
                if not entry.signature:
                    return False, f"seq {entry.seq}: entry is unsigned but this ledger is keyed"
                if not hmac.compare_digest(self._sign(entry.hash), entry.signature):
                    return False, f"seq {entry.seq}: signature does not verify (forged or re-chained)"
            expected_prev = entry.hash

        if self._key is not None:
            return True, f"chain intact and signed, {len(entries)} entries"
        return True, (
            f"chain intact, {len(entries)} entries "
            f"(UNSIGNED -- detects corruption and naive edits only; set "
            f"WARDEN_AUDIT_KEY to detect a writer who re-chains the log)"
        )
