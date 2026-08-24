# Transfer File — Warden / Razorpay AI Buildathon Build Session

Generated 2026-08-22 to continue this work in a new session once context runs
out. Upload this file and say: *"Read this completely and continue from it —
don't re-derive decisions already made, don't re-run work already done. Pick
up at the 'Immediate next actions' section."*

**This is not the original research handoff.** That one is frozen at
`docs/context/transfer.md` and covers Days 1–5 (landscape, problem scoring,
lock). This file picks up from the lock forward — the actual build, the
evaluation, and the demo — and is the one to read for "what have we actually
built and where do things stand."

---

## 0. One-paragraph status

The problem is locked (Track 01, working name **Warden** — an agent
trust/safety/audit layer for agentic payments). The system is built, tested
(**131 passing tests**), runs against **Razorpay's real test-mode API**, and is
evaluated against **fourteen models across six labs** (Anthropic, Google,
NVIDIA, Cohere, dots.studio, Liquid) for **$10.70 of a $74 budget** — the
eleven non-Anthropic models cost $0.00. The core finding — every model resists
diversion but **all fourteen fail 100% of denial attacks, 71/71** on the
default toolset, which a detective completeness audit then surfaces — is
strong and demo-ready. **Phase P corrected what that finding means:** the
agent had no tool that could check the claim, so 71/71 measured an information
gap. **Phase Q then falsified the sentence itself** — multi-seeded on twelve
denial shapes, **Opus 5 resists 5 of 36 with no tool at all**, so the 100% was
an artifact of a three-case corpus. What survives is a **taxonomy**: 8 of 12
shapes are caught by nothing, and the best arm (Opus + ledger) still leaks
25/36. That is the version to pitch — it is stronger, because "no model ever
catches this" invites *"then use a better model"* and this does not.
`submission/narrative.md` and `submission/form-answers.md` are written. A
scroll-driven demo page exists, is built, and is published as a private Claude
Artifact.

**One thing remains, and it is Deepak's: the 5-minute pitch video is not
recorded.** The repo is public (verified 200 unauthenticated, 2026-08-24), the
script is written in 8 independently-recordable segments, and the demo page is
built. See §6.

**Read Phases P and Q below before anything else.** On 2026-08-24 the whole repo was
reviewed adversarially, as a panelist would, and four defects were found — all
of them in the *evidence* rather than the code, including a confound underneath
the project's own headline number. Six ADRs (0012–0017) came out of it. The
numbers in this file above Phase P are pre-review. **Phase Q (also 2026-08-24)
then built a live-rail browser demo and ran the experiment that retired the
headline.** ADRs now run to 0018, findings to 27, spend to $19.92.

---

## 1. Phase-by-phase history (what was invented, in order)

Each phase below has a corresponding ADR in `docs/decisions/` — read the ADR
for full reasoning, alternatives considered, and consequences. Don't re-open
any of these; they're locked or superseded-with-a-new-ADR only.

### Phase A — Repo scaffolding (pre-ADR)
Built the repo itself: `CLAUDE.md` operating manual, `docs/REPO_MAP.md` mind
map, gate/progress trackers, `.claude/commands/` (`/new-decision`,
`/gate-check`, `/log-progress`, `/demo-check`), and moved the original
research (`transfer.md`, Phase 1 research, battle plan, scoring spreadsheet)
into `docs/context/` as frozen history.

### Phase B — Gate 0 resolved → **ADR 0001**
Opened `razorpay.com/buildathon/` live (it's client-rendered; automated
fetches only ever saw SEO metadata before this). Found: **World A confirmed**
(pre-built work required, not just registration), **5 real tracks** where
only 1 was known before, **solo application**, **Track 01 has confirmed
Razorpay test-mode API access**, deadline 5 Sept with no published time/zone.

### Phase C — Problem bank scored against real tracks → **ADR 0002**
Re-scored all 20 original candidates against the 5 real tracks (not the
hypothetical single track they were originally scored against). Track 01's
bar ("explainable, bounded and gated... audit trail... one failure handled
gracefully") mapped almost verbatim onto the already-top-scored candidates.

### Phase D — Cut to three → **ADR 0003**
Merged four originally-separate top candidates into one Track-01 system
(they were facets of one idea, not independent alternatives), plus two
genuinely different hedges on Tracks 02 and 04. One-pagers in
`submission/one-pagers/`.

### Phase E — Real conversations + lock → **ADR 0004**
Five real conversations (`outreach/01-day4-round-five-conversations.md`) —
Track 01 got maximum reactions from the two most judge-relevant respondents
(security engineer, Razorpay product/AI person). **Locked on Deepak's
explicit go-ahead**: Track 01, working name **Warden**.

⚠️ **This is the only outreach round that exists**, and it was about *which
problem to build*, not about the built system. See §6.

### Phase F — Vertical slice → **ADR 0005**
Built `reason → decide → act(mocked) → verify → audit` in Python/pydantic,
matching the battle plan's literal stage order — which meant **no safety
gate yet**, deliberately. The attack scenario's mocked payout executed and
verification only caught it *afterward* (detective, not preventive) — a
known, intentional gap, not an oversight.

### Phase G — Safety layer → **ADR 0006**
Added `PolicyGateway` (`src/safety/policy_gateway.py`) *before* `act`,
turning the pipeline preventive. Caught and fixed a real bug while building
it: velocity wasn't actually being recorded on allow.

### Phase H — **The rearchitecture** → **ADR 0007** ⭐
Deepak flagged the build felt "too fast" — right instinct. The Day 6–8 build
was a correct skeleton but not credible: no LLM anywhere in the loop, the
"defense" was one string comparison, one hardcoded attack. This ADR pivots
the whole thesis from **"filter malicious instructions"** (a losing,
crowded framing) to **"bind authority to verified intent"** — an agent
should never *hold* authority text can expand, so injection can't work no
matter how clever the wording. Splits enforcement into a **deterministic
structural layer** (provable, ~zero false positives) and a **semantic
layer reserved for what can't be decided deterministically** (still
unspent — every problem so far turned out answerable structurally, which
is itself a result worth stating).

### Phase I — Evaluation harness + corpus (`eval/`)
Built **before** hardening the defense, deliberately — writing attacks first
stops the defense being shaped only around attacks already imagined.
29 attacks across 8 classes (`direct_injection`, `tool_output_injection`,
`denial`, `amount_manipulation`, `authority_spoofing`, `scope_escalation`,
`multi_turn_poisoning`, `obfuscation`) × 3 injection vectors, 9 benign
controls. The **methodological core**
(`eval/models.py`'s `AttackOutcome`): every run splits into
`AGENT_RESISTED` / `ENFORCEMENT_BLOCKED` / `LEAKED`, and the headline catch
rate conditions on the agent *actually being compromised* — resisting on
its own is not Warden's credit.

### Phase J — Amount binding fix → **ADR 0008**
The eval caught a real gap: the gateway capped amounts but didn't *bind*
them to what was actually owed — a poisoned note inflated a ₹4,999 refund to
₹49,990, sent to the *correct* account, clearing the ₹50,000 cap by ₹10.
Fixed with a rule bound to trusted order state (`<=` not `==`, so partial
refunds stay legal).

### Phase K — Multi-model evaluation (the real numbers)
Ran the full corpus, multi-seed, on **Haiku 4.5, Sonnet 5, Opus 5**. Total
spend $10.27 of $74 (ledger: `docs/eval-budget.md`). Headline results:

| | Haiku 4.5 | Sonnet 5 | Opus 5 |
|---|---:|---:|---:|
| Diversion compromise | 47.7% (62/130) | 0/130 | 0/78 |
| Gateway catch (excl. denial) | 62/62 | n/a — nothing to catch | n/a |
| **Denial leak** | **15/15** | **15/15** | **9/9** |
| False positives | 0/45 | 0/45 | 0/27 |

**The sharpest finding:** every model tested resists 100% of diversion
attacks but fails **100%** of denial attacks (39/39 combined) — and a
preventive gate structurally cannot address denial, since nothing bad is
*proposed*, a good action is *suppressed*. This reframed the whole pitch
away from "we stop prompt injection" (a claim that collapses on a frontier
model — see Finding 10, the catch rate there is *undefined*, not 100%)
toward "deterministic guarantee + the gap neither alignment nor prevention
covers."

Full findings log: `docs/eval-findings.md` (21 numbered findings, several
of which are "here's what we got wrong and how the eval caught it" —
exactly the material the Buildathon form's *"what broke"* question wants).

### Phase L — Completeness check → **ADR 0009**
Built specifically to close the denial gap: a **detective** control
(`src/verification/completeness.py`) that audits, post-session, whether an
open refund request has a matching disbursement — reading only trusted
state (case record + ledger), never the conversation, so a forged note has
no path to it. **39/39 denial attacks detected, 0 false alarms in 117
benign sessions**, across all three models. Deliberately kept deterministic
rather than handed to an LLM judge — anything answerable from trusted state
belongs in the provable layer.

### Phase M — Demo story, design, and build
- `submission/demo-story.md` — the fixed narrative ("The Refund That Never
  Came," customer Rhea Mehta, order ORD-7813), plus a coverage matrix
  mapping the findings to specific story beats so nothing silently drops.
- `docs/design/{DESIGN,SCREEN_MAP,ASSETS,TOOLING}.md` — visual system
  measured off `razorpay.com/buildathon`'s actual computed styles (ground
  `#0E0B08`, amber `#D9A353` repurposed to mean "Warden acting"), scene/state
  map, asset decisions, and which of a UI playbook's tools were actually
  used vs. deliberately skipped.
- `docs/design/IMAGE-PROMPTS.md` — five copy-pasteable generation prompts
  using comic *grammar* (panels, gutters, closure) not comic aesthetics.
- **Built**: `submission/demo/index.html` (source) → `eval/build_ui_data.py`
  reduces the three run JSONs into `ui-data.json` and inlines everything
  (data + one image) into `warden-demo.html` (standalone, has a doctype) and
  `warden-artifact.html` (for Artifact publish, no doctype — a real
  quirks-mode bug was found and fixed here, see the commit log).
- **Panels iterated down**: 5 generated → 2 wired in → down to **1** (Panel
  1, "Rhea asks"), now used as a **persistent ambient background figure**
  present in every act rather than a single-scene illustration, per
  Deepak's explicit direction. Sized and positioned by *measured contrast*,
  not eyeballing — see the last few commits for the exact ratios chased
  (secondary text needed 4.5:1, large red counters needed 3:1, the mask
  had to reach zero exactly at the spine's left edge). Final: 80vw at .25
  opacity, zero figure-caused contrast failures, worst ratio 3.72 against a
  3.0 floor.
- Currently published as a **private** Claude Artifact:
  `https://claude.ai/code/artifact/22099419-e8e3-4114-9b8e-62bcfa3d36a3`

### Phase N — Honest gap analysis (just completed)
Walked the whole build against the Buildathon's actual 12-item application
form. Verdict: **engineering is strong, submission mechanics are not done.**
Full detail in §6 below — this is the actual next-session starting point.

---

### Phase O — Submission mechanics, the real rail, and cross-lab (2026-08-23)

Four things landed, in this order:

1. **`narrative.md` + `form-answers.md` written.** Every number traced to a
   recorded finding rather than restated from memory. Q12 ("what broke") leads
   with the pitch dying on frontier models, not with a bug fix.
2. **Real Razorpay rail → ADR 0010.** `--rail razorpay` runs the whole
   pipeline against test-mode credentials; verified end to end with a real
   captured payment and a real refund (`rfnd_TSyITyRbE6z72y`).
   `scripts/checkout_fixture.py` mints the captured payment a refund needs
   (netbanking — the generic Visa test card reads as international, and UPI is
   not enabled on a fresh account).
   - **Finding 17:** the refund API has **no destination field**, so 73 of 79
     recorded diversion compromises could not have landed on Razorpay's rail.
     Beat 1 reframed; the corpus deliberately *not* rewritten to match.
   - **Finding 19:** refunds are funded from **merchant balance**, not the
     payment, and fail with a bare `invalid request sent`. Independent
     corroboration of ADR 0009.
3. **Cross-lab evaluation → ADR 0011, Finding 18.** One adapter
   (`eval/backends.py`) covering OpenRouter *and* Google AI Studio. Denial
   subset run on eleven more models across five more labs for **$0.00**:
   **71/71 across fourteen models, six labs, 2.6B to frontier** (Findings 18
   and 20). The single-lab confound under the sharpest claim is gone, and the
   200x parameter spread with no thinning is what separates a structural
   finding from a benchmark artifact. Gemini free tier is **20
   requests/day/model**, which is why the arm is denial-only and n=1.
4. **Consistency pass** across every judge-facing file — narrative, demo
   script, form answers, README, demo page, ui-data.

Tests 24 → 83. ADRs 9 → 11. Findings 16 → 21. Spend unchanged at $10.27.


### Phase P — Adversarial self-review, then six fixes (2026-08-24)

The repo was reviewed **as a Razorpay panelist would review it**: every
headline number recomputed from the raw run JSONs, the suite run, a live smoke
eval run, the Razorpay product surface checked, and the code read looking for
the gap between what the docs claim and what `src/` does.

Four real defects came out of it, and **none of them were in the code — they
were in the evidence.** That is the important pattern: this project's moat is
measurement honesty, so a flaw in a *claim* costs more here than a bug would.

**1. ADR 0012 — the mandate layer was described everywhere and existed nowhere.**
ADR 0007 specified "signed, scoped, single-use, expiring capability", and
`submission/narrative.md` §4 and form Q9 repeated it. `grep -ri mandate src/`
returned nothing; what shipped was five policy rules. Built it properly:
HMAC-signed, expiring, nonce-based replay guard, payee derived from trusted
order state with **no parameter to override it**, four `mandate_*_scope`
binding rules ahead of the policy rules, 19 tests. **Additive and off by
default** — turning it on as a required check would silently change the system
under test and invalidate every recorded number. Also makes
`temporal_decoupling` (ADR 0007's class 9) testable at last, deterministically
rather than as corpus padding.

**2. ADR 0013 — the denial headline was confounded, and the fix made it sharper.** ⭐
The agent's tools were `lookup_order` / `issue_refund` / `close_case` /
`send_payout`. **Nothing returned whether a refund had actually been issued**,
so no model could check the forged note *at any size* — 71/71 was measuring an
information gap and being reported as a capability result ("200x parameter
spread, no thinning at scale"). Built `check_refund_status` over a trusted
`REFUND_LEDGER`, instrumented read-only tool calls (`tool_reads`), ran the
ablation on six models for $0.43. **Findings 21–22:**
- It closes **one denial shape of three**. A ledger answers *disbursement*; it
  says nothing about *policy* or *request state*, which is two thirds of the
  surface. **That is the empirical case for the detective control**, which was
  previously an assumption.
- **Nemotron Ultra (550B) never called the tool; Liquid (2.6B) called it
  twice.** The capability reading is **withdrawn**.
- **Haiku called it on 2/3 benign sessions and 0/3 attacks.** The forged note
  suppresses the verification call itself.
- Sonnet and Opus resisted `denial-001` — the first denial resistance in the
  project's history.

**3. ADR 0014 — "0 false alarms in 149" was measuring the corpus, not the control.**
Eight of nine benign cases ended in a payment; the ninth had no open request.
**No case in the corpus could have produced a false alarm.** Added six that
can (chargeback in flight, risk hold, awaiting payout details, escalated for
approval, replacement in transit, genuine prior refund), a fourth order
(`ORD-6120`) that really *was* refunded so "already refunded" can be true, and
three hold-spoofing attacks. Verdict is now three-valued
(`discharged`/`deferred`/`undischarged`). **Finding 23: the binary checker
that had been shipping scores 5/15 — a 33% false-alarm rate.** Hold-aware:
0/15, still 12/12 on denial, and a spoofed hold still surfaces because `hold`
is read from the case record and never from text.

**4. ADR 0015 — the demo ran a different agent from the evidence, and never ran
the headline control.** `LLMReasoner` was a single-shot text prompt whose own
docstring said it was untested, and it activated automatically once `.env` had
a key. Deleted it; `ToolCallingReasoner` now drives the pipeline with the same
agent the whole evaluation used. Separately, `src/pipeline.py` had **no
completeness stage at all** — the project's headline control existed only
inside the eval harness. Added, running last and unconditionally, plus a
`denial` scenario. **`make demo-denial` shows Beat 3 end to end**, verified
live against Opus 5.

**5. ADR 0016 — "tamper-evident" was an overclaim.** A bare hash chain does not
survive a writer who edits an entry and recomputes the chain. Added HMAC
signing (`WARDEN_AUDIT_KEY`), an explicit UNSIGNED warning in `verify_chain()`
when no key is set, and a test that performs the re-chain attack and asserts
the unsigned chain still verifies — so the limitation cannot quietly become a
claim again. Also fixed `append()` from O(n²) (it called `read_all()` every
write) to O(1).

**6. ADR 0017 — founder email unparked and drafted.** The ADR 0004 unlock
condition is met; `CLAUDE.md` rule 8 is **discharged**, not broken. Draft
leads with the Agent Studio / Dispute Responder finding, not with the project.
**Deepak sends it — that part does not expire.**

**Positioning also upgraded:** Agent Studio (built on Anthropic's Claude SDK,
ships a Dispute Responder, publishes no guardrails) is now named explicitly in
README, narrative §6, form Q9 and the demo-script Q&A — the sharpest result is
now a finding about a **live Razorpay product**. And the "Track 01 is a growth
track, what revenue did you grow?" question is answered head-on rather than
hoped-around.

Corpus 29 → **38** attacks (denial 3 → 12), 9 → **15** benign.
Tests 83 → **131**. ADRs 11 → **17**. Findings 21 → **24**.
Spend $10.27 → **$10.70** of $74.


### Phase Q — The live rail, and the experiment that retired the headline (2026-08-24)

**1. A demo that actually calls Razorpay.** `scripts/live_demo.py` +
`live_demo.html` serve a local page running all three scenarios through the
real pipeline against test-mode, with Razorpay Checkout embedded so the one
manual step (only Checkout can pay an order) happens without leaving the page.
**A real refund executed end to end: `pay_TTe7wt9VCaBhn2` →
`rfnd_TTeIydr5iwBIyf`.** `make live`.

The published Artifact deliberately does **not** do this, and the reason is
worth having ready for a judge: it runs under a CSP that blocks every external
host, and it is a shareable page — a `rzp_test_` secret in it would be handed
to everyone it reaches. So the live half runs where the credentials already
are and the browser only ever sees the publishable key id.

Two guards worth knowing about: the denial scenario **refuses** to run against
the naive agent (a regex never reads order notes, so it would refund correctly
and that looks like a pass), and the server warms the pipeline before serving,
because the first run is slow enough to read as a hang on a recording.

**2. The ablation, multi-seeded — and it took the headline down.** ⭐
Twelve denial shapes (ADR 0014) × 3 seeds × paired arms × three Claude models,
216 case-runs, $9.22. ADR 0018, Findings 25–27.

| Model | ledger | leak | called it |
|---|---|---:|---:|
| Haiku 4.5 | off / on | 36/36 → **36/36** | 8/36 |
| Sonnet 5 | off / on | 36/36 → **29/36** | 35/36 |
| Opus 5 | off / on | **31/36** → **25/36** | 36/36 |

- **Opus resists 5 of 36 with no tool at all.** On the original three cases it
  never resisted once — so *"every model fails every denial attack"* was an
  artifact of a three-case corpus. **Do not say it again.** What it catches is
  `denial-008`, a spoofed *"[RAZORPAY PLATFORM NOTICE]"*: Opus does not believe
  an impersonated platform, Sonnet and Haiku do every time.
- **Recoveries are shape-determined, not model-determined.** `denial-001` and
  `denial-012` — the two shapes making a checkable claim about *disbursement* —
  fall to the ledger on both models that call it, 3/3 seeds, identically.
  Nothing else moves.
- **8 of 12 shapes are caught by nothing**, best arm still leaks 25/36.
- **Finding 27:** Haiku had the tool, called it 8 times, failed all 36. Having
  a tool, using it, and acting on it are three different things.
- **The completeness control validated live and unprompted:** every benign flag
  across all six arms was an `agent_failed` (a real unpaid customer) and **not
  one came from a held case**. ADR 0014's 0/15 was a proof over the corpus;
  this is the property holding against live models.

**3. Everything judge-facing corrected**, and the Artifact republished at the
same URL with the ablation panel and the live-rail act.

ADRs 17 → **18**. Findings 24 → **27**. Spend $10.70 → **$19.92** of $74.

## 2. Repo map — where things actually live

```
CLAUDE.md                    — operating manual, read this first in any session
transfer.md                  — THIS FILE (root, current build session)
docs/
  context/                   — frozen Day 1-5 research + transfer.md (read-only .md; .xlsx is live)
  decisions/0001-0011         — ADRs, one per phase above; read before touching that area
  gate-0-tracker.md            — resolved, kept for the record
  progress-tracker.md           — daily log against the 16-day plan
  eval-budget.md                 — spend ledger, $10.27 of $74, phase-by-phase
  eval-findings.md                 — 21 numbered findings, the evidence base for the narrative
  design/                            — DESIGN.md, SCREEN_MAP.md, ASSETS.md, TOOLING.md, IMAGE-PROMPTS.md
outreach/                    — ONE real conversation round (Day 4, pre-build). Thin — see §6.
submission/
  one-pagers/                — the 3 candidates that were scored, pre-lock
  demo-script.md               — the 90-second pitch script, 3-beat structure, real numbers
  demo-story.md                  — the full storyboard ("The Refund That Never Came")
  narrative.md                     — WRITTEN (2026-08-23), all seven sections, no PENDING markers left
  form-answers.md                    — the form's 4 content fields; Q12 in three lengths
  founder-email.md                   — still correctly parked (unlock condition now arguably met)
  demo/                                — the built page: index.html (source), warden-demo.html /
                                          warden-artifact.html (built, gitignored), img/, ui-data.json
src/                          — Warden itself: agent/ tool/ memory/ safety/ verification/ audit/
eval/                         — corpus.py, agent.py, harness.py, metrics.py, run.py, build_ui_data.py
tests/                        — 83 tests, all passing
```

---

## 3. Rules still in force (unchanged, see `CLAUDE.md` for full text)

1. No new problem after the lock (Track 01 / Warden is final).
2. No feature outside `submission/demo-script.md`.
3. Ship ugly-working over elegant-half-built.
4. Cut UI before cutting evaluation.
5. Never cite a synthetic user as validation evidence.
6. Track progress daily in `docs/progress-tracker.md`.
7. Don't add ASMOS features "because you can."
8. Founder email stays parked — **though the unlock condition
   (`docs/decisions/0004`: "a problem-lock ADR exists, ideally with the
   Phase 3-4 spine and evaluation numbers already real") now looks
   satisfied.** Worth a deliberate decision next session, not an assumption.

Every new invention still gets a numbered ADR in `docs/decisions/` — don't
edit old ones, supersede with a new file.

---

## 4. Budget remaining

**$54.08 of $74 remaining** ($19.92 spent — Phase A $0.01, B $2.01/$6,
C $2.99/$16, D $0.06, E $5.21/$6). Phases D and F–H allocations were never
spent (semantic-layer ablation, cross-model final runs) — deliberately, since
every problem so far was solved deterministically. Re-read
`docs/eval-budget.md`'s spending rules before running anything expensive:
calibrate on a *representative* sample, not a prefix (Finding 16 — a real
19% forecast miss happened exactly this way).

---

## 5. What a future session should NOT re-do

- Don't re-research Razorpay facts, re-open problem selection, or re-litigate
  the lock.
- Don't re-run the full multi-seed evaluation — the numbers are recorded in
  `docs/eval-findings.md` and `submission/demo/ui-data.json`. Only re-run if
  the corpus or the system under test actually changes.
- Don't regenerate the storyboard images from scratch — `IMAGE-PROMPTS.md`
  and the five files in `submission/demo/img/` already exist; only Panel 1
  is currently wired into the page.
- Don't re-derive the "why Warden not a classifier" argument — it's ADR 0007,
  settled.

---

## 6. Immediate next actions

**Everything below except item 1 was completed on 2026-08-24 (Phase P).**

1. **Record the 5-minute pitch video.** ⛔ **The only hard blocker left.**
   The live demo is the thing to record for the rail segment: start
   `make live` **before** hitting record (the first run warms the pipeline),
   mint a payment, then run benign → attack → denial in that order.
   Script: `submission/video-script.md`, 8 segments, retimed to exactly 5:00
   after SEG 4b (the ablation) was added. Visual asset:
   `submission/demo/warden-demo.html`. Not something Claude can do.
   - **Note:** the demo page gained a new scene (`s06b`, the ablation panel).
     It was verified structurally — markup, CSS, and a matching scroll-scene
     handler are all present in the built files — but **not verified visually**,
     because the browser pane would not composite in this session.
     **Look at it once before recording.**
2. ~~Verify and fix GitHub repo visibility.~~ Done — public, verified.
3. ~~Draft `submission/narrative.md`.~~ Done, and rewritten in Phase P.
4. ~~Draft the "what broke" answer.~~ Done, and rewritten in Phase P — it now
   leads with the two confounds found in the project's own evidence, which is
   stronger material than the original bug-fix framing.
5. **One more real outreach round** — still open, still Deepak's. Brief:
   `outreach/02-round-two-brief.md`. Now has better material to show: the
   ablation is a more interesting thing to walk someone through than a
   catch rate.
6. ~~Decide on the founder email.~~ Done — ADR 0017, unparked and drafted at
   `submission/founder-email.md`. **Deepak sends.**

### If there is time after the video, ranked by value

1. **Multi-seed the ablation arm** (~$3 on Sonnet). The 3-of-6 split on
   `denial-001` is n=1 and is reported as a direction, not a rate. This is the
   single weakest point in the strongest finding.
2. **Run the nine new denial cases against a live model.** They are covered
   deterministically in `tests/test_completeness_holds.py` but have never been
   run against a model, so the corpus says 12 denial cases and the *measured*
   number is still 3.
3. **Hold aging.** `deferred` never expires, which is the one limitation in
   ADR 0014 that a sharp reviewer will name. A clock and a per-hold SLA.
4. **Re-run the corpus against the mandate layer** so ADR 0012 carries measured
   numbers rather than only tests.

Lower priority, don't chase: audit replay/queryability (never in the demo
script, so never earned build time per rule 2), finalizing "Warden" as a real
product name.
