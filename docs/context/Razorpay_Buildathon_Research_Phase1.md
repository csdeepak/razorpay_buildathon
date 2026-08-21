# Razorpay Buildathon — Research Phase 1 (Deep-Dive + Strategic Thesis)
Compiled 2026-08-20. Read the "TIME-CRITICAL" section first — everything else can wait a day, this can't.

---

## 0. TIME-CRITICAL — READ THIS FIRST

According to a third-party X post (not yet confirmed against the primary page's full content — see Unknowns), the Razorpay AI Buildathon has:

> **Applications close: 5 September 2026.**

Today is **August 20, 2026**. That is **16 days**, not "some point this cycle." Your context file's Step 1–8 sequence (deep research → problem selection → architecture → pre-build → *then* founder email) is the right sequence in principle, but it was written assuming you had runway. You may not. If this date is real, your pre-build window is closer to two weeks than the "quarter of engineering time" the original plan implicitly assumed. I'm flagging this bluntly because the single biggest risk to your plan right now isn't "wrong project" — it's "right project, missed deadline because you were still doing Step 3 of an 8-step research plan on day 12."

**Action before anything else in this document: open https://razorpay.com/buildathon/ yourself, on a normal browser (not a fetch tool — see why in Unknowns), and screenshot the actual application form, deadline, and track list.** I could not fully render that page (client-side JS; see §J). Everything below is reconstructed from secondary sources and needs your eyes on the primary page before you commit to a track.

---

## 1. What I found, and how confident I am in each piece

Confidence key: **VERIFIED** (primary source, dated) / **LIKELY** (consistent secondary sourcing) / **UNCONFIRMED** (single secondary source, could be wrong or stale).

### The Buildathon itself

- **VERIFIED** (razorpay.com/buildathon/ metadata): Tagline is *"Razorpay AI Buildathon — Build. Show. Get hired."* Framed as *"a student-only program to discover and hire Razorpay's next AI Builder Interns"*, with *"No resume screening — build something worth talking about."*
- **UNCONFIRMED** (single X post by a third party, @ajay_2512x): ₹75,000/month, 6 or 12 month duration, Bangalore in-person, students only, applications close 5 September 2026, first track listed is **"AI Growth & Agentic Commerce."** The post was truncated in search results — I only have the first track name, not the full list. [X post](https://x.com/ajay_2512x/status/2090393869473165453)
- **Do not confuse this with a different event**: there is also *"India's first OpenCode Buildathon by GrowthX"* at Razorpay HQ — a separate 8-hour, 100-participant hackathon with a ₹100K prize pool, run by GrowthX (an external community), with tracks in consumer apps / revenue-generating products / multi-agent systems. This is co-located at Razorpay and easy to conflate with the hiring-track Buildathon, but it looks like a different program with a different organizer. [TipRanks coverage](https://www.tipranks.com/news/private-companies/razorpay-hosts-ai-buildathon-to-deepen-ties-with-developer-ecosystem), [Razorpay on X](https://x.com/Razorpay/status/2045468704750927994)
- **LIKELY**: The role you're building toward is the same shape as Razorpay's standing **"AI Builder"** req on Greenhouse — chief-of-staff-style, "decompose business problems from first principles," "discovery to demo in under two weeks," full-stack + multi-agent + RAG, Claude Code/Cursor as primary tools. [Job posting](https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited/jobs/4713785005). This is a strong signal for what "AI Builder" means at Razorpay day-to-day: not a research role, an ambiguity-to-shipped-system role. That matches your desired positioning almost exactly — which is either great validation or a sign you've been pattern-matching your pitch to the job description. Hold both possibilities.
- I found **no official page content** on judging criteria, submission format, demo requirements, or pre-built-work rules. Every source that claims to summarize the buildathon page is working from SEO metadata, not the actual body copy. **This is a real gap, not a nitpick** — you cannot finalize a pre-build strategy without knowing the pre-built-work rule.

### Razorpay's 2026 AI/agentic direction (this part is well-sourced)

- **VERIFIED**, Razorpay Sprint 2026 (razorpay.com/sprint/26): SVP Engineering Prabu Ram frames 2026 as *"The Age of Agentic Payments."* 100+ product launches. Four pillars: (1) agentic stack — conversational/voice commerce, autonomous agents for disputes, cash forecasting, RTO prevention, subscription recovery; (2) international payments — localized checkout, AML, chargeback protection; (3) D2C/omnichannel — self-healing POS, accessibility; (4) RazorpayX — agents autonomously handling receivables, payouts, bookkeeping, payroll approval.
- **VERIFIED**, launched 12 March 2026: **Agent Studio**, built on Anthropic's Claude Agent SDK. Ships 8 pre-built agents: Dispute Responder, Subscription Recovery, Abandoned Cart Conversion (via SuperU / Nugget-Zomato), Cashflow Forecaster, RTO Shield, RTO Insights, Settlement Insights. No-Code Agent Builder in beta. A **third-party developer ecosystem for publishing agents is explicitly planned but not live** — this is a white-space signal, not a green light; see §4. [Blog](https://razorpay.com/blog/agent-studio-ai-agents-by-razorpay/)
- **VERIFIED**, launched 12 March 2026: **Agentic Platform / RazorSense** — reframes the merchant dashboard from instruction-based to intent-driven, AI-native onboarding (PAN/CKYC), auto-detected tech stack integration, autonomous reconciliation. [Blog](https://razorpay.com/blog/razorpay-agentic-platform/)
- **VERIFIED**, launched **18 August 2026** — two days before this research, i.e. current news, not background: **Vulcan**, described as "India's first transformer-based AI foundation model for payments." Trained on 4B payments / 3T data points, covers routing, fraud detection, risk, personalization (~3,000 signals/transaction). Claimed: 8–10% payment success rate improvement, 8x international card fraud detection, 5x fraud/dispute identification improvement, 40% more UPI-preference matching via Magic Checkout. Note the honest caveat from the source: **no published methodology, baselines, or sample period** — these are Razorpay's own beta numbers, not audited. [Medianama](https://www.medianama.com/2026/08/223-razorpay-vulcan-ai-foundation-model-payments/)
- Medianama also raises a real open question worth knowing about: whether Vulcan's training data includes personally identifiable consumer information, and how Razorpay — a data *processor* for merchants, not the data owner — justifies training a proprietary model on that data under India's DPDP Act. **If you build anything involving transaction-level data modeling, expect this exact question in the room.** It's a live compliance fault line at the company you're trying to join, and if you show you're aware of it, that's a serious signal of maturity — most 21-year-olds building hackathon fintech demos have never thought about it.
- **LIKELY**: Razorpay has been actively recruiting senior AI leadership — an ex-CTO/co-founder of Divyam.ai, and directors poached from Microsoft, Salesforce, and CRED — explicitly to build "autonomous, agent-driven financial systems." CTO quote: *"the next decade of financial infrastructure will be built very differently from the last."* [Source](https://digitalterminal.in/tech-companies/razorpay-bolsters-ai-strategy-with-senior-engineering-leaders-from-microsoft-salesforce-and-cred)
- **VERIFIED** (secondhand quote, paywalled primary): Harshil Mathur (co-founder) on agentic commerce: the core problem being solved is *secure payment execution when AI agents are involved* — "a new framework where the agent never sees" the sensitive payment data. This is the clearest single articulation of Razorpay's philosophical stance on agent-initiated payments: **isolate the agent from the credential, not "trust the agent."** [Substack summary](https://rizing.substack.com/p/how-razorpay-is-thinking-about-agentic) — I'd get behind the paywall on this one before finalizing anything about agent-payment security, it's likely the single most relevant primary artifact.

### Competition intelligence

I could not find dated write-ups of *previous* Razorpay Buildathon winners — this looks like a newer program without a public retrospective yet, which cuts both ways: no track record to study, but also no established "winning formula" that's already been copied by 200 other applicants.

Cross-referencing a 2026 MCP/AI-agents hackathon (Solo.io) and general AI hackathon pattern analysis, here's what actually separated winners, stripped of hackathon-blog fluff:

1. **Narrow, operational pain, not a platform.** The Solo.io winner (Frugalia) didn't build "an AI ops platform" — it autonomously found and fixed one specific class of Kubernetes cost waste. The clinical-data winner didn't build "AI for healthcare" — it solved secure federated access to one specific dataset (MIMIC-IV) through MCP. **Judges reward a scalpel, not a Swiss Army knife.** Your context file's own "Important Don'ts" already says this (don't build a generic chatbot) — this evidence just confirms it's the actual differentiator, not just good advice.
2. **Governance/compliance-flavored agent projects did unusually well** in the MCP hackathon — two separate winners were about *constraining* what an agent can do (protocol-level auth enforcement, automated security-posture governance), not about what a new agent can do. Given Razorpay's own philosophical stance above ("the agent never sees the credential"), a project that demonstrates disciplined agent permissioning in a payments context is directly on-thesis, not just generically well-received.
3. **Deployable > theoretical.** Every winner shipped something that ran against real infrastructure or real data, not a slide deck of an architecture. Given your 60–80%-pre-built strategy, this argues for spending pre-build time on a working system with real (or realistic-mocked) data, not a beautiful pitch deck.
4. **Judges weight demo communication heavily**, but only as a multiplier on a real system — it doesn't rescue a shallow one.

---

## 2. Strategic thesis (A + B combined)

Razorpay's 2026 bet, stated in its own words across four independent product launches in six months (Agent Studio in March, the Agentic Platform in March, Vulcan on Aug 18, plus the standing Sprint 2026 roadmap) is: **move from "software you instruct" to "an agent layer that acts autonomously inside financial workflows, with the payment credential itself kept out of the agent's hands."**

The company is not chasing "AI features." It's building: a foundation model trained on its own proprietary payments data (Vulcan), an execution layer for autonomous financial agents (Agent Studio), and a philosophical stance on agent-payment security (Mathur's "the agent never sees"). That's a coherent three-layer stack — model, execution, trust boundary — and it's the correct lens for evaluating any project idea: **which layer does your project sit in, and does it respect the trust boundary they've already publicly committed to?**

A project that just wraps an LLM around Razorpay's existing APIs to "let an agent pay for things" is on-trend but shallow — you'd be building the thing they already shipped (Agent Studio's pre-built agents cover disputes, subscriptions, cart recovery, cashflow, RTO, settlements). **You cannot win by re-building one of their eight existing agents with a nicer UI.** That's the first idea most applicants will have, and it's dead on arrival.

The actual white space is upstream or downstream of what they've shipped, not parallel to it.

---

## 3. Evidence-backed problem spaces (C) and white space (D)

Ranked by how directly they trace to something Razorpay has *said or shipped*, not by how interesting they sound:

1. **Third-party agent governance/marketplace tooling.** Agent Studio explicitly plans an open ecosystem for third-party agents but hasn't shipped it. Nobody has built the trust/audit/permissioning layer for *that* yet — because it doesn't exist yet. This is genuine white space, directly stated by Razorpay, unclaimed.
2. **Agent permissioning and spending-limit infrastructure for the "agent never sees the credential" model.** Mathur has articulated the philosophy; I found no evidence they've published the actual mechanism (scoped tokens? intent-based mandates? something like emerging agentic-commerce protocols?). A working prototype of *how* that boundary could be implemented and audited is directly on-thesis and technically hard enough to be credible.
3. **Consumer-side / merchant-side visibility into agent-driven spend.** Your context file already flagged this as a research question ("merchant visibility into AI-driven purchases") — I found nothing suggesting Razorpay has shipped this. As agentic commerce grows, someone needs to give a merchant or a CFO a real-time answer to "how much did AI agents just spend on my behalf, and was any of it wrong."
4. **DPDP/compliance-aware data handling for agent-facing financial models** — directly responsive to the exact gap Medianama called out in Vulcan's launch. A small, well-reasoned prototype or even a rigorous position paper on "how would you architect consent/data-scoping for a payments foundation model under DPDP" is unusually credible coming from a CS student, because almost no one at your level thinks about this.
5. **Reconciliation/failure-recovery agents for smaller merchants** who can't afford Agent Studio's enterprise-flavored rollout — a scaled-down, SMB-focused agent for RazorpayX-style bookkeeping/payouts. Lower novelty, but real pain, well evidenced by the Agentic Platform blog's own pain-point list (multi-day onboarding, five-hour integration, manual reconciliation).

**White space specifically**: #1 and #2 are the strongest — they sit exactly at the boundary Razorpay has publicly declared as unsolved. Everything downstream of "agent takes an action" is now visibly staffed (8 shipped agents, a foundation model, senior hires). Nobody has shown their hand on "how do you let a third party's agent operate here safely." That's your opening.

---

## 4. Your advantage / your weakness (F + G) — unfiltered

**Advantage**: ASMOS is not a toy. Verification-gated routing, trust scores with online reputation updates, an audit trail, and a reported 22% context-token cost reduction with a 95% CI across 10 seeds is *exactly* the vocabulary of "agent permissioning and auditability" that problem space #2 above needs. You are not pitching a hackathon idea cold — you already have a working trust/routing/audit substrate for multi-agent systems. That is a genuine, defensible edge over almost every other student applicant, most of whom will have a LangChain wrapper and a demo video.

**Weakness, and I mean this**: your resume's own scoring table (which you wrote, so you already know this) rates "Product/business signal" at 5.5/10 and "Razorpay-specific positioning" at 5/10. That's not a rounding error — that's the actual gap between you and someone who gets picked. ASMOS proves you can build rigorous systems. It does not, by itself, prove you can find a problem nobody told you to solve and argue why it matters to a business. The "no resume screening — build something worth talking about" framing of this Buildathon is a direct test of exactly that weaker half of your profile. If you show up with ASMOS-grade engineering wrapped around a problem statement that reads like "here's a cool agent trust demo," you will lose to someone with worse engineering and a sharper, more specific business case. **The technical depth is not in question. The discipline to pick one narrow, evidenced, business-relevant problem and stop there — not add ASMOS features because you can — is the actual risk to this plan.**

---

## 5. Unknowns that block a final decision (J)

These are not nice-to-haves — you cannot lock the project without resolving them:

1. **The real deadline and full track list.** I have one secondhand deadline (5 Sept) and one track name ("AI Growth & Agentic Commerce") from a single non-official X post. Get the primary page's actual content — open it in a real browser, not a scraper, because it's client-rendered and every automated fetch I ran (including this one) only got SEO metadata back.
2. **Pre-built-work rules.** Your entire strategy in §4 of your context file depends on being allowed to arrive with 60–80% built. Nothing I found confirms or denies this for this specific Buildathon. This is the single most important unknown for your pre-build plan and I could not verify it.
3. **Whether the GrowthX/OpenCode 8-hour hackathon and the hiring-track Buildathon are actually the same funnel or genuinely separate programs.** I believe they're separate based on organizer (GrowthX vs. Razorpay directly) and format (8-hour on-site vs. an application-based track system), but I could not fully confirm this and got them tangled in search results repeatedly — you should too, before you plan around one or the other.
4. **Whether "AI Growth & Agentic Commerce" is the track most aligned with white-space opportunity #1/#2 above, or whether there's a separate "developer platform" / "trust & risk" track that's a better fit** — I only have one track name, not the full list.
5. **Whether Vulcan's DPDP/consent gap (§1) is something Razorpay would welcome a student surfacing, or something that reads as presumptuous from an intern candidate.** Worth a gut-check with someone who knows the culture — possibly your founder contact — before you build a whole pitch around "your compliance posture has a hole in it."

---

## 6. Recommended next steps, in order

1. **Today**: open the actual buildathon page yourself and resolve unknowns #1–#4 above. Do not proceed to architecture until you have the real deadline and track list in front of you — if it really is 5 September, your timeline just got a lot shorter than the original 8-step plan assumed.
2. Deep-dive problem spaces #1 and #2 (agent governance / permissioned agent-payment execution) specifically against ASMOS's existing trust/routing/audit mechanics — figure out how much of ASMOS's substrate genuinely transfers versus how much you'd be relabeling.
3. Only after that: architecture and pre-build plan, sized to whatever real runway the deadline gives you.
4. Founder email stays parked until the project thesis is locked — that part of your original plan is still correct and I'm not overriding it.
