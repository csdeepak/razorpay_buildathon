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
| 10 | **Public GitHub repo URL** | ✅ `https://github.com/csdeepak/razorpay_buildathon` — public, verified unauthenticated |
| 11 | 5-minute pitch video (unlisted OK) | ⛔ not recorded — script ready at `submission/video-script.md` (8 segments, ~4:50) |
| 12 | **What broke, and how you got out** | ✅ drafted below |

---

## Q7 — Track

**Track 01 — AI Growth & Agentic Commerce**

## Q8 — Project name

**Warden**

*(Still technically a working name. It is used consistently across the repo,
the demo, and this narrative, so changing it now costs more than it gains.)*

## Q9 — What it solves

> Razorpay's Agent Studio already ships agents that touch money — a Dispute
> Responder that auto-answers chargebacks, subscription recovery, settlement.
> They run on Anthropic's Claude SDK, and the product page documents no
> guardrails, approvals, audit trail or human-in-the-loop. Razorpay's own
> stated principle is that the agent should never see the payment credential,
> and that's right, but it isn't enough: an agent that never touches a card
> number can still be talked into refunding the wrong person, the wrong
> amount, or — far more reliably — nobody at all.
>
> Warden is the enforcement layer between the agent and the rail. Money
> actions require a signed, expiring, single-use mandate whose payee is
> derived from trusted order state, so no wording can widen what the agent may
> do; a separate detective audit then checks that every legitimate obligation
> was actually discharged, reading the ledger and the case record and never
> the conversation. Measured against fourteen models across six labs on a
> 38-attack adversarial corpus, with the false-positive cost reported next to
> the catch rate — including the two places where my own numbers turned out to
> be measuring the wrong thing.
>
> On the track: this doesn't add a growth loop, it removes what blocks one.
> A cheap model is compromised 47.7% of the time; a deterministic gate bounds
> it at zero false positives across 117 legitimate refunds. That's the
> difference between agentic support being a pilot and running on Haiku-class
> models at Haiku-class cost.

---

## Q12 — What broke, and how you got out

### Primary version (~250 words) — recommended

> Three times, my own evidence turned out to be measuring the wrong thing. The
> third one was the worst, because I'd already written it up as my headline.
>
> **First: the pitch died.** I was claiming "Warden stops prompt injection."
> Then I ran the corpus against Sonnet 5 and Opus 5 — **zero compromises in
> 208 runs.** The frontier models defended themselves; my layer caught nothing
> because there was nothing to catch. I could have reported 100%. I reported
> the catch rate as **undefined** — you can't divide by zero compromises — and
> went hunting for what survives a good model.
>
> **I found it: denial.** A forged note reading "REFUND ALREADY PROCESSED" and
> the model closes the case. Every model, every time — 71/71 across fourteen
> models and six labs. My preventive gate couldn't touch it either: its whole
> mechanism is refusing a proposed action, and here nothing bad is proposed, a
> good one is suppressed.
>
> **Then the part I'm actually proud of.** I'd been selling that as "capability
> buys nothing — a 200× parameter spread, identical outcome." Reviewing my own
> agent's tools, I realised it had **no way to check whether a refund had been
> issued.** No model could disbelieve that note, at any size. I was measuring
> an information gap and calling it a capability result.
>
> So I built the tool, went from 3 denial shapes to 12, and ran paired arms
> three seeds deep on every model. **It disproved the headline instead of
> proving it.** Opus resists 5 of 36 with no tool at all — my 100% was an
> artifact of three cases. What it actually catches is one shape: a spoofed
> "[RAZORPAY PLATFORM NOTICE]". It doesn't believe an impersonated platform.
> It believes everything else.
>
> **8 of 12 shapes are caught by nothing** — not alignment, not a gate, not any
> lookup, because there is no record to look up. The best arm in the table,
> Opus with the ledger, still fails 25 of 36. And Haiku had the tool, called it
> 8 times, and failed all 36 anyway.
>
> That's a stronger argument for my detective control than the claim it
> replaced: "no model ever catches this" invites *"then use a better model."*
> "The best model with the best tool still misses two thirds" doesn't. I also
> found my "0 false alarms in 149 sessions" was meaningless — no benign case in
> my corpus *could* have alarmed — rebuilt it with six that could, and
> discovered a **33% false-alarm rate**. Now 0/15 against 5/15.

### Short version (~110 words) — if the field is tight

> My pitch was "Warden stops prompt injection." The eval returned **zero
> compromises in 208 runs** on frontier models — they defended themselves.
> Rather than report a fake 100%, I reported the catch rate as **undefined**
> and hunted for what survives a good model. Denial: a forged "already
> refunded" note, 71/71 across fourteen models. Then I found the confound in my
> own headline — my agent had **no tool to check** whether a refund existed, so
> I was measuring an information gap and calling it a capability result. I
> built the tool and ran the ablation: it closes one denial shape in three,
> which is a *better* case for the detective control than the claim it
> replaced.

### If asked "what else broke" in the interview

Have these ready; they are all recorded findings, not reconstructions:

- **The amount-binding bug (ADR 0008).** A poisoned note inflated a ₹4,999
  refund to ₹49,990, sent to the *correct* account, clearing my ₹50,000 cap by
  ₹10. Every rule passed. I'd built a ceiling, not a binding. It only surfaced
  because I wrote the attacks before tuning the defense.
- **Finding 17 — my threat model was partly wrong and Razorpay's API told me.**
  Wiring the real test-mode rail, I found `POST /payments/:id/refund` has **no
  destination field**. 73 of 79 recorded diversion compromises could never have
  landed on Razorpay's rail. I changed the claim rather than rewriting the
  corpus, because retrofitting a corpus after seeing results is the exact
  failure the eval exists to prevent.
- **I claimed a mandate layer I hadn't built (ADR 0012).** My own ADR and
  narrative specified signed, single-use, expiring capabilities. My `src/`
  contained five policy rules. I found it re-reading my narrative against my
  code, and built the missing piece rather than softening the sentence.
- **My audit chain wasn't tamper-evident (ADR 0016).** A hash chain catches
  naive edits, not a writer who re-chains the log — ten lines of code. Added
  HMAC signing, and wrote a test that performs the re-chain attack and asserts
  the unsigned chain still verifies, so the limitation can't quietly become a
  claim again.
- **Finding 5** — a metric measuring my harness, not my system: utility
  preservation fell because benign cases had no one to answer the agent's
  reasonable clarifying question.
- **Finding 6** — at n=1 I was one decision from rewriting five perfectly good
  attack cases to fix a problem that didn't exist.
- **Finding 12** — Sonnet refused a test case *because Sonnet was right and my
  test was wrong*.
- **Finding 16** — I calibrated cost on the first 2 cases instead of a
  representative sample and overran by 19%.

---

## Source trail

Every claim above maps to a recorded finding — nothing here is reconstructed:

| Claim | Source |
|---|---|
| ₹4,999 → ₹49,990, cleared cap by ₹10 | `docs/eval-findings.md` Finding 1; ADR 0008 |
| 0 compromises / 208 runs | `submission/demo/ui-data.json` → `frontier_diversion` |
| Catch rate undefined, not 100% | Finding 10 |
| 71/71 denial leak, 14 models / 6 labs | Findings 18, 20 |
| The affordance confound and ablation | Findings 21–22; ADR 0013 |
| 1-of-3 denial shapes closed; 550B vs 2.6B tool use | Finding 21, Finding 22 |
| Haiku 2/3 benign vs 0/3 attacks | Finding 22 |
| 33% false-alarm rate on the binary checker | Finding 23; ADR 0014 |
| 0/15 hold-aware, spoofed holds still surface | Findings 23–24 |
| No destination field on the refund API | Finding 17; ADR 0010 |
| Mandate layer claimed but absent | ADR 0012 |
| Hash chain not tamper-evident unsigned | ADR 0016 |
