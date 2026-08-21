"""The 'audit' stage: an append-only, hash-chained log.

Each entry's hash covers its own payload plus the previous entry's hash, so
altering or deleting a past entry breaks every hash after it -- verify_chain()
checks exactly that. This is today's (Day 6-7) real but minimal version of
"tamper-evident": Day 10 (docs/progress-tracker.md) goes deeper (replay,
queryability). Deliberately not cryptographic signing yet -- a hash chain
proves internal consistency, not who wrote it; that's a Day 10 question, not
a vertical-slice one.
"""

from __future__ import annotations

import hashlib
import json
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


def _canonical(seq: int, timestamp: str, event: str, payload: dict[str, Any], prev_hash: str) -> str:
    body = {"seq": seq, "timestamp": timestamp, "event": event, "payload": payload, "prev_hash": prev_hash}
    return json.dumps(body, sort_keys=True, default=str)


class AuditLedger:
    def __init__(self, path: Path | str = "var/audit_log.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def _last_hash(self) -> str:
        entries = self.read_all()
        return entries[-1].hash if entries else GENESIS_HASH

    def append(self, event: str, payload: dict[str, Any]) -> AuditEntry:
        entries = self.read_all()
        seq = len(entries) + 1
        prev_hash = entries[-1].hash if entries else GENESIS_HASH
        timestamp = datetime.now(timezone.utc).isoformat()
        digest = hashlib.sha256(_canonical(seq, timestamp, event, payload, prev_hash).encode("utf-8")).hexdigest()
        entry = AuditEntry(seq=seq, timestamp=timestamp, event=event, payload=payload, prev_hash=prev_hash, hash=digest)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")
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
        Returns (ok, message)."""
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
            expected_prev = entry.hash
        return True, f"chain intact, {len(entries)} entries"
