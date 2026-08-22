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
| 2026-08-22 | B | expanded corpus, matching baseline | haiku-4-5 | 38 | $0.195 | **$73.10** |

**Phase B spend so far: $0.89 of its $6 allocation.** Follow-up turns raised
the per-case-run basis to **$0.0060 structural / $0.0051 baseline** on Haiku
(from $0.0048) — longer conversations are the price of measuring utility
honestly. Use $0.0060 as the Haiku basis for Phase C forecasting, scaled to
the target model.

Blended per-case-run cost is now **measured over the real corpus** (multi-turn
cases included), which supersedes the smoke-run lower bound: **$0.0045
baseline / $0.0051 structural** on Haiku. The 1.4–1.8x uplift I warned about
did **not** materialise for Haiku — multi-turn cases barely moved the average.
Enforcement itself costs ~13% more (blocked agents write more; see
`docs/eval-findings.md` Finding 4). The verbosity uplift for Opus/Sonnet
remains untested and is still the main forecasting risk for Phase C.
