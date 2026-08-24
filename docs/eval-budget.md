# Evaluation Budget — $74 org credits

Living document. **Update the ledger at the bottom after every run.** Every
`python -m eval.run` prints its own cost; copy that number in rather than
estimating.

Hard constraint: **$74 total**, covering everything from here (2026-08-22)
to submission (2026-09-05). There is no second tranche.

## Cost basis — MEASURED 2026-08-22 (Phase A smoke)

Real figures from the smoke run: **3,018 input + 344 output tokens per
case-run**. My pre-run estimate (3,500/550) overestimated output by ~60%.

| Model | $/1M in | $/1M out | $/case-run | 32-case run | 150 cases x 5 seeds |
|---|---:|---:|---:|---:|---:|
| `claude-opus-5` | 5.00 | 25.00 | $0.024 | $0.76 | $17.78 |
| `claude-sonnet-5` | 2.00\* | 10.00\* | $0.010 | $0.31 | $7.16 |
| `claude-sonnet-5` (after Aug 31) | 3.00 | 15.00 | $0.014 | $0.46 | $10.66 |
| `claude-haiku-4-5` | 1.00 | 5.00 | $0.005 | $0.15 | $3.53 |

**Treat these as a lower bound.** The smoke sample was 3 *single-turn* cases
on the *tersest* model. Two things will push the real blended average up:

- **Multi-turn cases** (3 in the corpus, more coming) roughly double the
  conversation length.
- **Opus and Sonnet are more verbose** than Haiku, so output tokens — the
  expensive side, at 5x the input rate — will rise.

A prudent working assumption is **1.4–1.8x these figures** for a blended
corpus on a larger model. Phase B runs the full corpus and will produce a
true blended average; recalibrate again then, before committing to Phase C.

\* **Sonnet 5 introductory pricing ends 2026-08-31** — mid-project. After
that it's $3.00/$15.00, a 50% jump. **Front-load Sonnet runs before Aug 31.**

## Model allocation — and why it isn't only about cost

The agent under test does **not** need to be the most capable model, and
there's a methodological reason beyond price:

> The headline metric conditions on the agent actually being compromised
> (`eval/README.md`). A cheaper, less-aligned model gets compromised **more
> often**, which yields *more* enforcement signal per dollar. Opus 5 resisting
> an attack on its own produces an `AGENT_RESISTED` row that contributes
> nothing to the catch rate.

So cheap models aren't a degraded substitute here — for corpus development
they're the *better* instrument. And running across all three tiers supports
a stronger final claim than any single-model result: **"enforcement holds
regardless of which model drives the agent."**

| Phase | Model | Why |
|---|---|---|
| A. Wiring / smoke | Haiku 4.5 | Verifying plumbing, not measuring anything. |
| B. Corpus development → ~150 cases | Haiku 4.5 | Highest compromise rate = fastest signal on whether a written attack actually works. |
| C. Baseline + structural arms | Sonnet 5 | Primary reported results. Use before Aug 31 for intro pricing. |
| D. Semantic layer + ablation | Sonnet 5 | Third arm; the ablation is the ASMOS-grade differentiator. |
| E. Cross-model check | Opus 5 | Subset only. Supports the "holds across models" claim. |
| F. Final reported runs | Sonnet 5 + Opus 5 | The numbers that go in the submission. |

## Allocation

| Phase | Budget | Running total |
|---|---:|---:|
| A. Wiring / smoke (Haiku) | $1 | $1 |
| B. Corpus development to ~150 cases (Haiku) | $6 | $7 |
| C. Baseline + structural, 5 seeds (Sonnet) | $16 | $23 |
| D. Semantic layer + 3-arm ablation (Sonnet) | $12 | $35 |
| E. Cross-model check, subset (Opus) | $6 | $41 |
| F. Final reported runs + reruns | $13 | $54 |
| **Reserve (27%)** | **$20** | **$74** |

**The reserve is not padding.** The single biggest budget risk on this
project is discovering a harness bug *after* an expensive run and having to
redo it. Twenty dollars buys roughly two full Sonnet re-runs. Do not spend it
early.

## Spending rules

1. **Never run the full corpus at full seeds without a `--limit` dry run
   first.** One bad flag can burn a phase's budget in a single command.
2. **Always pair a protected run with its baseline** — but run the baseline
   at the *same* model and seed count, or the comparison is meaningless.
3. **Iterate at `--seeds 1`.** Multi-seed is for numbers you report, not for
   debugging.
4. **Recalibrate after every phase.** Copy the real `$/case-run` from the
   run's own output into the table above.
5. **Stop and re-plan if any phase overruns by >50%.** That means the token
   estimates are wrong, and every later phase is wrong too.
6. Raw run JSON in `eval/runs/` is gitignored — it holds full model output
   and would bloat the repo.

## Ledger

| Date | Phase | Command | Model | Case-runs | Cost | Remaining |
|---|---|---|---|---:|---:|---:|
| 2026-08-22 | A | `--smoke` | haiku-4-5 | 3 | $0.014 | $73.99 |
| 2026-08-22 | B | full corpus, `--enforcement none` | haiku-4-5 | 32 | $0.144 | $73.84 |
| 2026-08-22 | B | full corpus, `--enforcement structural` | haiku-4-5 | 32 | $0.162 | $73.68 |
| 2026-08-22 | B | verify amount-binding fix (ADR 0008) | haiku-4-5 | 33 | $0.158 | $73.52 |
| 2026-08-22 | B | expanded corpus (8 classes), structural | haiku-4-5 | 38 | $0.228 | $73.29 |
| 2026-08-22 | B | expanded corpus, matching baseline | haiku-4-5 | 38 | $0.195 | $73.10 |
| 2026-08-22 | B | **5-seed** structural (settles Finding 6) | haiku-4-5 | 190 | $1.105 | $71.99 |
| 2026-08-22 | C | Sonnet token calibration | sonnet-5 | 6 | $0.091 | $71.90 |
| 2026-08-22 | C | **5-seed** structural (reportable) | sonnet-5 | 190 | $2.900 | $69.00 |
| 2026-08-22 | D | completeness-check wiring confirmation | haiku-4-5 | 12 | $0.060 | $68.94 |
| 2026-08-22 | E | Opus token calibration (underestimated, see below) | opus-5 | 4 | $0.150 | $68.79 |
| 2026-08-22 | E | **3-seed** cross-model check | opus-5 | 114 | $5.063 | **$63.73** |

**Phase E: $5.21 of $6 — landed inside budget but the forecast was 19% low.**
`--limit N` takes a *prefix*, not a representative sample; calibrating on two
simple single-turn cases missed the multi-turn and denial cases that push
output tokens from 714 to 950 per case-run. See eval-findings Finding 16.
Opus basis for any future run: **$0.0444/case-run**.

### Current measured cost basis (supersedes the estimates at the top)

| Model | $/case-run | avg tokens | source |
|---|---:|---|---|
| `claude-haiku-4-5` | $0.0060 | 3,989 / 402 | Phase B, full corpus w/ follow-ups |
| `claude-sonnet-5` | $0.0153 | 4,308 / 664 | Phase C, 190 case-runs |
| `claude-opus-5` | $0.0444 | 4,130 / 950 | Phase E, 114 case-runs |

Phase-by-phase: **A** $0.01 · **B** $2.01 of $6 · **C** $2.99 of $16 ·
**D** $0.06 · **E** $5.21 of $6. Phase C came in far under budget because the
Sonnet baseline arm was skipped as uninformative — with zero compromises
there was nothing for a baseline to contrast against (eval-findings Finding
10).

Two cost effects worth carrying forward: enforcement itself adds ~13% tokens
(blocked agents write more), and contingent follow-up turns added another
~18% — that is what measuring utility honestly costs.

---

## Phase H — the affordance ablation (2026-08-24)

| Item | Cost |
|---|---:|
| Wiring smoke check (`--smoke`, Haiku) | $0.021 |
| Ablation, `claude-haiku-4-5` (run twice: first pass lacked `tool_reads`) | $0.034 |
| Ablation, `claude-sonnet-5` | $0.094 |
| Ablation, `claude-opus-5` | $0.267 |
| Ablation, Gemini 3.6 Flash / Nemotron Ultra 550B / Liquid 2.6B | $0.000 |
| `make demo-denial` live verification (Opus) | ~$0.01 |
| **Phase H total** | **~$0.43** |

**Running total: $10.70 of $74.** $63.30 remaining.

Three notes worth carrying forward:

- **The instrumentation cost a re-run.** The first Haiku ablation pass had no
  `tool_reads` counter, so it could show *that* the model still failed and not
  *whether it had checked* — which was the entire question. Cheap here ($0.017)
  and it would not have been on Opus. **Decide what the arm has to distinguish
  before spending on it**, not after reading the first result.
- **Opus is 8x Haiku and answered the same question.** The 3-of-6 split was
  visible on Sonnet at a fifth of the price. Opus was worth it once, to close
  the frontier end of the range; it is not worth it for iteration.
- **Free tiers carried the interesting half.** Nemotron Ultra (550B) never
  calling the tool while Liquid (2.6B) called it twice — the observation that
  retired Finding 20's capability reading — cost **$0.00**.

### What the remaining $63.30 could buy, ranked

1. **Multi-seed the ablation arm** (~$3 on Sonnet, 5 seeds x 6 cases x 6
   models). The 3-of-6 split is currently n=1 and reported as a direction,
   not a rate. This is the single highest-value remaining spend.
2. **Re-run the full corpus against the mandate layer** (~$4 Haiku + Sonnet).
   Would let ADR 0012's layer carry measured numbers instead of only tests.
3. **Multi-seed the nine new denial cases** (~$2). They are currently covered
   deterministically in `tests/test_completeness_holds.py` but have never been
   run against a live model.

None of these are required for the submission. All three are the honest answer
to "what would you do next with the budget you didn't spend."
