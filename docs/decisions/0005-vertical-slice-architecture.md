# 0005 — Vertical slice: stack, architecture, and the detective-not-preventive gap

Date: 2026-08-21
Status: locked

## Context

`docs/decisions/0004-problem-locked-track-01.md` locked Warden. Days 6–7
(`docs/progress-tracker.md`) call for a vertical slice — one complete path,
end to end, "ugly is fine, it must run" — through the stage order stated
literally in `docs/context/Razorpay_16_Day_Battle_Plan.md`: **reason →
decide → act (mocked) → verify → audit**. Safety is explicitly a separate
Day 8 addition in that same plan, not part of this slice.

## Decision

**Stack:** Python 3.11, pydantic v2 for typed models, pytest for tests.
Matches Deepak's strongest listed skills (`docs/context/transfer.md` §1) and
needs no build step for a 16-day clock.

**Architecture**, one module per layer under `src/`:

- `models.py` — shared pydantic models (`OrderRecord`, `Scenario`,
  `ProposedAction`, `ExecutionResult`, `VerificationVerdict`).
- `memory/state.py` — `OrderStore`, an in-memory ground-truth order lookup.
  Deliberately the *only* source of the "real" payment instrument — the
  reasoner and verifier both consult it, but the untrusted inbound message
  never carries it directly. This is a genuine (if simple) trust-boundary
  decision, not incidental.
- `agent/reasoner.py` — `NaiveReasoner` (default, fully offline: trusts any
  destination account explicitly stated in the message, falls back to the
  order's original instrument) and `LLMReasoner` (real Anthropic call,
  activates only if `ANTHROPIC_API_KEY` is set; untested in this
  environment — no key here, no `anthropic` package installed).
- `tool/razorpay_mock.py` — `MockRazorpayClient`, no network call, executes
  whatever it's handed. No preventive logic on purpose.
- `verification/verifier.py` — `Verifier`, checks the executed action's
  destination against `OrderRecord`, never against the message or the
  agent's own rationale.
- `audit/ledger.py` — `AuditLedger`, append-only hash-chained JSONL log with
  `verify_chain()` for tamper detection.
- `pipeline.py` / `cli.py` — orchestration and a `python -m src.cli
  --scenario {benign,attack}` entry point.
- `scenarios.py` — the two demo scenarios: a clean refund request, and the
  headline prompt-injection attack from `submission/demo-script.md`.

**The known, intentional gap:** because `verify` runs after `act` per the
plan's own literal ordering, today's pipeline is a *detective* control on
the attack scenario — the mocked payout executes to the attacker's account,
and only then does verification flag it. Confirmed by running both
scenarios (`make demo`, `make demo-benign`) and by `tests/test_pipeline.py`,
including a test that documents this gap explicitly
(`test_action_executes_before_verification_runs`) so it can't be mistaken
for an accident later.

## Alternatives considered

- **Add a pre-execution safety gate today, since it's obviously the "real"
  fix.** Rejected. The plan explicitly reserves this for Day 8
  (`docs/context/Razorpay_16_Day_Battle_Plan.md` Phase 3 table) and frames
  Day 6–7 as proving the pipeline runs at all. Building it early isn't a
  problem in itself, but it would blur what Day 8 actually delivers and
  quietly relitigate a schedule decision that wasn't this task's to change.
  The gap is also a better demo beat honestly told: it motivates Day 8
  instead of hiding why it's needed.
- **A real LLM-backed reasoner as the only option.** Rejected for today —
  no API key or `anthropic` package in this environment, and "must run"
  matters more than "must call a real model" for a Day 6–7 slice.
  `LLMReasoner` exists and is wired to activate automatically once a key is
  set, so this isn't deferred work, just untested work.
- **Skip the `memory/state.py` separation and read payment-instrument data
  straight off `Scenario`.** Rejected. Folding it into `OrderRecord`, looked
  up independently by both the reasoner (as a fallback) and the verifier (as
  ground truth), makes the trust boundary a real architectural fact instead
  of a naming convention — cheap now, and it's exactly the kind of thing
  that's expensive to retrofit once Day 8/9 build on top of it.

## Consequences

- Gate 3 (`docs/progress-tracker.md`, end of Day 10) requires the loop to
  run end to end on one real scenario — done today, three-plus days early.
- Day 8 has a concrete, demonstrated problem to solve: move (or add) a check
  before `act`, not just "build a safety layer" in the abstract.
- `eval/`'s Day 11 adversarial harness can build directly on
  `tests/test_pipeline.py`'s fixtures (`OrderStore`, `AuditLedger`,
  `MockRazorpayClient`) rather than reinventing scenario plumbing.
- `requirements.txt` and `pyproject.toml` (pytest config) now exist;
  `make setup` / `make test` / `make demo` / `make demo-benign` are wired to
  real commands instead of placeholders.
