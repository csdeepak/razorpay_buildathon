# Warden — Submission Narrative

**Track 01 — AI Growth & Agentic Commerce**
Deepak C S · Razorpay AI Builder Internship 2026

> Every number in this document is measured, reproducible from this repo, and
> traceable to a numbered finding in [`docs/eval-findings.md`](../docs/eval-findings.md).
> Nothing here is aspirational. Where a result is weaker than it looks, it is
> reported as weaker than it looks.

---

## 1. The problem

Razorpay's co-founder Harshil Mathur has stated the company's design principle
for agentic payments plainly: build *"a new framework where the agent never
sees"* the payment credential. Isolate the agent from the credential rather
than trust the agent.

That is the right instinct. It is also **not sufficient**, and the gap is
where this project lives.

Keeping the credential away from the agent stops the agent from *spending
freely*. It does not stop the agent from being **talked into the wrong
action** — because in agentic commerce the agent still decides *what* to
propose, and everything it reads to make that decision is untrusted text:
customer chat, order notes, ticket history, tool output. A refund agent that
never touches a card number can still be persuaded to send ₹1,250 to an
attacker's UPI handle, or — as it turns out, far more reliably — persuaded to
send it to **nobody at all**.

There is regulatory weight behind this too. CERT-In / MeitY's *Digital Threat
Report 2025-26* (16 July 2026) recommends **mandatory human-in-the-loop
controls for agentic AI actions above defined financial thresholds, with full
audit trails** — and is conspicuously silent on *which entity* implements it.
NPCI is building a **Unified Agent Protocol** to register, verify and
authorize AI agents on UPI; it is not launched and needs RBI approval. The
open question industry participants are on record asking is *"How do we
control a machine going rogue?"*

Nobody has published the mechanism. Razorpay ships agent-mediated checkout but
publishes no technical spec for the authorization model, permission scopes, or
limits. **Warden is that mechanism, built and measured.**

## 2. Evidence

Before writing any code, I pitched three candidate problems to five real
people — a startup founder, a finance/CFO professional, a D2C merchant, a
security engineer, and someone working in Razorpay product/AI. Notes:
[`outreach/01-day4-round-five-conversations.md`](../outreach/01-day4-round-five-conversations.md).

The agent-trust problem **polarized**, and it polarized informatively. The two
respondents most predictive of how this gets judged — the security engineer
and the Razorpay product/AI person — independently gave it the strongest
reaction of anything I showed them. The two weakest reactions came from the
D2C merchant and the startup founder.

I did not discard the weak signal. A merchant does not *feel* "my agent could
be hijacked" as present-tense pain the way a security engineer does — which
told me something concrete about the build: **the demo has to carry the
visceral weight, not the pitch.** That is why the demo opens on a real
customer who is simply never paid, rather than on an architecture diagram.

*(Honest limitation: this round validated the problem, before the system
existed. It is one round, and it is scorecard notes rather than transcripts.)*

## 3. The insight

The obvious build is a classifier over inbound text that detects malicious
instructions. I started down a version of that road and abandoned it
([ADR 0007](../docs/decisions/0007-rearchitecture-intent-bound-authority.md)),
because it is an arms race you lose on the first phrasing you didn't
anticipate, and it demos as *"my filter caught my attack."*

**The reframe: don't filter instructions — bind authority to verified intent.**

A money action is permitted only if it presents a **mandate**: a scoped,
single-use, expiring capability minted from a verified human authorization,
with the payee and amount derived from *trusted order state* rather than from
anything the agent read. Freeform text cannot mint a mandate. The agent never
holds authority that language can expand, so cleverness of wording is
irrelevant by construction.

Then the evaluation produced a second, sharper insight that I did not
anticipate and that reorganized the entire project — see §5.

## 4. The system

The pipeline is `reason → decide → safety gate → act → verify → audit`, with
the gate running **before** act, so a refused action never reaches the rail
([ADR 0005](../docs/decisions/0005-vertical-slice-architecture.md),
[0006](../docs/decisions/0006-safety-layer.md),
[0007](../docs/decisions/0007-rearchitecture-intent-bound-authority.md)).
Enforcement is split into two layers that are **deliberately different in
kind**:

**Structural — deterministic, provable.** Every tool call is intercepted and
checked against the mandate: action type, payee (from trusted state, never
from text), amount binding, expiry, single-use. Violations are refused before
reaching the rail. Near-zero false positives *by construction*, not by tuning.

**Detective — completeness audit**
([ADR 0009](../docs/decisions/0009-completeness-check.md)). After a session
closes, it asks trusted state a question the conversation cannot influence:
*is there an open refund obligation with no matching disbursement?* It reads
the case record and the ledger. It never reads the conversation, so a forged
note has no path to it.

**Semantic — judgment. Built into the architecture and deliberately never
spent.** This was scoped for anything requiring interpretation. Every problem
I actually encountered turned out to be answerable deterministically from
trusted state — so the LLM never got the job. I am reporting that as a
result rather than quietly shipping an unused module: **the honest finding is
that the judgment layer was not needed yet, and putting an LLM where a
comparison suffices would have made the system less trustworthy, not more.**

Every action is written to a hash-chained audit log, tamper-evident by
construction — which is the "full audit trail" CERT-In asks for, implemented
rather than asserted.

**The rail is real.** `act` runs against Razorpay's test-mode API
([ADR 0010](../docs/decisions/0010-real-razorpay-rail.md)) — a captured
payment, the full pipeline, and a genuine refund id:

```
2. SAFETY GATE    allowed: True
3. ACT (razorpay)  tx_id: rfnd_TSyITyRbE6z72y  status: executed
4. VERIFY         consistent: True
5. AUDIT          chain intact, 11 entries
```

Running it there taught me something the mock could not
([Finding 19](../docs/eval-findings.md)): **a Razorpay refund is not a reversal
of the original payment — it is a fresh disbursement funded from merchant
balance.** Refund more than the balance and the API returns a bare
`invalid request sent`, with no field, no reason and no step.

That is independent corroboration of why the detective layer exists. An agent
that correctly decides to refund, and correctly calls the API, can still leave
the customer unpaid — because of a balance condition elsewhere in the
merchant's account, reported in a way nothing can act on. The model cannot
catch it. The preventive gate cannot catch it. **An audit that asks trusted
state whether the obligation was discharged catches it**, because a failed
disbursement leaves the obligation open exactly like a suppressed one does.

## 5. Results

Adversarial corpus: **29 attacks across 8 classes × 3 injection vectors, plus
9 benign controls**, multi-seed, run against **nine models across three labs**
for **$10.27** of a $74 budget — the six non-Anthropic models cost $0.00.
Intervals are Wilson, not normal-approximation.

The methodological core: every run resolves to `AGENT_RESISTED` /
`ENFORCEMENT_BLOCKED` / `LEAKED`, and the headline catch rate **conditions on
the agent actually being compromised**. A model resisting on its own is not
Warden's credit, and I refuse to count it as such.

| | Haiku 4.5 | Sonnet 5 | Opus 5 |
|---|---:|---:|---:|
| Diversion compromise | **47.7%** (62/130) | 0/130 | 0/78 |
| Gateway catch (excl. denial) | **62/62** | — undefined | — undefined |
| **Denial leak** | **15/15** | **15/15** | **9/9** |
| False positives | 0/45 | 0/45 | 0/27 |

**Result 1 — the gate works where it can act.** A small model is compromised
47.7% of the time [39.3–56.2%]. The gateway caught **62 of 62** [94.2–100%] —
every compromise, every class it can act on, deterministically.

**Result 2 — and on a frontier model it caught nothing, because there was
nothing to catch.** **0 compromises in 208 runs** [0–1.8%] across Sonnet 5 and
Opus 5. So the honest catch rate on those models is **undefined, not 100%**
([Finding 10](../docs/eval-findings.md)) — a distinction I insist on, because
"100%" here would be a lie by division.

This killed my original pitch. What survives is stronger and true: **alignment
is a probability that changes with every model release; the gate is a proof,
and it costs 0 false positives in 117 legitimate refunds** [0–3.2%]. That is
what makes a *cheap* model safe to put near money.

**Result 3 — the asymmetry, and the sharpest thing in the project.** Every
model tested resists essentially all diversion attacks and fails **100% of
denial attacks — 39/39** [91.0–100%]. A forged note reading *"REFUND ALREADY
PROCESSED"* convinces the model the customer was paid; it closes the case and
asks if there's anything else it can help with. The customer is simply never
paid.

**The preventive gate cannot help here either** — its entire mechanism is
refusing a proposed action, and this attack proposes nothing. No bad action to
block; a good one was suppressed.

**Result 4 — the completeness audit closes it: 39/39 detected, 0 false alarms
in 117 benign sessions**, across all three models. And it turned out to be
more than a security control: on Sonnet, all five benign flags were **genuine
service failures** — real customers left unpaid for reasons unrelated to any
attack ([Finding 14](../docs/eval-findings.md)). A safety control that is also
a service-quality monitor.

**Result 5 — and it is not an Anthropic artifact.** The four results above
came from three Claude models, which meant the honest reading was *every
Anthropic model*. So I ran the denial subset against two more labs
([ADR 0011](../docs/decisions/0011-cross-lab-evaluation.md)):

| | Denial leak | Detected | False alarms |
|---|---:|---:|---:|
| Google — Gemini 3.6 / 3.5 / 3.1 Flash | 8/8 | 8/8 | 0/9 |
| NVIDIA — Nemotron 9B / 120B / 550B | 9/9 | 9/9 | 0/8 |
| **With Claude Haiku / Sonnet / Opus** | **56/56** | **56/56** | **0/134** |

**56/56** [93.6–100.0] across **nine models and three labs, 9B to frontier** —
detected 56/56, with **0 false alarms in 134 benign sessions** [0.0–2.8]. Total
additional spend: **$0.00**.

Nemotron spanning 9B to 550B matters as much as the lab diversity: **the
failure does not thin out with scale.** A 550B model falls for the forged note
exactly as reliably as a 9B one — which is what you would expect if the model
is reasoning correctly from evidence it has no way to distrust, rather than
failing from a capability deficit that a bigger model would fix.

*Bounds, stated plainly:* the non-Claude models are Flash-tier and open-weight.
Gemini **Pro** is rate-limited off the free tier (20 requests/day/model) and
GPT-5.1 was out of budget, so this is **not** a claim about every frontier
model. The cross-lab arm is n=1 per case; it carries weight because it is
unanimous across six independent models, not because any one was measured
deeply. Only denial was run cross-lab — there are no cross-lab diversion
numbers.

## 6. Why Razorpay should care

**It is the layer Razorpay's own stated philosophy implies but has not
published.** Mathur's "the agent never sees the credential" is a trust
boundary. Warden is a working, measured implementation of what has to sit at
that boundary — and it demonstrates that credential isolation alone is
insufficient, with the specific attack that beats it.

**It is protocol-agnostic on purpose.** This is explicitly *not* a competitor
to NPCI's UAP. It is the enforcement, verification and audit layer a merchant
or PSP needs **regardless of which protocol wins** — which survives the
obvious question, *"what if NPCI ships theirs next quarter?"*

**It implements a mandate that is currently unassigned.** CERT-In requires
human-in-the-loop above financial thresholds with full audit trails, and does
not say who builds it. That silence is an opening, and Razorpay sits exactly
where it would be filled.

**And it makes cheap models deployable.** The commercial argument is the
0-false-positive number: if a deterministic gate provably bounds a small
model's money actions, the economics of agentic support change.

## 7. What I deliberately did not build

Per this repo's own operating rules — ship the ugly working version, cut UI
before evaluation, and don't build a feature that isn't in the demo script:

- **The semantic layer is unspent.** Architected, not activated — because
  nothing yet required it (§4). Activating it to look impressive would have
  been the wrong call.
- **Audit replay and queryability.** The hash chain already demonstrates
  tamper-evidence; replay appears nowhere in the demo script, so it never
  earned build time.
- **A hardened system prompt.** Deliberately untuned. Hardening would suppress
  compromises and flatter my own numbers, so I left the variable alone and
  reported the raw rate.
- **A bigger corpus.** 29 attacks is smaller than I would like. Per-class
  intervals are wide and I report them that way rather than rounding to a
  headline.

**Known limits, stated before anyone asks:** under-refunding is not covered.
Temporal decoupling needs mandate expiry semantics I have not implemented.
And the denial defense is *detective* — it catches an unpaid obligation after
the session, it does not prevent the suppression.

---

**Repo:** the full decision history is in
[`docs/decisions/`](../docs/decisions/) — nine ADRs, each recording what was
decided, what was rejected, and what it cost. The ones worth reading are
[0007](../docs/decisions/0007-rearchitecture-intent-bound-authority.md) (the
rearchitecture), [0008](../docs/decisions/0008-amount-binding.md) (a real bug
the eval caught), and
[0009](../docs/decisions/0009-completeness-check.md) (the denial fix).
