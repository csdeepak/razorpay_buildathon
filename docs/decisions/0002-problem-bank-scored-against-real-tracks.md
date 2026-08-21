# 0002 — Problem bank scored against the 5 real tracks

Date: 2026-08-21
Status: proposed

## Context

`docs/decisions/0001-gate-0-resolved.md` surfaced five real Buildathon tracks
where the problem bank in
`docs/context/Razorpay_Landscape_and_Problem_Scoring.xlsx` had only been
scored against a hypothetical single track. Day 2 of
`docs/context/Razorpay_16_Day_Battle_Plan.md` calls for finishing the problem
bank; the real track definitions (each with a named "bar" and, in one case,
confirmed API access) are new, load-bearing inputs to that scoring that
didn't exist when the original 20 candidates were seeded.

## Decision

Added three columns to the **Problem Bank** sheet — `Best-fit track`,
`Track fit (1-10)`, `Track fit flags / notes` — scoring all 20 existing
candidates against the 5 tracks confirmed in ADR 0001, plus a "TRACK FIT
SUMMARY" block below the existing legend. The original 6-criteria scores,
weights, and formulas were left untouched; this is an additive second pass,
in the same spirit as the sheet's own instruction that scores are "seeds to
argue with, not answers."

Headline findings:
- Track 01 (AI Growth & Agentic Commerce) is the strongest fit for the
  already-highest-scored candidates (#1, #3, #2, #5) — its stated bar
  ("explainable, bounded and gated," "audit trail," "one failure handled
  gracefully") reads as a near-literal description of that cluster, and it's
  the only track with confirmed real test-mode API access.
- #9 (deduction forensics / settlement Q&A) is the single biggest mover:
  VALIDATE-tier on the original 6 criteria, but it name-matches Track 04's
  own listed example direction ("Settlement Q&A agent").
- Two tensions surfaced: Track 02 and Track 04 both list example directions
  ("Chargeback evidence responder," "Forward cash forecaster") that Agent
  Studio already ships as pre-built agents — the same collision the original
  bank auto-killed candidates #18–20 for. Flagged in each affected row's
  notes rather than resolved here.

## Alternatives considered

- **Folding track fit into the existing weighted `Total` formula as a 7th
  criterion** — rejected. The weighting scheme (0.25/0.2/0.2/0.15/0.12/0.08)
  is Deepak's own and owning any change to it isn't this pass's call; adding
  columns keeps the original formula machinery untouched and lets him decide
  whether/how to merge the two scores.
- **A separate markdown doc instead of editing the spreadsheet** — rejected.
  The spreadsheet is the working artifact for this exact task and the one
  Deepak will actually open Day 2/3; a parallel doc would fork the source of
  truth.

## Consequences

- This does not cut the bank to 3 (`Gate 1`, end of Day 3) or lock a problem
  (`Gate 2`, end of Day 5) — both stay Deepak's calls, informed by this pass
  plus real conversations.
- A LibreOffice recalculation pass (`recalc.py`) could not run on this
  Windows machine (no LibreOffice install; the sandboxed recalc script
  requires `AF_UNIX`, unavailable on Windows). The `WEIGHTED` column's
  formulas were not modified — only its previously-cached values were at
  risk of being dropped by the openpyxl save. Fixed by splicing the original
  cached values (pulled from the prior git commit, not recomputed) directly
  into the sheet XML, so both the formula and the correct cached result are
  present. Recommended: re-run `recalc.py` from a Linux/macOS environment (or
  just open the file in Excel/Google Sheets, either of which force a full
  recalculation on load — `calcPr fullCalcOnLoad="1"` is already set) next
  time a real change touches the `WEIGHTED` formulas.
