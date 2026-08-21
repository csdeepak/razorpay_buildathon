# Pre-Payment Vendor-Invoice Fraud/Anomaly Detector

**Track:** 02 — AI Risk Manager
**Original candidate:** #8.
**Score:** 7.62 (original 6-criteria) · 9/10 track fit.

## The problem

Before money leaves via vendor/invoice payments, catch duplicate invoices,
anomalous amounts, or fraud patterns — one narrow, well-scoped class of loss,
matching Track 02's own bar exactly: *"a working detector, verifier or
auto-responder for one class of loss, with measured precision and recall on
a held-out test set."*

## Who feels the pain

Accounts-payable and enterprise finance-ops teams paying vendors through
Razorpay-like rails.

## Why now

Razorpay's Vendor Payments product already exists, so the workflow this sits
inside is real. AI-enabled fraud is actively hitting Indian BFSI (per
Track 02's own "why now"), and Track 02 was built explicitly to surface "the
risk and ML minded builders the others miss" — a different muscle than
Track 01's agent-safety framing.

## What "solved" looks like

A detector trained and tested on a held-out invoice dataset flags duplicate
or anomalous invoices before payment executes, reporting honest precision,
recall, and false-positive cost — not just a catch count. Strictly
defense-only: detection and flagging, nothing offense-capable, satisfying
Track 02's disqualification rule directly.

## Demo beat (90 seconds)

Feed a batch of invoices, including planted duplicates and anomalies → the
detector flags them before payment → precision/recall and false-positive
cost shown on screen, not a single cherry-picked catch.

## Biggest open risk — this is a hypothesis, not a validated pain

The original problem-bank note for #8 flagged this explicitly: **the pain is
unvalidated.** This is exactly the kind of candidate Day 4's real
conversations exist to test — if an AP or finance-ops person doesn't
recognize this as a real, current headache within the first two minutes of
conversation, that's the signal to let it go rather than argue with the
data.
