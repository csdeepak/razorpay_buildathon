# Context (research + working scoring tool)

Three of these four files are the frozen historical record from the session
that produced the original strategy; one is a live working tool. Don't
conflate them.

- **`transfer.md`** — the handoff note. Start here if you need the compressed
  version of everything below. States who Deepak is, what's verified about
  Razorpay, the top-3 scored problem candidates, and the immediate next action.
  **Frozen — read-only.**
- **`Razorpay_Buildathon_Research_Phase1.md`** — the original deep-dive:
  sourced facts about Razorpay's 2026 AI direction (Vulcan, Agent Studio,
  Agentic Platform, Sprint 2026), competition intelligence, and the
  white-space analysis. **Frozen — read-only.**
- **`Razorpay_16_Day_Battle_Plan.md`** — the critique of the original plan
  plus the day-by-day roadmap this whole repo's `docs/progress-tracker.md`
  is built from. Read §1 (verdict) and §6 (rules of engagement) even if
  you skip the rest. **Frozen — read-only.**
- **`Razorpay_Landscape_and_Problem_Scoring.xlsx`** — 4 sheets: Razorpay
  Landscape (23 product areas), Problem Bank (20 candidates scored against
  the original 6 criteria, plus a second pass scored against the 5 real
  Buildathon tracks — see `docs/decisions/0002-problem-bank-scored-against-real-tracks.md`),
  16-Day Tracker, Sources. **Living document, edit it freely** — its own
  header says the scores are "seeds to argue with, not answers." This is
  where Day 2/3 scoring work actually happens; log anything that changes the
  problem thesis as an ADR, but don't hesitate to overwrite a score here.

For the three frozen files: if a fact turns out to be wrong or a decision
gets superseded, don't edit them — write a new ADR in `docs/decisions/`
instead and let them stay an honest snapshot of what was known/decided on
2026-08-20. Referenced facts and dates inside those three (e.g. "today is 20
Aug 2026") are frozen at time of writing — do not treat them as live.
