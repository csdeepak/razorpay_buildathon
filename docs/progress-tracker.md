# Progress Tracker

Daily percentage-complete tracking against
`docs/context/Razorpay_16_Day_Battle_Plan.md`, per rule 6 in `CLAUDE.md`: a
slipping gate means cut scope, not extend the phase. Update this every day
worked, even if the update is "0% today, here's why."

Plan baseline: Day 1 = Thu 20 Aug 2026. Deadline confirmed as 5 September
2026 (no time-of-day/timezone published) — see `docs/gate-0-tracker.md`.

## Phase checklist

### Phase 1 — Landscape + problem hunt · Days 1–3 · target 15%
- [x] Day 1 (Thu 20): Gate 0 resolved (done Day 2, see below) + landscape sheet ~50%
- [x] Day 2 (Fri 21): Problem bank scored against the 5 real tracks (20 rows) — see `docs/decisions/0002-problem-bank-scored-against-real-tracks.md`. Landscape sheet still not finished.
- [x] Day 3 work (done early, Fri 21): Cut to 3 (see `docs/decisions/0003-cut-to-three.md`); one-pagers written in `submission/one-pagers/`
- [ ] 5 outreach messages sent — still open, Deepak's own outreach
- **Gate 1 (end Day 3): written half done a day early.** Three problems, each with a written one-pager, in `submission/one-pagers/`. Outreach messages still needed before Day 4 conversations can start.

### Phase 2 — Validate + lock · Days 4–5 · target 25%
- [x] Day 4 work (done early, Fri 21): 5 real conversations logged in `outreach/01-day4-round-five-conversations.md` — Track 01 strongest, especially among the two most judge-relevant respondents
- [x] Day 5 work (done early, Fri 21): **Problem LOCKED** — Track 01, agent trust/safety/audit layer ("Warden"). ADR: `docs/decisions/0004-problem-locked-track-01.md`. Demo script drafted in `submission/demo-script.md` *before any code*.
- **Gate 2 (end Day 5): CLEARED, three days early.** Hard lock in effect. No new problem after this — `CLAUDE.md` rule 1.

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
| 2026-08-21 | 2 | — | Repo restructured into `razorpay_buildathon` — docs, decisions log, gate/progress trackers, submission scaffold, Claude Code workflow commands set up. **Gate 0 resolved**: opened razorpay.com/buildathon/ live — World A confirmed, all 5 tracks now known (only 1 was known before), pre-built work confirmed required, solo application, Track 01 has confirmed Razorpay test-mode API access. See `docs/decisions/0001-gate-0-resolved.md`. **Problem bank (20 candidates) scored against the 5 real tracks** — Track 01 is the strongest fit for the existing top cluster (#1/#3/#2/#5), #9 is the biggest mover (VALIDATE → matches Track 04's own example direction). See `docs/decisions/0002-problem-bank-scored-against-real-tracks.md`. **Cut to 3**: #1/#3/#5/#2 merged into one Track 01 system, plus #8 (Track 02) and #9 (Track 04) as hedges. Three one-pagers written. See `docs/decisions/0003-cut-to-three.md`. **5 real conversations logged** (`outreach/01-day4-round-five-conversations.md`) — Track 01 got maximum reactions from the security engineer and Razorpay product/AI respondents. **Problem LOCKED** on Deepak's go-ahead: Track 01, agent trust/safety/audit layer, working name "Warden." See `docs/decisions/0004-problem-locked-track-01.md`. Demo script drafted. Gates 1 and 2 both cleared three days ahead of the plan's own schedule. Landscape sheet (Phase 1) is the one thing from this stretch still not finished — low priority now that the problem is locked. |
