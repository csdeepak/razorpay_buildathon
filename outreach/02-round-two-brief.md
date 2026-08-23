# Round 2 — Showing the *built* system

**Status: prep. No conversations logged yet.**
Created 2026-08-23. Log results in `03-...`, `04-...` etc. per
`outreach/README.md`'s naming.

## Why this round exists, and how it differs from Round 1

Round 1 (`01-day4-round-five-conversations.md`) asked *"which of these three
problems is real?"* — before any code existed. It did its job: Track 01 got
the strongest reaction from the two most judge-relevant respondents, and the
problem was locked on it.

But it validated a **problem statement**, and the submission now rests on a
**built system with a surprising result**. Razorpay's stated rubric includes
*problem taste*; evidence gathered before the build cannot speak to whether
the thing that got built is the right thing.

This round asks a different question, and it is the one worth asking:

> **Does the denial finding land as a real threat with someone who would have
> to defend against it — or does it read as a lab curiosity?**

That is falsifiable. If a security engineer says *"we'd catch that in
reconciliation the next morning, it isn't interesting"*, that is a genuine
problem with the thesis and it is much better to hear it now than in a Q&A.

## Who to talk to (2–3 is enough)

Priority order, by how much their reaction would move a judge:

1. **The security engineer from Round 1.** Gave Track 01 its maximum reaction
   *before* seeing anything built. Their reaction to the actual result is the
   single most valuable data point available, and re-contacting someone who
   already engaged is the easiest ask on this list.
2. **The Razorpay product/AI person from Round 1.** Closest available proxy
   for a judge. If they see the Finding 17 correction — that refunds cannot
   be redirected on Razorpay's own rail — their reaction tells you whether
   naming it was the right call.
3. **Whoever gave you the founder-office contact.** Independent of this round,
   they should see the built thing before any founder email goes out
   (`submission/founder-email.md`, still parked).

Anyone in fintech ops, payments, or fraud/risk is a reasonable substitute.
**Two real conversations beat five polite ones.**

## What to show — in this order, ~5 minutes

Do **not** open with the architecture. Open with the failure.

1. **The scenario, in one sentence.** "A support agent that can issue refunds.
   Someone puts a fake note on the order saying the refund already went out."
2. **What every model does.** It believes the note, closes the case, asks if
   there's anything else it can help with. The customer is never paid.
3. **The number.** 56/56 — nine models, three labs, 9B to frontier. *Then
   pause.* This is the moment the conversation is actually about.
4. **Why nothing catches it.** Nothing bad was proposed; a good action was
   suppressed. A preventive gate has nothing to refuse.
5. **The fix, briefly.** A post-session audit that never reads the
   conversation — it asks the ledger whether an open obligation went
   undischarged. 56/56 caught, 0 false alarms in 134 benign sessions.

Optional, only if they're engaged: Finding 19 — a refund is a fresh
disbursement from merchant balance, so it can fail for reasons unrelated to
the payment and leave the same undischarged obligation with no attacker
involved at all.

## What to actually ask

The value is in what they volunteer, so ask few questions and leave silence.

- **"Would this get caught today, in a system you've worked on?"**
  The key question. If yes — *how*, and how long would it take?
- **"Is the absence of a payment something anything you run alarms on?"**
  Most monitoring watches for bad events, not missing ones. Worth testing.
- **"Where would you put this — the agent, the payment layer, or reconciliation?"**
  Tests whether the architectural placement is right.
- **"What would stop you deploying it?"**
  Invites the objection. Take it seriously if it comes.

Do **not** ask "is this useful?" or "does this seem valuable?" — those are
questions people answer politely, which is how you learn nothing.

## What to capture

Per `outreach/README.md`: role not name (unless they okay attribution), what
they said **unprompted**, what surprised you, and whether it changed the
thesis.

**Quote verbatim where you can.** A sentence in someone else's words is worth
more in the narrative than any paraphrase — `submission/narrative.md` §2
currently has none, and it is the section's weakest point.

## Rules that still bind

- **`CLAUDE.md` rule 5.** No synthetic or AI-roleplayed respondent, ever. If
  you rehearse this pitch against a persona first, that rehearsal is private
  and is never logged here or cited anywhere.
- **A thesis change is a decision.** If someone says "the real problem is X"
  and it lands, that is an ADR in `docs/decisions/`, not a quiet edit.
- **Report what was said, including the flat reactions.** Round 1's most
  useful finding was the D2C merchant's *lukewarm* response — it is why the
  demo carries the visceral weight instead of the pitch.
