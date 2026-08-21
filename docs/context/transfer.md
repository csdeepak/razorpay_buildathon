# Transfer File — Razorpay AI Builder Campaign
Generated 2026-08-20 to continue this work in a new account/session. Upload this file and say: *"Read this completely and continue from it — don't re-litigate decisions already made, don't re-run research already done. Pick up at the 'Immediate next action' section."*

---

## 0. Who this is and what "done" looks like

Deepak — B.Tech CS, PES University RR Campus, expected 2027. Target: get into Razorpay as an **AI Builder Intern**, via two reinforcing tracks:

1. **Founder's Office** — a Razorpay founder gave direct email access and asked to see his built projects. Highest priority because of direct access. **The founder email is deliberately parked** until the Buildathon project thesis is locked — do not write it early.
2. **Official Razorpay AI Buildathon** (razorpay.com/buildathon/) — tagline *"Build. Show. Get hired."* Student-only, no resume screening, hires directly into AI Builder Intern roles.

Desired positioning: **"AI systems builder who can solve ambiguous product/business problems"** — not "student with AI projects," not "hackathon participant," not "prompt engineer."

The two tracks reinforce each other: a strong Buildathon showing becomes the proof-of-work the founder email references.

---

## 1. Deepak's technical profile (context the new session needs)

**Strong areas:** Python, AI/ML, Agentic AI, multi-agent systems, LLM memory, AI engineering, PyTorch, computer vision, deep learning, transformers, explainable AI, RAG, FastAPI, Next.js, full-stack, CI/CD, statistical evaluation.

**Experience:** Agentic AI Researcher & Engineer Intern, Center of Cloud Computing and Big Data (Jun–Jul 2026) — multi-agent LLM workflows, memory-management logic, routing subtasks, agent ownership evaluation, handoff behavior.

**Main projects, in order of relevance to this campaign:**

- **ASMOS (Adaptive Semantic Memory OS for Multi-Agent LLMs)** — the single most important project for this campaign. Shared semantic-memory substrate, **verification-gated owner routing**, top-k fallback, **trust scores with online reputation updates**, **audit components**, Docker, statistical validation. Reported: 22.09% context-token cost reduction, 95% CI [17.93%, 26.27%], 10 seeds, route@1 = 1.000 in held-out validation. This is his strongest evidence of rigorous AI-systems research and the closest thing he has to a head start on the white-space opportunity identified below (agent trust/permissioning/audit).
- **Deepak.ai / Dex** — personal portfolio site (deepak-ai-web.vercel.app) with a grounded AI assistant, prompt guardrails, 34-case regression coverage, CI. Concept: "turning curiosity into working systems." Not the Buildathon project — this is the founder-email portfolio piece.
- **Docksmith** — container-runtime/systems engineering project. Shows depth beyond AI abstractions.
- Dental OPG disease detection, Turb-DETR, ShortcutScore — technically strong but not fintech-relevant; not first choice to show Razorpay.

**Deepak's own resume self-assessment (he wrote this, treat it as accurate, not modesty):**
AI/ML depth 9/10, research ability 9/10, software engineering 7.5/10, Founder's Office potential 8/10, **product/business signal 5.5/10**, **Razorpay-specific positioning 5/10**, overall 8/10.

**Core diagnosis, agreed in this session:** technical depth is not the risk. The risk is (a) picking a vague/abstract problem instead of a narrow evidenced one, (b) scope-creeping in more ASMOS-style features "because he can," and (c) spending the runway on analysis instead of shipping — his comfort zone (research) is not where his gap is (product judgment).

---

## 2. What's VERIFIED about Razorpay (primary-sourced, dated — do not re-research these)

- **Vulcan** — "India's first transformer-based AI foundation model for payments," built with **NVIDIA** (GPU compute) and **AWS** (cloud infra + SageMaker). Launched **18 August 2026**. Trained on ~4 billion payments / ~3 trillion data points, ~3,000 signals/transaction. Covers routing, fraud detection, risk, personalization. Claimed: 8–10% payment success rate lift, 8x international card fraud detection, 5x fraud/dispute identification, 40% more UPI-preference matching via Magic Checkout. **No published methodology or baselines** for these claims (Medianama). **Open DPDP/consent question**: unclear if training data includes PII, and Razorpay is a data *processor* for merchants, not the data owner — no disclosed legal basis or merchant opt-out. Access is enterprise-only (Typeform signup) — **no public API for students to build on top of it.**
- **Agent Studio** — launched 12 March 2026, built on Anthropic's Claude Agent SDK. Ships **8 pre-built agents**: Dispute Responder, Subscription Recovery, Abandoned Cart Conversion, Cashflow Forecaster, RTO Shield, RTO Insights, Settlement Insights, plus a No-Code Agent Builder (beta). **A third-party developer ecosystem for publishing agents is explicitly announced but NOT YET SHIPPED.** Do not build any of the 8 existing agents — instant auto-kill in scoring.
- **Agentic Platform / RazorSense** (12 March 2026) — reframes the merchant dashboard from instruction-based to intent-driven; AI-native onboarding, autonomous reconciliation.
- **Razorpay Sprint 2026** — "The Age of Agentic Payments," 100+ launches, four pillars: agentic stack (conversational/voice commerce, autonomous dispute/cashflow/RTO/subscription agents), international payments, D2C/omnichannel, RazorpayX autonomous finance (payables, payouts, bookkeeping, payroll).
- **Co-founder Harshil Mathur's stated philosophy on agentic payments:** the core design principle is that **"the agent never sees" the payment credential** — isolate the agent from the credential rather than trust the agent. Razorpay ships "UPI Reserve Pay" for agent-mediated checkout but **publishes no technical spec** for the authorization model, permission scopes, or limits. This silence is a real gap, not a solved problem.
- **AI leadership hires** (2026): ex-CTO/co-founder of Divyam.ai, plus directors poached from Microsoft, Salesforce, CRED — explicitly to build "autonomous, agent-driven financial systems." CTO quote: "the next decade of financial infrastructure will be built very differently from the last."
- **The AI Builder job itself** (standing Greenhouse req) reads as chief-of-staff-style: "decompose business problems from first principles," full-stack + multi-agent + RAG, "discovery to demo in under two weeks," Claude Code/Cursor as primary tools. This is almost certainly the shape of role the Buildathon hires into.

### The regulatory white space (this is the strongest strategic finding — don't lose it)

- **CERT-In / MeitY, Digital Threat Report 2025-26 (16 July 2026)**: recommends **mandatory human-in-the-loop controls for agentic AI actions above defined financial thresholds, with full audit trails.** Silent on which entity (PSP? agent developer?) must implement it.
- **NPCI Unified Agent Protocol (UAP)**: registration/verification/authorization of AI agents on UPI, delegated payments with spend caps built on UPI Circle. **Not launched, needs RBI approval.** Industry's own on-record open question: *"How do we control a machine going rogue?"*
- **Central Bank Payments News (26 June 2026)**: named, unsolved problems — no cryptographic proof of what a human principal actually authorized; **temporal decoupling** (permission granted hours/days before the agent acts, allowing context drift); agent-specific attacks (prompt injection, intent drift under adversarial composition, agent hijacking/privilege escalation, cascading multi-agent failures). Mastercard is building **Agentic Tokens** (scoped, time-bound) and a **Verifiable Intent** framework globally, contributing to FIDO/EMVCo/IETF/W3C. **No Indian equivalent public spec exists.**

**Deepak's own instinct — "agent → decision → financial action → verification → audit" — independently converged on exactly what India's regulator and payments body are currently trying to specify.** This is the pitch: build the enforcement/verification/audit layer a merchant or PSP will need regardless of which protocol eventually wins. **Protocol-agnostic** — do not build a competing protocol to NPCI's, that reads as arrogant and demos badly.

---

## 3. What's STILL UNCONFIRMED — Gate 0, blocks everything, resolve first

The only real facts we have about the Buildathon's actual mechanics come from **one third-party X post** (@ajay_2512x), never verified against the primary page: **₹75,000/month, 6 or 12 month duration, Bangalore in-person, students only, applications close 5 September 2026, one known track "AI Growth & Agentic Commerce."**

razorpay.com/buildathon/ is a client-rendered Next.js page. Every automated fetch (WebFetch, and a Chrome browser-automation attempt where the extension wasn't connected) only returned SEO metadata — title and description — never the body copy. **This has not been resolved as of this transfer.**

Six questions to answer by opening the page directly in a real browser, before building anything:

1. Real application deadline and timezone.
2. Full track list (only "AI Growth & Agentic Commerce" is confirmed).
3. Submission format — repo? demo video? deck? live presentation?
4. **Pre-built-work rule** — the single most important unresolved line. The entire 16-day pre-build plan assumes this is allowed.
5. Do participants get any Razorpay API sandbox / Agent Studio / Vulcan access, or is everything mocked? (Assume mocked until proven otherwise.)
6. Team or solo?

Three possible worlds depending on the answers:
- **World A** — apply by 5 Sept with a project attached → the 16-day build plan (below) is correct as-is.
- **World B** — 5 Sept is registration only, building happens in a later phase → research/validation days are still pure profit, build phase shifts later.
- **World C** — on-site timed sprint, pre-built work banned → the entire build plan is wrong; 16 days becomes rehearsal/domain-fluency prep, not a submission.

**Do not let a new session re-do this research. Just get the answers and proceed.**

---

## 4. The problem-scoring outcome (already done — don't redo it)

A full spreadsheet exists: `Razorpay_Landscape_and_Problem_Scoring.xlsx` (in the PAY folder), with 4 sheets — Razorpay Landscape (23 product areas mapped to users/money-flow/pain/gap), Problem Bank (20 candidates scored on strategic alignment, demoability, buildability, technical depth, profile fit, novelty — weighted, novelty weighted lowest on purpose), 16-Day Tracker, Sources.

**Top 3 scored candidates**, all money-moving, all agent-governance-flavored, none colliding with Agent Studio's shipped agents:

1. **Prompt-injection defence for payment-taking agents** (score 8.92) — an agent is hijacked mid-task and tries to move money to an attacker; your layer catches it. Best demo in the bank: a visible attack, visibly caught, with a catch-rate number.
2. **Policy enforcement gateway between third-party agents and payment rails** (8.54) — scopes, spend caps, velocity limits, category/time bounds. Directly fills the layer NPCI's protocol will require at the merchant/PSP edge.
3. **Verifiable-intent layer** — cryptographic proof of what the human actually authorized, surviving the hours/days gap before the agent acts (8.28). Deepest problem, but abstract — only viable paired with a demo that shows a violation being caught, not a policy screen.

**Auto-killed** (Agent Studio already ships these — do not rebuild): cashflow forecasting, RTO/COD prediction, chargeback evidence automation.

**Explicitly rejected as a validation method: synthetic/AI-roleplayed user interviews.** An LLM playing a merchant agrees with whatever it's handed — no ground truth, manufactures problems, and saying "I interviewed synthetic users" to a judge is a credibility kill shot. Personas may only be used to rehearse a pitch before taking it to a real human — never cited, never in a deliverable.

---

## 5. The 16-day battle plan (already written — `Razorpay_16_Day_Battle_Plan.md` in the PAY folder)

Assumes World A (see §3) and the unconfirmed 5 Sept deadline. Today when this was written: **20 Aug 2026**.

- **Days 1–3 (landscape + problem hunt)** → cut to 3 candidate problems, one-pagers written.
- **Days 4–5 (validate + lock)** → 3–5 real conversations (not synthetic), then **hard lock on one problem by end of Day 5** — no reopening after this. Write the demo script *before* any code.
- **Days 6–10 (build the spine)** → vertical slice running end-to-end (reason → decide → act(mocked) → verify → audit) by Day 7; safety layer Day 8; verification layer Day 9 (the moat); audit layer Day 10.
- **Days 11–13 (evidence)** → adversarial evaluation harness, run it, get real numbers (multi-seed, same rigor as ASMOS). **This phase is where the campaign wins or loses — if scope must be cut later, cut UI, never evaluation.**
- **Days 14–16 (ship)** → record a 90-second demo, write the submission narrative, buffer day. **Real internal deadline is 4 Sept, not 5th — never submit at the literal deadline.**

**Layer-depth allocation (already decided, don't re-litigate):** Agent reasoning / tool calling / memory = THIN (2026 commodity, zero differentiation). Safety, Verification, Audit, Evaluation = DEEP (this is the coherent story: an agent can act on money, and you can prove what it was allowed to do, what it did, and that guardrails hold under attack).

**Standing rules of engagement:**
1. No new problem after the Day 5 lock.
2. No feature that isn't in the demo script.
3. Ship the ugly working version before the elegant half-built one.
4. Cut UI before cutting evaluation.
5. Never cite a synthetic user as evidence.
6. Track percentage completion daily against the plan; a slipping gate means cut scope, not extend the phase.
7. When the urge is to add an ASMOS feature "because you can" — don't. That specific impulse is the identified failure mode.
8. Founder email stays parked until the project thesis is locked.

---

## 6. Files already produced this session (check the PAY folder before regenerating anything)

All saved to `C:\Users\csdee\PESU\PAY\` on Deepak's device:
- `Razorpay_Buildathon_Research_Phase1.md` — first research pass (strategic thesis, problem spaces, competition intelligence, unknowns)
- `Razorpay_16_Day_Battle_Plan.md` — the critique + roadmap described in §5
- `Razorpay_Landscape_and_Problem_Scoring.xlsx` — the scored spreadsheet described in §4

If the new session has access to this same device/folder, read these directly instead of re-deriving them. If not, this transfer file's summaries above are sufficient to continue without re-reading.

---

## 7. Immediate next action for the new session

**Do not re-research anything above. Do not re-open the problem selection. Do not suggest synthetic user interviews.**

1. Ask Deepak whether Gate 0 (§3) has been resolved yet — has he opened razorpay.com/buildathon/ himself and gotten answers to the six questions?
   - If **not resolved**: that is the only blocking task. Help him extract the answers (he may paste page text, a screenshot, or describe what he saw), then confirm which of World A/B/C applies and adjust the day-by-day plan in §5 accordingly.
   - If **resolved**: update the plan with the real deadline/tracks/rules, recompute how many days remain, and move straight to wherever Deepak is in the Day 1–16 sequence (ask him what he's completed).
2. Once Gate 0 is resolved and the plan is time-adjusted, the next substantive task is the **Day 4–5 work**: real conversations to validate the top-3 problems (§4), then the hard lock.
3. Keep the ruthless-mentor register: challenge weak reasoning, name the specific failure mode when scope creeps, don't soften critique. Deepak has explicitly asked for this and has responded well to it so far.
