# 0012 — The mandate layer, built rather than described

Date: 2026-08-24
Status: **locked**

## Context

[ADR 0007](0007-rearchitecture-intent-bound-authority.md) is the project's
central architectural claim: *don't filter instructions, bind authority to
verified intent.* It specifies a mandate as **"a signed, scoped, single-use,
expiring capability minted from a verified human authorization."**
`submission/narrative.md` §4 repeats that specification almost verbatim, and
the form's Q9 answer says money actions "require a mandate scoped from trusted
order state."

**None of it existed.** A review grep for `mandate`, `nonce`, `expiry`,
`single_use` across `src/` returned nothing. What shipped was
`src/safety/policy_gateway.py`: five ordered rules — category, payee_scope,
amount_binding, spend_cap, velocity. Those rules are sound and every recorded
result depends on them, but they are **policy**, not **capability**. Policy
asks "is this action within limits?" A capability asks "was this action
authorised at all, and is that authorisation still valid?" A refund that is
within every limit but was never authorised passes the first and fails the
second, and only the second is what ADR 0007 claims to enforce.

This is the worst possible place for a gap. The buildathon panel reviews
architecture and technical decisions directly, and the specific question
"show me where single-use is enforced" had no answer. Worse, the whole project
is positioned on measurement honesty — an overclaim in the most-read document
does more damage here than it would anywhere else.

## Decision

**Build it.** `src/safety/mandate.py` implements what ADR 0007 specified:

- `Mandate` — `{mandate_id, action_type, order_id, payee, max_amount,
  issued_at, expires_at, single_use, nonce, signature}`.
- `MandateMinter.mint(order, ...)` — **the payee is derived from the
  `OrderRecord` and there is no parameter to override it.** `max_amount` may
  narrow the ceiling and raises if asked to widen it. Signed HMAC-SHA256 over
  a canonical payload that round-trips through JSON.
- `MandateVerifier` — signature, expiry, and replay against a `NonceRegistry`.
- `PolicyGateway` gains four binding rules (`mandate_order_scope`,
  `mandate_action_scope`, `mandate_payee_scope`, `mandate_amount_scope`) that
  run **before** the policy rules, plus `mandate_missing` and
  `mandate_unverifiable`.

The nonce is burned on the single path that reaches "allowed", alongside the
velocity record — the same check-and-record atomicity the gateway already
used, for the same reason.

**It is additive and off by default.** `PolicyGateway(..., require_mandate=False)`
and `check(order, action)` with no mandate behave exactly as before.

## Alternatives considered

- **Edit the narrative to describe the five rules instead.** Cheapest, and
  genuinely defensible — the rules do enforce intent-binding for the payee and
  amount. Rejected because ADR 0007 is the intellectual core of the
  submission, and retreating from it to match a thinner implementation is a
  worse story than building the thin missing piece. The work was three hours.
- **Make mandates mandatory and re-run the evaluation.** Rejected on
  measurement grounds, and this is the load-bearing reason for `require_mandate`
  defaulting to False: every number in `docs/eval-findings.md` was measured
  against the policy rules alone. Turning on a new required check silently
  changes the system under test and invalidates 24 findings and $10.27 of
  recorded runs. The layer ships tested and demonstrable; re-measuring the
  whole corpus against it is a separate, honest, unaffordable-today piece of
  work, and saying so is better than quietly conflating the two.
- **Public-key signatures.** Rejected for now, and the reasoning is recorded
  in the module docstring rather than hidden: minter and verifier are the same
  trust domain here, so HMAC is sufficient and has no key-distribution story
  to get wrong. It becomes the wrong choice the moment a merchant mints and
  Razorpay verifies — that is the upgrade path, and it is the same upgrade
  [ADR 0016](0016-signed-audit-chain.md) defers for the same reason.
- **A real HITL escalation path.** ADR 0007's diagram shows one. Still not
  built, still not claimed. Named here so it stays a known gap rather than
  drifting back into the narrative.

## Consequences

- ADR 0007's specification is now true of the code. `submission/narrative.md`
  and the Q9 answer can describe expiry and single-use because they exist.
- **`temporal_decoupling`** — class 9 of ADR 0007's taxonomy, previously
  untestable because "it needs mandate expiry, which lands with the mandate
  layer" — is now testable, and is tested deterministically
  (`tests/test_mandate.py::test_expired_mandate_is_refused`). It is
  deliberately **not** added to the LLM corpus: the eval gateway runs without
  mandates, so corpus cases there would test nothing. Padding the corpus to
  claim nine of nine classes would be the exact sin ADR 0011 refused.
- 19 new tests. The gateway now has two failure vocabularies —
  `mandate_*` for authority, bare names for policy — and `rule_fired` still
  names exactly one, which the demo depends on.
- **What this still does not do:** no HITL escalation, no durable/shared nonce
  store (in-memory, so replay protection does not survive a restart or span
  processes), no key rotation, and the corpus numbers do not cover it.
