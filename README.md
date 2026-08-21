# razorpay_buildathon — Warden

Warden (working name) is an agent trust/safety/audit layer for agentic
payments — a submission for the Razorpay AI Buildathon, Track 01 (AI Growth
& Agentic Commerce), and supporting evidence for a parallel Founder's Office
conversation at Razorpay.

**Status: vertical slice running (2026-08-21).** Problem locked at Gate 2
after real-world validation across five conversations
(`docs/decisions/0004-problem-locked-track-01.md`); the Day 6–7 vertical
slice runs end to end (`docs/decisions/0005-vertical-slice-architecture.md`).
No safety gate yet — that's Day 8. No new problem after the lock —
`CLAUDE.md` rule 1.

```bash
pip install -r requirements.txt   # or: make setup
make demo                         # attack scenario: payout executes, then gets caught
make test                         # 6 passing tests
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
boundary requires: an agent's payment gets reasoned about, gated against
policy, executed on Razorpay test-mode APIs, and written to a tamper-evident
audit trail — demoed by catching a real prompt-injection attack rather than
showing a policy screen. Full sourcing in `docs/context/`; validation
evidence in `outreach/`.

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
src/                    — Warden itself. Vertical slice running; safety/ is
                            the one layer still empty (Day 8)
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
