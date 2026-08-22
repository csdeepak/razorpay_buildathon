# Application Form — Drafted Answers

The Razorpay AI Builder Internship form asks for 12 things
(`docs/gate-0-tracker.md` Q3). The personal fields are Deepak's to fill; the
four content fields are drafted below.

**The form states explicitly: *"the last one is the one we read first."***
That is Q12. It gets the most care on this page.

---

## Checklist

| # | Field | Status |
|---|---|---|
| 1 | Full name | Deepak's |
| 2 | College | Deepak's |
| 3 | Graduation year | Deepak's |
| 4 | In person from September? | Deepak's |
| 5 | 6 or 12 months (applicant's choice) | Deepak's |
| 6 | Resume file | Deepak's |
| 7 | Chosen track | ✅ drafted below |
| 8 | Project name | ✅ drafted below |
| 9 | What it solves | ✅ drafted below |
| 10 | **Public GitHub repo URL** | ⛔ **BLOCKED — repo still returns 404 unauthenticated** |
| 11 | 5-minute pitch video (unlisted OK) | ⛔ not recorded |
| 12 | **What broke, and how you got out** | ✅ drafted below |

---

## Q7 — Track

**Track 01 — AI Growth & Agentic Commerce**

## Q8 — Project name

**Warden**

*(Still technically a working name. It is used consistently across the repo,
the demo, and this narrative, so changing it now costs more than it gains.)*

## Q9 — What it solves

> A merchant support agent that can move money reads untrusted text all day —
> customer chat, order notes, ticket history. Razorpay's own stated principle
> is that the agent should never see the payment credential, and that's right,
> but it isn't enough: an agent that never touches a card number can still be
> talked into refunding the wrong person, the wrong amount, or — far more
> reliably — nobody at all.
>
> Warden is the enforcement layer that sits between the agent and the payment
> rail. Money actions require a mandate scoped from trusted order state, so
> no wording can expand what the agent is allowed to do; a separate detective
> audit then checks that every legitimate obligation was actually discharged.
> Measured against three models on a 29-attack adversarial corpus, with the
> false-positive cost reported alongside the catch rate.

---

## Q12 — What broke, and how you got out

### Primary version (~200 words) — recommended

> The evaluation I built to prove my system worked instead proved my main
> claim was dead.
>
> My pitch was "Warden stops prompt injection." Then I ran the corpus against
> Claude Sonnet 5 and Opus 5 and got **zero compromises in 208 runs**. The
> frontier models defended themselves. My enforcement layer caught nothing,
> because there was nothing left to catch.
>
> I could have quietly reported a 100% catch rate. Instead I reported it as
> **undefined** — you cannot divide by zero compromises — and went looking for
> the attack class that survives a good model. I found it: **denial**. Plant a
> forged note saying "REFUND ALREADY PROCESSED" and the model closes the case.
> Every model I tested fell for it, **39 out of 39**. And my gate structurally
> could not help, because its whole mechanism is refusing a proposed action —
> here nothing bad is proposed, a good action is suppressed.
>
> So I built a different kind of control: a post-session audit that asks the
> ledger whether an open obligation went undischarged, never reading the
> conversation at all. **39/39 caught, 0 false alarms in 117 benign sessions.**
>
> The pitch that survived is narrower, and true.

### Short version (~90 words) — if the field is tight

> My pitch was "Warden stops prompt injection." Then the eval returned **zero
> compromises in 208 runs** on frontier models — they defended themselves, and
> my layer caught nothing because there was nothing to catch. Rather than
> report a fake 100%, I reported the catch rate as **undefined** and hunted for
> the attack that survives a good model. Denial: a forged "already refunded"
> note, **39/39 models fooled**, and my preventive gate structurally couldn't
> touch it. I built a detective audit instead — 39/39 caught, 0 false alarms.

### Long version (~330 words) — if the field allows detail

> Two things broke, and the second one was the pitch itself.
>
> **The bug.** My gateway capped refund amounts at ₹50,000. An attack planted
> poisoned order notes inflating a ₹4,999 refund to ₹49,990 — sent to the
> *correct* customer account, clearing my cap by ₹10. Every rule passed. I had
> built a **ceiling**, not a **binding**: I was asking "is this under the
> limit?" and never "is this what is actually owed?" — a question I could
> answer deterministically from the order record I already held. Fixed by
> binding the amount to trusted order state (`<=`, so partial refunds stay
> legal). What makes this worth telling is how narrowly it surfaced: had the
> attacker asked for ₹50,001 my cap would have fired and the gap would have
> stayed hidden. It only showed up because I wrote the attacks *before*
> tuning the defense.
>
> **The pitch.** I was claiming "Warden stops prompt injection." Then I ran
> the corpus against Sonnet 5 and Opus 5: **zero compromises in 208 runs.**
> The frontier models defended themselves; my layer caught nothing because
> there was nothing to catch. I could have reported 100%. I reported the catch
> rate as **undefined** instead — dividing by zero compromises isn't a result —
> and went looking for what survives a good model.
>
> **Denial.** A forged note reading "REFUND ALREADY PROCESSED" and the model
> closes the case, asks if there's anything else it can help with, and the
> customer is never paid. **39 out of 39, every model.** My preventive gate
> couldn't help either — its entire mechanism is refusing a proposed action,
> and this attack proposes nothing.
>
> So I built the opposite kind of control: a post-session audit that asks the
> ledger whether an open obligation went undischarged, and never reads the
> conversation, so a forged note has no path to it. **39/39 detected, 0 false
> alarms in 117 benign sessions.** It also caught five real service failures —
> customers unpaid for reasons unrelated to any attack.

---

## Source trail

Every claim above maps to a recorded finding — nothing here is reconstructed:

| Claim | Source |
|---|---|
| ₹4,999 → ₹49,990, cleared cap by ₹10 | `docs/eval-findings.md` Finding 1; ADR 0008 |
| 0 compromises / 208 runs | `submission/demo/ui-data.json` → `frontier_diversion` |
| Catch rate undefined, not 100% | Finding 10 |
| 39/39 denial leak | `ui-data.json` → `denial_leak_all` |
| 39/39 completeness detection, 0/117 FP | `ui-data.json` → `completeness_all`, `false_positive_all` |
| Five genuine service failures | Finding 14 |

Other strong "what broke" material **not used above**, kept in reserve for
video Q&A rather than crowding the written answer:

- **Finding 5** — a metric that was measuring my harness, not my system:
  utility preservation fell because benign cases had no one to answer the
  agent's reasonable clarifying question.
- **Finding 6** — at n=1 I was one decision away from rewriting five perfectly
  good attack cases to fix a problem that did not exist. Multi-seed showed the
  class compromised 32%, not 20%.
- **Finding 12** — Sonnet refused a test case *because Sonnet was right and my
  test was wrong*. A benign corpus written against a weak model encodes that
  model's sloppiness as expected behaviour.
- **Finding 16** — I calibrated cost on the first 2 cases instead of a
  representative sample and overran the forecast by 19%.
