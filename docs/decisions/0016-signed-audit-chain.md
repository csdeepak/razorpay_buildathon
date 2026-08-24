# 0016 — What the audit chain actually proves

Date: 2026-08-24
Status: **locked**

## Context

`src/audit/ledger.py` implemented a SHA-256 hash chain and the repo called it
**tamper-evident** — in `README.md`, in `submission/narrative.md` ("tamper-
evident by construction — which is the 'full audit trail' CERT-In asks for,
implemented rather than asserted"), and in the demo output.

A hash chain does not support that word unqualified. It detects accidental
corruption and naive edits. It does **not** survive an attacker with write
access to the file: editing an entry and recomputing every hash after it is
ten lines of code, and the result is a perfectly consistent chain telling a
different story. For a payments audit trail, in a submission that leans on
CERT-In's audit requirement, that is the wrong kind of overclaim — and it is
the kind a security engineer on a panel finds immediately.

Separately: `append()` called `read_all()` on every write, re-parsing the
entire log to learn the last hash and sequence number. Writing N entries was
O(N²), on the audit trail itself.

## Decision

**Sign the entries, and say precisely what is and is not proved.**

- Each entry carries an optional `signature`: HMAC-SHA256 over the entry hash,
  keyed by `WARDEN_AUDIT_KEY`. An attacker who can write the file but cannot
  read the key can still re-chain it — and every signature then fails, because
  they cannot forge one.
- **Unsigned mode is preserved and announced.** With no key, entries are
  written unsigned and `verify_chain()` returns *"chain intact, N entries
  (UNSIGNED — detects corruption and naive edits only; set WARDEN_AUDIT_KEY to
  detect a writer who re-chains the log)"*. A demo that silently degrades to a
  weaker guarantee while printing the same reassuring message is exactly what
  this project keeps arguing against.
- The chain head is cached after one read at construction. `append()` is O(1);
  `verify_chain()` still reads and recomputes from scratch and never trusts
  the cached head.

## What is still not claimed

Both recorded in the module docstring and asserted as tests, so they cannot
quietly become claims:

- **No external anchor.** Whoever holds the key can rewrite history wholesale
  and re-sign it. `test_an_attacker_holding_the_key_still_wins` asserts
  exactly that. Defeating it needs the chain head published somewhere the
  writer does not control — a notary, a counterparty, a transparency log.
- **No non-repudiation.** HMAC is symmetric: a valid signature proves "someone
  with the key wrote this", never "this party wrote this". Public-key signing
  is the upgrade, and it is the same upgrade
  [ADR 0012](0012-mandate-layer.md) defers for the same reason.

## Alternatives considered

- **Require a key and fail without one.** Rejected: it breaks `make demo` for
  anyone who clones the repo, and stranger-runnability is a stated Gate-5
  requirement. Working unsigned and saying so loudly keeps both properties.
- **Ed25519 instead of HMAC.** Rejected today for the ADR 0012 reason — signer
  and verifier are one trust domain — and named as the upgrade rather than
  omitted.
- **Anchor the chain head externally.** The genuinely right answer, and out of
  scope for the remaining time. Named as the gap instead of implied away.
- **Soften the README wording and leave the code alone.** Rejected: signing
  was two hours, and "I noticed my own overclaim and closed it" is worth more
  than a hedged sentence.

## Consequences

- `README.md` and `submission/narrative.md` must stop saying "tamper-evident"
  without qualification. The accurate phrasing is *hash-chained and
  HMAC-signed; detects any edit by a writer who does not hold the key; not
  externally anchored, so a key-holder can still rewrite history.*
- 8 new tests, including `test_a_rechained_log_defeats_an_unsigned_chain`,
  which performs the attack the old wording was papering over and asserts that
  an unsigned chain verifies afterwards.
- `AuditEntry.signature` defaults to `""`, so logs written before this ADR
  still parse.
- The suite got faster (0.86s → 0.44s), which is the O(N²) fix showing up.
