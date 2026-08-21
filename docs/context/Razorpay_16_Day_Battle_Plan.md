# The 16-Day Battle Plan
**Target: AI Builder Intern, Razorpay. Assumed deadline: 5 Sept 2026. Today: 20 Aug 2026.**

Read §1 before you feel good about anything. Read §2 before you write a line of code.

---

## 1. Verdict on your plan

### What you got right — and I don't say this often

**Your instinct to hunt money-movement problems is correct**, and better than you realize. You wrote:

> Agent → decision → financial action → verification → audit

Two weeks before you wrote that, India's CERT-In published the *Digital Threat Report 2025-26* (16 July 2026) recommending **mandatory human-in-the-loop controls for agentic AI actions above defined financial thresholds, with full audit trails.** NPCI is simultaneously building a **Unified Agent Protocol** to register, verify and authorize AI agents on UPI — not launched, still needs RBI approval — and the open question industry participants are on record asking is *"How do we control a machine going rogue?"*

You independently converged on the architecture that India's payments body and its cyber regulator are currently trying to specify. That is not a coincidence you should be modest about. That is the pitch.

Your seven-layer decomposition is also right in kind. The judge test — *"would Razorpay adopt this?"* — is the correct north star. Percentage tracking is a good discipline for a solo builder because it makes self-deception harder. Keep all of that.

### What's trash, in descending order of how much damage it will do

**1. Synthetic user interviews. This is the worst idea in your plan and you should kill it today.**

An LLM asked to roleplay an Indian D2C merchant will agree with whatever problem you hand it. It has no ground truth about whether anyone actually loses sleep over reconciliation. You will generate transcripts that *feel* like evidence and contain zero information. Your own context file, rule §6, says **"Do not manufacture problems."** Synthetic interviews are an industrial-scale problem-manufacturing machine wearing a research-methodology costume.

And the failure mode isn't just epistemic, it's tactical: if a judge asks *"how did you validate this?"* and your answer contains the word "synthetic," you have just told a room of people who ship real products that you couldn't be bothered to talk to a human. That is a kill shot in Q&A and you will not recover from it in the ninety seconds you'll have.

The only legitimate use: rehearsing your own pitch against a hostile persona before you take it to a real person. That's a sparring partner, not a source. Never cite it, never put it in a slide.

**2. "Find 20 problems and score them on 6 criteria."**

That's 120 judgments. Two to three days. On a 16-day clock with an *unconfirmed* deadline, that isn't rigor — it's procrastination with a spreadsheet, and it's the exact failure mode of a research-brained person under time pressure.

Worse: you don't have 20 real problems. You have maybe five, and you'll invent fifteen to fill the rows. **Filling rows to hit a round number is manufacturing problems** — the thing you already told yourself not to do, arriving through the back door.

Generate what comes naturally in three hours. Score in one pass. Cut to three by end of Day 3. I've seeded the sheet with 20 candidates already so this costs you hours, not days — but the seeds are hypotheses to be killed, not a menu to order from.

**3. Seven layers in sixteen days.**

You'll build seven shallow ones. Three of them — agent reasoning, tool calling, memory — are commodity in 2026. Every competitor will have them and nobody has ever been hired for them. Your moat is in three others. Build three deep, three thin. §4 has the split.

**4. "10 real users."**

Right instinct, arbitrary number, and it dies if you start it late. Five real conversations begun on Day 3 beat ten rushed ones on Day 13. Ten is a vanity metric; what you need is the moment someone says *"actually the real problem is X"* and it reorganizes your thinking. That happens on conversation two or not at all.

**5. "A demo for each type of product launch."**

I don't know what this means, and a judge won't either. One demo. Ninety seconds. Rehearsed until it's boring to you.

### The meta-risk, which is bigger than any item above

Your plan front-loads roughly six days of analysis before a line of code exists. Your own resume self-assessment scores your product/business signal at **5.5/10** — and more analysis does not fix that. Analysis is your comfort zone. It's what a research-oriented engineer does when the real task is frightening. The cure is shipping something narrow with a real person's reaction attached, and the only currency that buys is days.

### On "half of me wants to exclude this project"

That doubt is not information about the project. It's what an unlocked problem statement feels like from the inside, and it will get *worse* with more research, not better — research feeds it. It resolves the moment you commit to one problem and start building.

And the arithmetic says commit. Downside: sixteen days and you don't get selected. Upside: the job. Either way you end up holding a shipped agentic-fintech system with evaluation numbers attached — which is precisely the ammunition your founder email currently lacks and the exact hole in your profile (Razorpay-specific positioning, 5/10). **There is no branch of this tree where you finish worse off than you started.** Stop relitigating it.

---

## 2. GATE 0 — today, ~2 hours, blocking everything

You still do not know what you are submitting. Not approximately — at all. Three worlds are live:

- **World A:** apply by 5 Sept *with a project/portfolio*. → The 16-day build below is right.
- **World B:** 5 Sept is registration only; building happens later. → Days 1–5 below are still pure profit; the build phase stretches.
- **World C:** on-site timed sprint, pre-built work banned. → **The entire build plan is wrong.** 16 days becomes preparation — reusable libraries, rehearsed architecture, domain fluency — not a submission.

Every hour you build before resolving this is an hour wagered on a coin flip.

Go to https://razorpay.com/buildathon/ in your browser (I can't — it's client-rendered JS and my fetch tools only ever see the SEO metadata; the Chrome extension isn't connected to this session either). Answer these six, in writing:

1. Real application deadline and timezone.
2. Full track list — I only have one name secondhand, *"AI Growth & Agentic Commerce."*
3. Submission format: repo? demo video? deck? live presentation? All?
4. **Pre-built-work rule.** The single most important line on that page for you.
5. Do participants get Razorpay API sandbox / Agent Studio / Vulcan access, or do you mock everything? (Assume mock until proven otherwise — Vulcan's only public entry point is an enterprise Typeform.)
6. Team or solo?

Paste the page text back to me and I'll rebuild this plan around the real constraints in one pass.

---

## 3. The roadmap

Assumes World A and ~7 focused hours/day. **If you have classes, cut scope — never sleep.** A tired builder on Day 14 makes decisions that cost more than the hours saved.

### Phase 1 — Landscape + problem hunt · Days 1–3 (Aug 20–22) · target 15%

| Day | Work | Output |
|---|---|---|
| 1 (Thu 20) | Gate 0. Then start the landscape map — it's seeded, you're verifying and extending, not starting blank. | Six confirmed facts + landscape sheet ~50% |
| 2 (Fri 21) | Finish landscape. Work the problem bank: kill seeds that collide with Agent Studio's existing 8 agents, add your own. Score in one pass. | 20 rows scored |
| 3 (Sat 22) | Cut to 3. Write a one-page thesis per survivor. Send outreach messages for 5 conversations. | 3 one-pagers, 5 messages sent |

**Gate 1 (end Day 3):** three problems, each with a written one-pager. *If you can't write the one-pager, you don't understand the problem — that's the test, and it's pass/fail.*

### Phase 2 — Validate + lock · Days 4–5 (Aug 23–24) · target 25%

| Day | Work |
|---|---|
| 4 (Sun 23) | 3–5 real conversations. Merchants, founders, finance ops, anyone who moves money for a living. PES alumni, your club network, LinkedIn cold DMs, your Razorpay founder contact's orbit. Ask what breaks, not whether they like your idea. |
| 5 (Mon 24) | **LOCK ONE PROBLEM.** Write the product thesis + architecture. Then write the demo script — *before any code.* |

**Gate 2 (end Day 5): hard commitment.** After this you do not shop for ideas again. Reopening the problem after Day 5 is the single most common way solo builders lose these things, and it always feels justified at the time.

Writing the demo script before the code is not a formality. If you cannot script ninety compelling seconds, the project is wrong — and Day 5 is a cheap day to learn that. Day 14 is not.

### Phase 3 — Build the spine · Days 6–10 (Aug 25–29) · target 60%

| Day | Work |
|---|---|
| 6–7 | **Vertical slice.** One complete path, end to end: reason → decide → act (mocked) → verify → audit. Ugly is fine. It must *run*. |
| 8 | Safety layer: permissions, scopes, limits, velocity. The "agent never sees the credential" boundary, implemented. |
| 9 | Verification layer. Go deep. This is your moat. |
| 10 | Audit layer: every consequential action recorded, replayable, queryable. |

**Gate 3 (end Day 10):** the loop runs end to end on one real scenario. **If it doesn't run by Day 10, cut scope — do not extend the phase.** A smaller system that works beats a larger one that doesn't, and on Day 10 that trade is still cheap.

### Phase 4 — Evidence · Days 11–13 (Aug 30–Sep 1) · target 85%

| Day | Work |
|---|---|
| 11 | Evaluation harness + adversarial cases. What happens under prompt injection? When a limit is breached? When a tool fails mid-transaction? When two agents cascade? |
| 12 | Run it. Get numbers. Multi-seed where it applies — you already know how, ASMOS is the proof. |
| 13 | UI / demo surface. **Only now.** |

**This phase is where you win.** Everyone demos the happy path. Almost nobody stands up and says *"here's what happens when it goes wrong, here's the guardrail catching it, and here's the number across 200 adversarial cases."* You have done exactly this kind of statistical evaluation before — 95% CI, 10 seeds, held-out validation. Almost no student competitor can. **Do not let this phase get compressed. If something has to give on Day 12, cut UI polish, never the evaluation.**

**Gate 4 (end Day 13):** you have numbers. Not vibes.

### Phase 5 — Narrative + ship · Days 14–16 (Sep 2–4) · target 100%

| Day | Work |
|---|---|
| 14 | Record the demo. Many takes. 90 seconds. |
| 15 | Write the submission: problem → evidence → insight → system → results → why Razorpay should care → what's next. README a stranger can run. |
| 16 (Fri Sep 4) | Buffer. Everything submittable by end of day. |

**Your deadline is 4 September, not the 5th.** Builders who target the real deadline miss it. Submit on the morning of the 5th at the latest — never at 11pm, when a broken upload has no recovery path.

---

## 4. Architecture — your seven layers, re-weighted

Your list was right. The *depth allocation* is what decides whether you're memorable.

| Layer | Depth | Why |
|---|---|---|
| Agent (reason/plan) | **Thin** | Commodity. Every competitor has it. Zero differentiation. |
| Tool (actions) | **Thin** | Mock Razorpay's APIs faithfully. Real sandbox only if Gate 0 says you get one. |
| **Safety** (permissions/limits) | **DEEP** | Directly answers CERT-In's threshold mandate and Mathur's *"the agent never sees"* stance. |
| **Verification** (don't trust the model) | **DEEP** | Your ASMOS moat — verification-gated routing and trust scoring already exist in your work. |
| Memory | **Thin** | Needed for state. Not a differentiator in this problem. |
| **Audit** (every action recorded) | **DEEP** | CERT-In literally requires *"full audit trails."* Regulatory tailwind, free credibility. |
| **Evaluation** | **DEEP** | Rarest signal in the room. Almost nobody your age ships statistical evaluation of an agent system. |

The four DEEP layers are one coherent story: **an agent can act on money, and you can prove what it was allowed to do, what it actually did, and that the guardrails hold under attack.** Four thin layers, four deep ones, one sentence. That's a system, not a feature list.

---

## 5. The white space — so Phase 1 doesn't start blank

Primary-sourced and dated. Every one of these is verifiable; none are manufactured.

1. **NPCI's Unified Agent Protocol** — registration, verification and authorization for AI agents on UPI. Under development with industry consultation, **not launched**, needs RBI approval. Open question on record: *"How do we control a machine going rogue?"*
2. **CERT-In / MeitY, Digital Threat Report 2025-26 (16 July 2026)** — recommends mandatory human-in-the-loop above defined financial thresholds, **with full audit trails.** Notably silent on *which* entity implements it. That silence is an opening.
3. **The global authorization gap** (Central Bank Payments News, June 2026): no cryptographic proof of what the human principal authorized; **temporal decoupling** — permission granted hours or days before the agent acts; attack surface unique to agents (prompt injection, intent drift, agent hijacking, cascading multi-agent failure). Mastercard is building Agentic Tokens + Verifiable Intent globally. **India has no equivalent public spec.**
4. **Razorpay ships "UPI Reserve Pay"** for agentic payments and publishes **no** technical specification of the authorization model, permission scopes, or limits. Documented silence, not documented solution.
5. **Agent Studio's third-party agent ecosystem is announced, not shipped.** No trust, permissioning, or audit layer exists for third-party agents on Razorpay's rails — because the ecosystem itself doesn't exist yet.

### The honest counter-argument, because I'd be doing you a disservice otherwise

This space is **abstract, and abstract demos die.** "Agent authorization infrastructure" degrades very easily into a screenshot of a permissions config screen: technically deep, emotionally dead, forgotten in ten minutes. Passing the "would Razorpay adopt this" test on substance is not the same as being remembered.

Two rules if you go here:

- **The demo must show the system catching something.** Agent gets prompt-injected → tries to pay an attacker → your layer blocks it → here's the audit record → here's the catch rate across N adversarial cases. That has a heartbeat. A policy editor does not.
- **Do not build "NPCI's UAP, but mine."** Competing with a national protocol reads as arrogant and demos terribly. Build the enforcement, verification and audit layer a *merchant or platform* needs regardless of which protocol wins. Protocol-agnostic, immediately useful, and it survives the judge asking *"what if NPCI ships theirs next quarter?"* — a question you should assume you'll get.

---

## 6. Rules of engagement

Pin these where you'll see them at 2am on Day 11.

1. **No new problem after Day 5.** Non-negotiable.
2. **No feature that doesn't appear in the demo script.** If it isn't on screen for 90 seconds, it isn't earning its build time.
3. **Ship the ugly version first, always.** Working and ugly on Day 7 beats elegant and half-built on Day 12.
4. **Cut UI before cutting evaluation.** Your numbers are the moat. Polish isn't.
5. **Never cite a synthetic user.** Ever.
6. **Write the number down when you fail a gate.** You wanted percentage tracking — its value is that it makes a slipping schedule visible before it's fatal.
7. **When you want to add an ASMOS feature "because you can" — don't.** That impulse is your specific failure mode. Scope creep dressed as technical ambition.
8. **The founder email stays parked** until the project thesis is locked. Still correct, still holding.

---

## 7. What winning looks like on 4 September

A judge who has watched forty demos should be able to repeat your thing back in one sentence, unprompted, an hour later.

Not *"an AI agent for payments"* — that's forty out of forty. Something closer to:

> *"The one that showed an agent getting hijacked mid-transaction and the guardrail catching it, with the catch rate on screen."*

You get that sentence by being narrow, by having numbers, and by showing a failure caught rather than a success staged. All three are inside your existing skill set. None of them require another week of research.

---

**Next action: Gate 0.** Six answers. Then we rebuild this against reality and pick the problem.
