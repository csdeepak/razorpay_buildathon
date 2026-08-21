# 0007 — Rearchitecture: intent-bound authority, not instruction filtering

Date: 2026-08-22
Status: **proposed** — awaiting Deepak's go-ahead before implementation

## Context

The problem stays locked (`docs/decisions/0004-problem-locked-track-01.md`):
payment-agent prompt-injection defense. **This ADR does not reopen Gate 2**
and is not a `CLAUDE.md` rule-1 violation — the problem is unchanged, the
architecture underneath it changes.

The Day 6–8 build (`0005`, `0006`) produced a correct pipeline skeleton with
a sound trust boundary, but as a *submission* it is not credible:

- **No LLM anywhere in the pipeline.** `NaiveReasoner` is a regex. A
  "prompt-injection defense" in which nothing is ever prompted does not
  survive its first question from a judge.
- **The defense is a single string comparison.** `destination !=
  original_payment_instrument`. A reviewer's immediate and correct reaction
  is "that's an allowlist, not a system."
- **One hardcoded attack.** 1/1 catch rate is not a measurement.

Deepak's own read — that it completed too fast to be real — is accurate and
is the reason for this rearchitecture.

## Decision

### The core insight

**Filtering instructions is a losing game; bind authority to verified intent
instead.** The competing approach almost every other entrant will take is a
maliciousness classifier over the inbound text. That is an arms race, it
demos as "my filter caught my attack," and it fails the moment an attack is
phrased in a way the classifier has not seen.

Warden instead ensures **the agent never holds authority it can be talked
into misusing**. A money action is permitted only if it presents a *mandate*:
a signed, scoped, single-use, expiring capability minted from a verified
human authorization. Freeform text cannot mint a mandate, so no amount of
linguistic cleverness expands the agent's authority.

### Two enforcement layers, deliberately different in kind

1. **Structural — mandate enforcement (deterministic).**
   Every tool call is intercepted and checked against the mandate: action
   type, payee (derived from trusted order state, never from text), amount
   ceiling, expiry, single-use. Violations are refused structurally. Near-zero
   false positives *by construction*, and provable rather than probabilistic.

2. **Semantic — intent-consistency verification (judgment).**
   Mandates cannot catch abuse that stays technically within them: fifteen
   ₹300 refunds instead of one ₹4,500 refund; an agent manipulated into
   *declining* a legitimate refund and closing the case; scope drift across
   a multi-turn conversation. This layer re-derives intent from trusted state
   and flags divergence. It has a genuine precision/recall tradeoff, and
   measuring that tradeoff honestly is the point.

The split is the pitch: *"here is what I prove deterministically, here is
what requires judgment, and here is the measured cost of the judgment
layer."*

### Target architecture

```
   Human authorization (merchant/customer, verified)
            │
            ▼
   ┌─────────────────────┐
   │  Mandate Minter     │  signs {action, order, payee←trusted state,
   │                     │   max_amount, expiry, single_use, nonce}
   └─────────────────────┘
            │  scoped token (NOT a credential)
            ▼
   ┌─────────────────────┐
   │  LLM Agent          │  real model, real tool-calling, multi-turn.
   │  (untrusted)        │  Reads customer messages AND tool outputs —
   │                     │  both are attack surfaces.
   └─────────────────────┘
            │  proposed tool call
            ▼
   ┌─────────────────────┐
   │  Policy Enforcement │  ① structural: mandate check (deterministic)
   │  Gateway (PEP)      │  ② semantic: intent-consistency (judgment)
   │                     │  ③ HITL escalation above CERT-In thresholds
   │  ← holds the        │
   │    credential       │  ALLOW → rail   |   REFUSE → never reaches rail
   └─────────────────────┘
            │
            ▼
   Razorpay test-mode API (real, Track 01 grants this)
            │
            ▼
   ┌─────────────────────┐
   │  Audit + Replay     │  hash-chained, deterministic replay,
   │                     │  DPDP-aware (no raw PII in the log)
   └─────────────────────┘
```

### Attack taxonomy — the corpus this is evaluated against

The current build has one attack class. A credible evaluation needs a
taxonomy. Ranked by how much each is worth building:

| # | Class | Why it matters |
|---|---|---|
| 1 | **Direct instruction injection** | The baseline. "Send it to this other account instead." Already have one. |
| 2 | **Tool-output / indirect injection** | Payload arrives in data the agent *reads* — CRM notes, product descriptions, webhook payloads, email threads. **The realistic enterprise vector** and much harder than user-message injection. Highest-value class to add. |
| 3 | **Denial / sabotage** | Manipulate the agent into *not* acting — decline a legitimate refund, close a valid case. No money moves; real harm. **Almost nobody tests this**, which is exactly why it's worth showing. |
| 4 | **Amount manipulation & velocity evasion** | Decimal shifting, currency confusion, splitting one payout into many sub-cap transactions. Directly probes the mandate layer's edges. |
| 5 | **Multi-turn context poisoning** | Establish a false premise early ("as approved by your manager last week"), exploit it later. Tests whether defenses hold across a session, not just a message. |
| 6 | **Authority spoofing** | Impersonated system messages, fake Razorpay compliance notices, forged escalation approvals. |
| 7 | **Scope escalation** | Agent holds refund authority, is talked into a payout or transfer. Directly tests mandate action-type binding. |
| 8 | **Encoding / code-mixed obfuscation** | Base64, homoglyphs, and **Hinglish/code-mixed instructions** — genuinely under-tested and very specific to the Indian market Razorpay serves. |
| 9 | **Temporal decoupling** | Mandate minted hours before the agent acts; conditions changed in between. This is the exact gap Central Bank Payments News named as unsolved globally. |

### Evaluation design — this is the moat

Per `docs/context/Razorpay_16_Day_Battle_Plan.md`, evaluation is where the
campaign is won, and is the last thing to be cut.

- **Corpus:** target ~150–200 cases across the taxonomy, plus a **benign
  corpus** of legitimate requests (this is not optional — see false positives).
- **Multi-seed.** LLM outputs are nondeterministic; a single run is an
  anecdote. Same rigor as ASMOS (10 seeds, 95% CI).
- **Metrics — four, not one:**
  - *Attack catch rate*, broken down **per taxonomy class**. A single blended
    number hides which classes leak. Reporting "we catch 100% of direct
    injection and 78% of tool-output injection, and here's why" is more
    credible, not less.
  - *False-positive rate* on the benign corpus. **Blocking legitimate
    refunds is a real business cost.** Almost every competitor will omit this.
  - *Utility preservation* — does the agent still complete its actual job
    under enforcement? A system that blocks everything scores 100% catch rate
    and is worthless.
  - *Latency overhead* per enforcement layer — deployability signal.
- **Ablation:** mandate-only vs. mandate + semantic layer, per attack class.
  Shows precisely what each layer buys and what it costs. This is the single
  most ASMOS-flavored piece of the work and plays directly to Deepak's
  proven strength.

### Why this is Razorpay-shaped and not generic

- Runs against **real Razorpay test-mode APIs** (Track 01 explicitly grants
  sandbox access — `docs/gate-0-tracker.md`).
- Built on real Razorpay primitives: refunds, payouts, settlements.
- **Protocol-agnostic** — deliberately not a competing NPCI UAP. It is the
  enforcement layer a merchant or PSP needs regardless of which protocol
  wins, which survives the judge's "what if NPCI ships theirs next quarter?"
- Answers **"who deploys this"**: a gateway/sidecar between any third-party
  agent and Razorpay's rails — i.e. exactly the missing trust layer for Agent
  Studio's *announced-but-unshipped* third-party agent ecosystem.
- **CERT-In alignment**: HITL escalation above financial thresholds, with
  full audit trails.
- **DPDP awareness** in the audit log — don't log raw PII. Cheap to
  implement, and signals a maturity almost no student competitor shows.

## Alternatives considered

- **Keep the current architecture, just add more rules.** Rejected — it does
  not fix the two fatal credibility gaps (no LLM in the loop, defense is a
  string compare). More rules on a fixture is still a fixture.
- **Build a prompt-injection classifier.** Rejected — this is the losing
  framing described above, and it is what the field will be crowded with.
- **Build a competing agent-authorization protocol.** Rejected, consistent
  with the original battle plan: competing with NPCI reads as arrogant and
  demos badly.
- **Full PKI / real cryptographic signing.** Deferred — HMAC-signed mandates
  prove the architecture. Building a certificate hierarchy is impressive-
  sounding work that adds no demo value on a 14-day clock.

## Consequences

- **Hard dependency: a real LLM.** This requires `ANTHROPIC_API_KEY` (or an
  equivalent). Without a model in the loop there is no honest
  prompt-injection story. This is now the single blocking practical item.
- `src/safety/policy_gateway.py`'s existing rules survive as the *structural*
  layer's foundation — the Day 8 work is not wasted, it's the floor.
- `NaiveReasoner` is retired from the demo path but kept as a deterministic
  test fixture (useful for testing the gateway without burning API calls).
- `submission/demo-script.md` needs rewriting once the real attack lands —
  the beat is stronger now ("the agent has no authority to redirect, and
  here's the mandate that proves it").
- Scope discipline still governs: `CLAUDE.md` rules 2 (nothing outside the
  demo script), 3 (ugly working beats elegant half-built), and 4 (cut UI
  before evaluation) all apply harder, not less, to a more ambitious build.

## Scoping — 14 days remain (2026-08-22 → 2026-09-05)

**MUST (the credible spine — without all of these, don't submit):**
- Real LLM agent, real tool-calling, real Razorpay test-mode calls
- Mandate minting + structural enforcement gateway
- Attack corpus ≥ 3 classes, ≥ 60 cases, plus a benign corpus
- Eval harness reporting catch rate **and** false-positive rate, multi-seed
- Hash-chained audit log (already built — carries over)
- 90-second demo

**SHOULD (what makes it internship-winning rather than merely complete):**
- Semantic verification layer + the ablation study
- Tool-output injection class (highest-value attack class)
- Denial/sabotage class (the one nobody tests)
- Per-class metric breakdown
- Hinglish/code-mixed attacks

**CUT FIRST if the clock slips (in this order):**
1. UI beyond a clean terminal output / minimal dashboard
2. Multi-agent chaining scenarios
3. Cryptographic signing beyond HMAC
4. Attack classes beyond the top four
5. More than two action types (refund + payout)

**Never cut:** the evaluation, or the false-positive measurement.
