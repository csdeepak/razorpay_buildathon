# Settlement Deduction Forensics / Reconciliation Agent

**Track:** 04 — AI Finance Controller
**Original candidate:** #9.
**Score:** 6.98 (original 6-criteria, VALIDATE-tier) · 9/10 track fit — the
single biggest mover once the real tracks were known.

## The problem

Trace an unexplained settlement deduction to its root cause with a fully
auditable chain. Track 04's own bar: close one finance-ops loop over a
50+ record batch, report the match rate, and give an honest list of the
exceptions it could not resolve.

## Who feels the pain

Finance teams and chartered accountants reconciling Razorpay settlements —
sourced directly from Razorpay's own blog language: *"unexplained deductions
finance teams cannot trace."* Rare to have the pain point in the target
company's own words rather than inferred.

## Why now

Track 04 lists **"Settlement Q&A agent"** as a named example direction —
close to a word-for-word match for this candidate. Track 04's own stated
"why now": *"verification capacity, not generation speed, is the
bottleneck"* — reconciliation, settlement, and forecasting are still mostly
done by hand.

## What "solved" looks like

Given a batch of 50+ synthetic settlement records, the agent matches
transactions to settlement deductions, explains each deduction's cause via a
traceable, auditable chain, and reports a match rate plus an honest
exception list for what it couldn't resolve. Track 04's own words: *"one
cherry-picked match proves nothing."*

## Demo beat (90 seconds)

Run against a batch → match rate climbs on screen → trace one deduction
end-to-end from settlement report to root cause → show the honest exception
list, not a swept-under-the-rug 100%.

## Biggest open risk

The original note for #9 asked the sharper question directly: *"is this
AI-shaped, or just a better report?"* If Day 4 conversations reveal the real
bottleneck is data access or a UI gap rather than something an LLM's
reasoning genuinely adds to, this candidate should be the first cut — a
well-built deterministic reconciliation script isn't a Buildathon-worthy
answer to a track literally named "AI Finance Controller."
