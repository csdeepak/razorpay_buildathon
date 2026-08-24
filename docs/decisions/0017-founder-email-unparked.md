# 0017 — The founder email: unparked, drafted, and Deepak's to send

Date: 2026-08-24
Status: **locked** (decision), **awaiting Deepak** (the send itself)

## Context

A Razorpay founder gave Deepak direct email access and asked to see built
projects. `CLAUDE.md` rule 8 and `submission/founder-email.md` have kept that
channel deliberately parked, with an explicit unlock condition set in
[ADR 0004](0004-problem-locked-track-01.md):

> a problem-lock ADR exists in `docs/decisions/`, ideally with the Phase 3–4
> spine (`src/`) and evaluation numbers (`eval/`) already real, so the email
> references a shipped system rather than an intention.

`transfer.md` flagged in the previous session that the condition "now looks
satisfied" and that it deserved *"a deliberate decision, not an assumption."*
This ADR is that decision, made rather than drifted into.

Every clause of the condition is met, and by a margin: the problem locked on
Day 5 (ADR 0004), `src/` runs end to end against Razorpay's real test-mode API
(ADR 0010, a genuine `rfnd_...` id), and there are 24 recorded findings across
fourteen models. Since this week there is also something the condition did not
anticipate and that changes the calculus: **a finding about a live Razorpay
product.** Agent Studio ships a Dispute Responder on Anthropic's Claude SDK,
and all three Claude models tested close a case on a forged *"already
refunded"* note, every time.

## Decision

**Unpark it. Draft it. Do not send it — that is Deepak's call and Deepak's
send.**

The parking rule existed to stop the channel being spent on an intention.
It is not a rule against ever using the channel, and holding it further now
costs something real: the Buildathon closes 5 September, the form is
effectively anonymous until a panel reads it, and the founder channel is the
one place where the work is attached to a name in advance.

Three constraints on the draft, all of which follow from rules this repo
already runs on:

1. **Lead with the finding about their product, not with the project.** The
   asset is *"I tested the model family your Agent Studio runs on, and here is
   what it does with a forged note"* — a measurement about their surface, not
   a student describing a build.
2. **Include the self-corrections.** The affordance confound (ADR 0013) and
   the false-alarm rate that measured nothing (ADR 0014) are the strongest
   material in the whole submission, and they are exactly what a founder's
   office is screening for. An email that only reports wins reads like every
   other one in the inbox.
3. **No synthetic anything, no inflated claims, and no ask beyond a read.**
   `CLAUDE.md` rule 5 applies to this channel too.

## Alternatives considered

- **Keep it parked until the video is recorded.** Tempting for tidiness.
  Rejected: the repo is public and runnable now, and the email's value is
  time-decaying against a 5 September deadline. If the founder replies asking
  for a video, that is a good problem.
- **Send it instead of applying through the form.** Rejected outright. The
  form is the actual hiring process; the email is a parallel channel, not a
  substitute, and treating it as a shortcut would read exactly that way.
- **Have Claude send it.** Not on the table. It is an outward-facing message
  to a real person under Deepak's name, and the drafting/sending split is the
  correct one regardless of how ready the draft looks.
- **Lead with the 71/71 headline.** Rejected — that is the number this week's
  ablation put an asterisk on, and sending an overclaim to the one contact who
  cannot be re-pitched would be the worst possible place to make that mistake.

## Consequences

- `CLAUDE.md` rule 8 is now **discharged**, not broken. The rule said "parked
  until the thesis is locked"; the thesis is locked and the condition is met.
  A future session should read rule 8 alongside this ADR rather than as a
  standing block.
- `submission/founder-email.md` carries a real draft below its status line,
  and the status line changes from **DO NOT SEND** to **READY — Deepak sends**.
- If it is sent and a reply lands, that is a real conversation and it belongs
  in `outreach/` under the existing rules — role not name unless attribution
  is agreed, what surprised him, and whether it changed the thesis.
- Risk accepted: a founder who reads a long email badly is worse than one who
  never received it. Mitigated by keeping it to a screenful, leading with a
  concrete measurement, and asking only for a read.
