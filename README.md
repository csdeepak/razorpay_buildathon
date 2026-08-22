# razorpay_buildathon — Warden

Warden (working name) is an agent trust/safety/audit layer for agentic
payments — a submission for the Razorpay AI Buildathon, Track 01 (AI Growth
& Agentic Commerce), and supporting evidence for a parallel Founder's Office
conversation at Razorpay.

**Status: evaluated against three live models (2026-08-22).** Preventive
gateway plus a detective completeness audit, measured over an adversarial
corpus of 29 attacks across 8 classes with 9 benign controls, multi-seed, on
Claude Haiku 4.5, Sonnet 5, and Opus 5.

| Result | Number |
|---|---|
| Small model (Haiku 4.5) compromise rate | **47.7%** (62/130) |
| — of those, caught by the gateway | **62 / 62** |
| Frontier models (Sonnet 5 + Opus 5) compromise rate | **0 / 208** — catch rate is *undefined*, not 100% |
| False positives, all nine models | **0 / 134** · utility preserved |
| **Denial attacks — every model fails** | **56 / 56** across 9 models / 3 labs, and no preventive gate can stop them |
| — caught by the completeness audit | **56 / 56**, 0 false alarms |

**The finding worth reading twice:** zero diversion attacks compromised a
frontier model — and *every single* denial attack succeeded against *every*
model tested: **nine models, three labs (Anthropic, Google, NVIDIA), 9B to
frontier.** It does not thin out with scale; a 550B model falls for the forged
note as reliably as a 9B one. Denial is the one class where capability buys
nothing, and it is the class a preventive gate cannot address by construction.
The completeness audit catches all of it, deterministically.

Full evidence in [`docs/eval-findings.md`](docs/eval-findings.md); the
90-second story in [`submission/demo-script.md`](submission/demo-script.md).

```bash
cp .env.example .env              # add your ANTHROPIC_API_KEY (gitignored)
pip install -r requirements.txt   # or: make setup
make test                         # 83 passing tests
python -m eval.run --smoke        # 3 case-runs, verifies wiring
```

## The thesis, in one paragraph

Razorpay's 2026 product direction (Vulcan, Agent Studio, the Agentic
Platform) moves payments from software-you-instruct to agents that act
autonomously inside financial workflows — while co-founder Harshil Mathur has
publicly staked out "the agent never sees" the payment credential as the
trust boundary. India's regulators (CERT-In, NPCI) are simultaneously trying
to specify mandatory human-in-the-loop controls and agent authorization for
UPI, and neither Razorpay nor the regulators have published a working
mechanism yet. Warden builds the enforcement/verification/audit layer that
boundary requires: an agent's payment is gated against policy derived from
trusted state, executed on Razorpay test-mode APIs, written to a
tamper-evident audit trail, and — after the session — audited for
obligations it quietly failed to discharge.

The evaluation reshaped the claim. Warden is **not** "we stop prompt
injection" — a current frontier model stops it unaided, and the honest
catch rate there is *undefined*, not 100%. What Warden provides is a
**deterministic** guarantee where alignment offers only a probability that
shifts with every model release, at a measured cost of zero false positives
— and coverage of **denial attacks**, which every model tested fails 100% of
the time and which no preventive gate can address. Full sourcing in
`docs/context/`; validation evidence in `outreach/`; measurements in
`docs/eval-findings.md`.

## Repo structure

```
CLAUDE.md              — operating manual for AI-assisted sessions in this repo
docs/
  context/              — frozen research (.md, read-only) + the scoring
                            spreadsheet (.xlsx, a living tool, edit freely)
  decisions/             — ADRs: one file per invented/locked decision
  gate-0-tracker.md       — the 6 buildathon-mechanics questions (resolved)
  progress-tracker.md      — daily % complete vs. the 16-day plan
  REPO_MAP.md              — full navigable mind map
submission/             — everything that ships to Razorpay (one-pagers, demo
                            script, final narrative, parked founder email)
outreach/               — real validation conversations only, never synthetic
src/                    — Warden itself: preventive gateway (safety/) +
                            detective completeness audit (verification/)
eval/                   — adversarial corpus + evaluation harness
.claude/commands/       — Claude Code workflow commands (see below)
```

See `docs/REPO_MAP.md` for the full mind map and routing logic, and
`CLAUDE.md` for the rules of engagement this repo runs on.

## Working with this repo (Claude Code)

Custom commands in `.claude/commands/`:

- `/new-decision` — scaffold a new ADR when something gets invented or locked
- `/gate-check` — report current gate status and flag any rule at risk
- `/log-progress` — append today's entry to the progress tracker
- `/demo-check` — cross-check `src/` against the demo script for scope drift

## Status tracking

- Blocking question: [`docs/gate-0-tracker.md`](docs/gate-0-tracker.md)
- Daily progress: [`docs/progress-tracker.md`](docs/progress-tracker.md)
- Decisions made so far: [`docs/decisions/`](docs/decisions/)

## License

MIT — see `LICENSE`.
