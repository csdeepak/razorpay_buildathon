# razorpay_buildathon

Building an agent trust/permissioning/verification/audit layer for
agentic payments — a submission for the Razorpay AI Buildathon
("Build. Show. Get hired.") and supporting evidence for a parallel
Founder's Office conversation at Razorpay.

**Status: pre-lock.** The problem is not yet chosen. Three candidates are
scored and under validation (see below) — expect this README to be rewritten
once `docs/decisions/` has a problem-lock ADR.

## The thesis, in one paragraph

Razorpay's 2026 product direction (Vulcan, Agent Studio, the Agentic
Platform) moves payments from software-you-instruct to agents that act
autonomously inside financial workflows — while co-founder Harshil Mathur has
publicly staked out "the agent never sees" the payment credential as the
trust boundary. India's regulators (CERT-In, NPCI) are simultaneously trying
to specify mandatory human-in-the-loop controls and agent authorization for
UPI, and neither Razorpay nor the regulators have published a working
mechanism yet. This project builds the enforcement/verification/audit layer
that boundary requires, protocol-agnostic, demoed by catching a real attack
rather than showing a policy screen. Full sourcing in `docs/context/`.

## Repo structure

```
CLAUDE.md              — operating manual for AI-assisted sessions in this repo
docs/
  context/              — frozen historical research (read-only)
  decisions/             — ADRs: one file per invented/locked decision
  gate-0-tracker.md       — the 6 buildathon-mechanics questions blocking everything
  progress-tracker.md      — daily % complete vs. the 16-day plan
  REPO_MAP.md              — full navigable mind map
submission/             — everything that ships to Razorpay (one-pagers, demo
                            script, final narrative, parked founder email)
outreach/               — real validation conversations only, never synthetic
src/                    — the system itself, empty until the problem locks
eval/                   — adversarial evaluation harness
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
