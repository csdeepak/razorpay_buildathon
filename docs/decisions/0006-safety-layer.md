# 0006 — Safety layer: the pipeline becomes preventive

Date: 2026-08-21
Status: locked

## Context

`docs/decisions/0005-vertical-slice-architecture.md` built the Day 6–7
vertical slice with a known, intentional gap: no pre-execution gate, so the
attack scenario's mocked payout executed and `verify` only caught it
afterward. That ADR named Day 8 (`docs/progress-tracker.md`, Phase 3) as
where this gets closed, matching
`docs/context/Razorpay_16_Day_Battle_Plan.md`'s own line: *"Safety layer:
permissions, scopes, limits, velocity. The 'agent never sees the credential'
boundary, implemented."* `submission/demo-script.md`'s catch beat already
described this exact behavior ("the call never reaches the rail") before it
existed in code — today's build makes that line true.

## Decision

Added `src/safety/policy_gateway.py` (`PolicyGateway`) and
`src/memory/state.py`'s `VelocityTracker`, and moved the gate into the
pipeline **before** `act`:

    reason -> decide -> safety gate -> act (mocked, only if allowed) -> verify -> audit

`PolicyGateway.check()` runs four rules in fixed order, stopping at the
first failure, so `PolicyVerdict.rule_fired` always names exactly one rule:

1. `category` — is this action type one the merchant allows at all
2. `payee_scope` — for a refund, destination must equal the order's own
   original payment instrument
3. `spend_cap` — single-transaction ceiling
4. `velocity_amount` / `velocity_count` — cumulative amount/count per UTC day

On the attack scenario, `payee_scope` fires and the mocked payout is never
called. `verify` still runs regardless (it doesn't depend on execution) and
independently agrees — the CLI now says so explicitly: *"two different
mechanisms catching the same attack, not one point of failure."*

`PolicyGateway.check()` records to `VelocityTracker` itself, atomically,
when it allows an action — see Consequences for why this mattered.

## Alternatives considered

- **Have the pipeline (or the caller) record velocity separately from the
  check call.** Tried first, and it was a real bug, not a hypothetical:
  `check()` read velocity state but nothing ever called
  `VelocityTracker.record()` on a successful check, so the daily caps were
  silently unenforceable — they'd always read as "nothing spent yet." Caught
  by writing `tests/test_safety.py` before trusting the rule mattered.
  Fixed by making the gateway record internally on allow, so there's no code
  path that returns "allowed" without also recording it.
- **Give `payee_scope` a separate, merchant-configured allow-list instead of
  deriving it from `OrderRecord`.** Rejected for now — the only action type
  modeled is `refund`, where "must return to the original payment
  instrument" is how refunds actually work, not an arbitrary policy choice.
  A configurable allow-list becomes real once a second action type (e.g. a
  vendor payout) exists; premature today.
- **Skip testing spend cap / velocity / category since the two demo
  scenarios don't exercise them.** Rejected — `CLAUDE.md` rule 2 says
  nothing earns build time that isn't in the demo script, but *testing* a
  built rule isn't the same as building new demo material. Unit-tested
  `PolicyGateway` directly in `tests/test_safety.py` instead of inventing
  off-script CLI scenarios.

## Consequences

- `submission/demo-script.md`'s catch beat is now literally true, not
  aspirational — re-verify against `make demo` output next time that file is
  edited.
- Gate 3 (`docs/progress-tracker.md`) stays cleared; this deepens the spine
  rather than re-opening it.
- Day 9 (verification, the moat) and Day 10 (audit, replay/queryability)
  still stand as the two deepening passes left in Phase 3.
- `eval/`'s Day 11 adversarial harness has a real gateway to attack now, not
  just a reasoner and a verifier — worth generating cases that specifically
  target each of the four rules, not just `payee_scope`.
