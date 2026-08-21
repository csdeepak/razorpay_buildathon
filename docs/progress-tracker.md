# Progress Tracker

Daily percentage-complete tracking against
`docs/context/Razorpay_16_Day_Battle_Plan.md`, per rule 6 in `CLAUDE.md`: a
slipping gate means cut scope, not extend the phase. Update this every day
worked, even if the update is "0% today, here's why."

Plan baseline: Day 1 = Thu 20 Aug 2026. Real deadline unconfirmed — see
`docs/gate-0-tracker.md`.

## Phase checklist

### Phase 1 — Landscape + problem hunt · Days 1–3 · target 15%
- [ ] Day 1 (Thu 20): Gate 0 resolved + landscape sheet ~50%
- [ ] Day 2 (Fri 21): Landscape finished; problem bank scored (20 rows)
- [ ] Day 3 (Sat 22): Cut to 3; one-pagers written; 5 outreach messages sent
- **Gate 1 (end Day 3):** three problems, each with a written one-pager in `submission/one-pagers/`.

### Phase 2 — Validate + lock · Days 4–5 · target 25%
- [ ] Day 4 (Sun 23): 3–5 real conversations logged in `outreach/`
- [ ] Day 5 (Mon 24): Problem locked (ADR in `docs/decisions/`); demo script written in `submission/demo-script.md` *before any code*
- **Gate 2 (end Day 5):** hard lock. No reopening after this.

### Phase 3 — Build the spine · Days 6–10 · target 60%
- [ ] Day 6–7: Vertical slice runs end-to-end (reason → decide → act(mocked) → verify → audit)
- [ ] Day 8: Safety layer (permissions/scopes/limits/velocity)
- [ ] Day 9: Verification layer (the moat)
- [ ] Day 10: Audit layer (every consequential action recorded, replayable, queryable)
- **Gate 3 (end Day 10):** loop runs end to end on one real scenario, or scope gets cut — do not extend the phase.

### Phase 4 — Evidence · Days 11–13 · target 85%
- [ ] Day 11: Evaluation harness + adversarial cases built (`eval/`)
- [ ] Day 12: Harness run, numbers captured, multi-seed where applicable
- [ ] Day 13: UI / demo surface — only now
- **Gate 4 (end Day 13):** real numbers, not vibes.

### Phase 5 — Narrative + ship · Days 14–16 · target 100%
- [ ] Day 14: Demo recorded (90 seconds)
- [ ] Day 15: Submission narrative written (`submission/narrative.md`), README made stranger-runnable
- [ ] Day 16: Buffer. Submit morning of, never at the literal deadline.

## Log

| Date | Day | % complete | Notes |
|---|---|---|---|
| 2026-08-20 | 1 | — | Research phase 1, battle plan, and problem-scoring spreadsheet produced. Gate 0 not yet resolved. |
| 2026-08-21 | 2 | — | Repo restructured into `razorpay_buildathon` — docs, decisions log, gate/progress trackers, submission scaffold, Claude Code workflow commands set up. No landscape/problem-bank work logged yet today. |
