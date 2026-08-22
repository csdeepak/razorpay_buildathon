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
(**83 passing tests**), runs against **Razorpay's real test-mode API**, and is
evaluated against **nine models across three labs** (Anthropic, Google,
NVIDIA) for **$10.27 of a $74 budget** — the six non-Anthropic models cost
$0.00. The core finding — every model resists diversion but **all nine fail
100% of denial attacks, 56/56**, which a completeness audit then catches 56/56
with 0 false alarms in 134 benign sessions — is strong and demo-ready.
`submission/narrative.md` and `submission/form-answers.md` are written. A
scroll-driven demo page exists, is built, and is published as a private Claude
Artifact.

**Two things remain, both Deepak's and neither of them engineering: the
GitHub repo is still private (form Q10, a hard blocker — verified 404
unauthenticated on 2026-08-23), and the 5-minute pitch video is not
recorded.** See §6.

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

Full findings log: `docs/eval-findings.md` (19 numbered findings, several
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
   subset run on six more models across two more labs for **$0.00**:
   **56/56 across nine models, three labs, 9B to frontier.** The single-lab
   confound under the sharpest claim is gone. Gemini free tier is **20
   requests/day/model**, which is why the arm is denial-only and n=1.
4. **Consistency pass** across every judge-facing file — narrative, demo
   script, form answers, README, demo page, ui-data.

Tests 24 → 83. ADRs 9 → 11. Findings 16 → 19. Spend unchanged at $10.27.

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
  eval-findings.md                 — 19 numbered findings, the evidence base for the narrative
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

**$63.73 of $74 remaining** ($10.27 spent — Phase A $0.01, B $2.01/$6,
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

## 6. Immediate next actions — the actual next phase

Per Deepak: next phase is **understanding where the project stands** and
**filling gaps at specific stages** rather than new building. In priority
order:

1. **Verify and fix GitHub repo visibility.** Checked this session: both the
   GitHub API and the page itself returned "not found" for
   `github.com/csdeepak/razorpay_buildathon` on an unauthenticated request —
   consistent with the repo being **private**. The Buildathon form requires
   a *public* repo URL. This is a hard blocker and it's a two-click fix in
   GitHub's own settings (Claude can't do it — no `gh` CLI in this
   environment, and it's Deepak's account setting regardless). **Do this
   first, before anything else, and confirm.**
2. **Draft `submission/narrative.md`.** Currently an empty template. Every
   fact it needs already exists across the 9 ADRs and `eval-findings.md` —
   this is synthesis, not new research, and Claude can draft it directly
   once asked.
3. **Draft the "what broke, and how you got out" form answer.** Razorpay
   reads this one first. Best raw material: ADR 0008 (amount binding),
   Finding 6 (n=1 nearly deleted 5 good cases), Finding 5 (a metric that was
   measuring the test harness, not the system), Finding 12 (a smarter model
   exposed a badly-written benign case). Needs distilling to ~1 paragraph.
4. **Record the 5-minute pitch video.** The demo page and
   `submission/demo-script.md` exist specifically to support this. Not
   something Claude can do; can help tighten the script first.
5. **One more real outreach round**, showing the *built* Warden system (not
   just the problem) to a couple of real people — ideally including whoever
   gave Deepak the founder-office contact. Strengthens "problem taste" and
   "AI judgment," two of Razorpay's four stated judging criteria, with
   post-build evidence rather than only pre-build validation.
6. **Decide on the founder email deliberately.** The parking condition looks
   satisfied now (locked problem + real spine + real evaluation numbers) —
   worth an explicit ADR-style decision either way, not a default.

Lower priority, don't chase unless the above are done: growing the corpus
past 29 cases, deepening audit replay/queryability (Day 10, never in the
demo script, so never earned build time per rule 2), finalizing "Warden" as
a real product name instead of a working one.
