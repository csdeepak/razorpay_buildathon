# 0004 — Problem locked: agent trust/safety/audit layer (Track 01)

Date: 2026-08-21
Status: **locked**

## Context

`docs/decisions/0003-cut-to-three.md` cut the bank to three candidates, each
anchored to a different Buildathon track. `outreach/01-day4-round-five-conversations.md`
recorded five real reactions across all three, satisfying the plan's 3–5
conversation quota for Gate 2 ahead of schedule.

The signal was directionally clear rather than close: **Track 01 (agent
trust/safety/audit layer)** drew maximum reactions from the two respondents
most likely to resemble an actual Buildathon judge — a security engineer and
a Razorpay product/AI person — independently of each other. Its weaker pull
with the D2C merchant and startup founder matched a risk the candidate's own
one-pager had already named before any conversation happened (abstract-demo
risk), which is evidence the risk model was right, not a new problem.
Track 04 (settlement forensics) pulled a genuinely strong secondary reaction,
especially from the CFO — real, not a consolation prize, and named below as
the fallback.

Deepak confirmed the lock explicitly rather than having it inferred from the
data alone.

## Decision

**Locked: the agent trust/safety/audit layer for agentic payments — an
agent's money-moving action gets reasoned about, gated against policy
(scopes/spend caps/velocity/category/time bounds), executed against Razorpay
test-mode APIs, and written to a tamper-evident audit trail, with a
prompt-injection attack as the headline failure case caught on screen.**
Track 01 — AI Growth & Agentic Commerce. Full spec:
`submission/one-pagers/01-agent-trust-safety-audit-layer.md`.

Working codename for the system: **Warden**. Purely internal shorthand for
docs and code — cheap to change before the Day 14–15 narrative if a better
name turns up; not itself a locked decision.

Per `CLAUDE.md` rule 1: **no new problem after this.** Track 02 and Track 04
are closed as headline candidates.

## Alternatives considered

- **Track 02 (invoice fraud detector)** — real pain, its strongest reaction
  by far (🔥🔥🔥) came from the D2C merchant, but flat with the security
  engineer and Razorpay product/AI respondents — the two whose read best
  predicts judging. Not locked.
- **Track 04 (settlement forensics)** — the honest runner-up. Strongest CFO
  reaction of the whole round (🔥🔥, higher than that CFO gave Track 01) and a
  strong secondary Razorpay product/AI read (🔥🔥🔥). **Kept as the named
  fallback**, consistent with `docs/decisions/0003-cut-to-three.md` — if the
  Track 01 vertical slice (Gate 3, end of Day 10) fails to run end-to-end and
  scope must be cut hard, this is where to look first, not a re-scoring of
  the whole bank.

## Consequences

- Next per `docs/progress-tracker.md`: write `submission/demo-script.md`
  *before any code*, then Days 6–10 build the vertical slice.
- `README.md` gets rewritten off the "pre-lock" placeholder to state the
  locked thesis plainly.
- Every layer built from here on must trace to this one-pager and the demo
  script — `CLAUDE.md` rule 2. `/demo-check` exists specifically to enforce
  this once `src/` has real code in it.
- If this candidate needs to be abandoned later, that is itself a decision
  requiring a new ADR referencing this one as superseded — not a silent
  pivot.
