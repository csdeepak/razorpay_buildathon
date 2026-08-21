# Agent Trust/Safety/Audit Layer for Agentic Payments

**Track:** 01 — AI Growth & Agentic Commerce
**Merges original candidates:** #1 (prompt-injection defence), #3 (policy
enforcement gateway), #5 (tamper-evident audit trail), #2 (verifiable-intent
layer, as the mechanism underneath) — see `docs/decisions/0003-cut-to-three.md`.
**Score:** 8.92 (original 6-criteria, as #1) · 10/10 track fit.

## The problem

An AI agent transacting on a merchant's behalf can be hijacked — a prompt
injection mid-task, a scope it was never granted, a spend limit it should
never cross — and today there is no working, demoable way to prove, before
or after the fact, that a given money-moving action was explainable, bounded,
gated, and actually authorized. Razorpay's own co-founder has staked out the
philosophy ("the agent never sees" the credential) without publishing the
mechanism. India's regulator has mandated the outcome (human-in-the-loop
above thresholds, full audit trails) without saying who builds it.

## Who feels the pain

Merchants and platforms (like Razorpay) exposing payment rails to
first-party or third-party AI agents — precisely Track 01's own framing of
"agentic commerce," and precisely the trust boundary Agent Studio's
announced-but-unshipped third-party agent ecosystem will eventually need.

## Why now

- CERT-In / MeitY Digital Threat Report 2025-26 (16 Jul 2026): mandatory
  human-in-the-loop above financial thresholds, with full audit trails —
  silent on who implements it.
- NPCI's Unified Agent Protocol: registering/authorizing agents on UPI,
  still pre-launch, needs RBI approval.
- Harshil Mathur (Razorpay co-founder): the agent must never see the payment
  credential — no published authorization mechanism.
- Track 01's own stated bar, word for word: *"every money action explainable,
  bounded and gated... show the audit trail and one failure handled
  gracefully"* — and it's the only track with confirmed Razorpay test-mode
  API access, so the demo can run against something real.

## What "solved" looks like

An agent attempts a payment. The policy gateway checks it against scopes,
spend caps, velocity, and category/time bounds before it reaches the rail.
An out-of-policy or hijacked attempt is blocked in real time. Every allowed
and blocked action is written to a tamper-evident, replayable audit log.
Under adversarial testing (Day 11–12, `eval/`), the system reports a real
catch rate across N attack cases — not a single staged success.

## Demo beat (90 seconds)

Agent gets prompt-injected mid-task → tries to pay an attacker → the gateway
blocks it → the audit record for that block is shown → the catch rate across
the adversarial case set is shown on screen. Matches the target sentence in
`submission/demo-script.md`.

## Biggest open risk

Abstract-demo risk: "agent authorization infrastructure" can degrade into a
permissions config screen if the attack isn't made visceral. The prompt-
injection attack must be the visible headline, with the policy/audit
mechanics as supporting evidence, not the other way round.
