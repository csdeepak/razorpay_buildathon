# Gate 0 — Buildathon Mechanics (blocks everything)

Source: `docs/context/transfer.md` §3. As of the last transfer note
(2026-08-20), every fact below traced to a **single third-party X post**,
never verified against the primary page. `razorpay.com/buildathon/` is
client-rendered — automated fetch tools only ever returned SEO metadata, never
body copy. **This must be resolved by opening the page in a real browser.**

Status: **UNRESOLVED** — update this file the moment it's checked.

## The six questions

- [ ] 1. Real application deadline and timezone (currently assuming 5 Sept 2026, unconfirmed).
- [ ] 2. Full track list (only "AI Growth & Agentic Commerce" confirmed).
- [ ] 3. Submission format — repo? demo video? deck? live presentation?
- [ ] 4. **Pre-built-work rule.** The single most important unresolved line —
      the entire 16-day pre-build plan assumes prior work is allowed.
- [ ] 5. Razorpay API sandbox / Agent Studio / Vulcan access for participants,
      or is everything mocked? (Assume mocked until proven otherwise.)
- [ ] 6. Team or solo?

## Which world are we in?

- **World A** — apply by the deadline with a project attached → the 16-day
  build plan in `docs/context/Razorpay_16_Day_Battle_Plan.md` is correct as-is.
- **World B** — the deadline is registration only, building happens later →
  research/validation days are still pure profit, the build phase shifts.
- **World C** — on-site timed sprint, pre-built work banned → the entire
  build plan is wrong; the 16 days become rehearsal/domain-fluency prep, not
  a submission.

Current assumption: **World A** (unverified).

## Once resolved

1. Fill in the checkboxes and answers above.
2. Write an ADR in `docs/decisions/` capturing which world applies and why —
   this is exactly the kind of "new thing invented/confirmed" the decision
   log exists for.
3. Update `docs/progress-tracker.md` with the real deadline and recomputed
   days remaining.
