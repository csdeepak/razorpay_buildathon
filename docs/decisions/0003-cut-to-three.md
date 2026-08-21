# 0003 — Cut to three (Gate 1)

Date: 2026-08-21
Status: proposed

## Context

Gate 1 (`docs/progress-tracker.md`, end of Day 3) calls for cutting the
20-candidate problem bank to three, each with a one-pager, ahead of Day 4's
real conversations. `docs/decisions/0002-problem-bank-scored-against-real-tracks.md`
changed the shape of this cut: the four highest-scored candidates on the
original 6 criteria — #1 (prompt-injection defence), #3 (policy enforcement
gateway), #5 (tamper-evident audit trail), #2 (verifiable-intent layer) — all
map to Track 01 and, per that ADR's own "headline read," **converge into one
coherent system** rather than four independent alternatives. Treating them as
three separate one-pagers would spend two of the three precious Day 4
validation slots re-testing facets of the same idea instead of hedging
against it being wrong.

## Decision

Three survivors, each a genuinely different hypothesis, each anchored to a
different real track:

1. **Agent trust/safety/audit layer for agentic payments** — merges original
   candidates #1, #3, #5, and #2 into one system: an agent's money-moving
   action gets reasoned about, gated against policy (scopes/caps/velocity),
   executed on Razorpay test-mode APIs, and logged to a tamper-evident audit
   trail, with a prompt-injection attack as the headline failure case caught
   on screen. Track 01. One-pager:
   `submission/one-pagers/01-agent-trust-safety-audit-layer.md`.
2. **Pre-payment vendor-invoice fraud/anomaly detector** — original
   candidate #8. Track 02. One-pager:
   `submission/one-pagers/02-vendor-invoice-fraud-detector.md`.
3. **Settlement deduction forensics / reconciliation agent** — original
   candidate #9. Track 04. One-pager:
   `submission/one-pagers/03-settlement-deduction-forensics.md`.

## Alternatives considered

- **Literal top-3 by original weighted score** (#1, #3, #2, unmerged) —
  rejected for the reason in Context: it isn't three hypotheses, it's one
  hypothesis wearing three one-pagers, and it doesn't buy any diversification
  for Day 4.
- **#6 (agent identity/reputation/trust marketplace), 8.04 orig, STRONG** —
  rejected. Flagged twice already, in the original bank's own note ("risk:
  reads as ASMOS relabelled") and in `CLAUDE.md` rule 7 (don't add a feature
  "because ASMOS already has it"). Picking it as a Gate-1 survivor would be
  exactly that impulse with extra steps.
- **#11 (payout failure recovery with rollback), Track 03, fit 8/10** —
  closest runner-up to #9 for the third slot; Track 03's own example
  direction ("Payment degradation → root cause → recovery action") matches
  it almost as tightly as Track 04's matches #9. Kept in reserve: if Day 4
  conversations kill #9 or #8, this is the first replacement to reach for,
  not a re-scoring of the whole bank.
- **#4 (risk-aware HITL escalation)** — not given a separate one-pager
  because it's conceptually a facet of survivor #1's policy-gating layer
  (deciding *when* to interrupt a human is part of the same gate/escalate
  mechanism), not a distinct problem.

## Consequences

- Three one-pagers now exist in `submission/one-pagers/`, satisfying Gate 1's
  written requirement.
- The "5 outreach messages sent" half of Gate 1 is still open — that's
  Deepak's own outreach, not something done here.
- This is **not** the Day 5 lock (`Gate 2`). Any of the three can die on
  contact with a real conversation; #11 is the named fallback if one does.
