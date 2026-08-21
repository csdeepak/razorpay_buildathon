---
description: Append today's entry to docs/progress-tracker.md
---

Ask the user (if not already stated in the conversation) what was completed
today and their honest percentage-complete estimate against the current
phase's target in `docs/progress-tracker.md`.

Then:
1. Compute the plan day number from the date (Day 1 = 2026-08-20).
2. Append a row to the Log table in `docs/progress-tracker.md`: date, day
   number, % complete, one-line notes.
3. Tick any phase checklist boxes that are genuinely done — don't tick
   something half-finished just to show progress.
4. If the day's target percentage (stated at the top of each phase section)
   was missed, say so plainly and ask whether scope should be cut per
   `CLAUDE.md` rule 6 — don't silently let the phase extend instead.
