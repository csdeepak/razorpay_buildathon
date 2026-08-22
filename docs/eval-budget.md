# Evaluation Budget — $74 org credits

Living document. **Update the ledger at the bottom after every run.** Every
`python -m eval.run` prints its own cost; copy that number in rather than
estimating.

Hard constraint: **$74 total**, covering everything from here (2026-08-22)
to submission (2026-09-05). There is no second tranche.

## Cost basis

Measured per-case-run averages will replace these after the first smoke run.
Current figures assume ~3,500 input + ~550 output tokens per case-run (a
multi-turn tool-calling conversation, ~3 model calls).

| Model | $/1M in | $/1M out | $/case-run | 32-case run | 150 cases x 5 seeds |
|---|---:|---:|---:|---:|---:|
| `claude-opus-5` | 5.00 | 25.00 | $0.031 | $1.00 | $23.44 |
| `claude-sonnet-5` | 2.00\* | 10.00\* | $0.013 | $0.40 | $9.38 |
| `claude-haiku-4-5` | 1.00 | 5.00 | $0.006 | $0.20 | $4.69 |

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
| — | — | *(nothing spent yet)* | — | 0 | $0.00 | **$74.00** |
