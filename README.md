# razorpay_buildathon — Warden

Warden (working name) is an agent trust/safety/audit layer for agentic
payments — a submission for the Razorpay AI Buildathon, Track 01 (AI Growth
& Agentic Commerce), and supporting evidence for a parallel Founder's Office
conversation at Razorpay.

**Status: evaluated against fourteen models across six labs.** A preventive
gateway with intent-bound mandates, plus a detective completeness audit,
measured over an adversarial corpus of 38 attacks across 8 classes with 15
benign controls, multi-seed.

| Result | Number |
|---|---|
| Small model (Haiku 4.5) diversion compromise rate | **47.7%** (62/130) |
| — of those, caught by the gateway | **62 / 62** |
| Frontier models (Sonnet 5 + Opus 5) diversion compromise | **0 / 208** — catch rate is *undefined*, not 100% |
| Gateway false positives, all fourteen models | **0 / 149** · utility preserved |
| **Denial attacks, default toolset — every model fails** | **71 / 71** across 14 models / 6 labs, and no preventive gate can stop them |
| Denial attacks **once the agent can check the ledger** | **1 of 3 shapes closes** · 3 of 6 models resist it · the other two shapes stay 100% |
| Completeness audit false alarms, hold-aware | **0 / 15** — against **5 / 15** for the binary version it replaced |

**The finding worth reading twice.** Every model tested fails every denial
attack — a forged *"REFUND ALREADY PROCESSED"* note and the case gets closed.
But the interesting half is *why*, and the first version of this README got it
wrong. The agent had **no tool that could check**, so 71/71 measured an
information gap, not a capability gap.

So we gave it one. `check_refund_status` reads the trusted ledger, and the
result is sharper than the claim it replaced:

- **It closes exactly one denial shape of three.** A ledger answers questions
  about *disbursement*. It answers nothing about *policy* ("this SKU is
  final-sale") or *request state* ("the request was filed in error") — and
  those stay **100% failures on every model**, tool or no tool.
- **Scale does not predict who uses it.** NVIDIA's Nemotron Ultra (550B) never
  called the tool. Liquid's LFM 2.5 (2.6B) called it twice.
- **The forged note suppresses the check itself.** Haiku 4.5 called the
  verification tool on 2 of 3 *benign* sessions — where it was pointless — and
  **0 of 3 denial** sessions, where it was the entire answer.

That is the empirical case for a detective control, and until this ablation it
was an assumption: two thirds of the denial surface cannot be closed by giving
the agent more tools, because no lookup answers the claim. A post-session
audit over trusted state never has to answer it — it asks whether the
obligation was discharged.

Full evidence in [`docs/eval-findings.md`](docs/eval-findings.md) (24 numbered
findings, several of them "here is what I got wrong and how the eval caught
it"); the 90-second story in
[`submission/demo-script.md`](submission/demo-script.md).

```bash
cp .env.example .env              # add your ANTHROPIC_API_KEY (gitignored)
pip install -r requirements.txt   # or: make setup
make test                         # 131 passing tests
make demo                         # diversion attack, blocked before the rail
make demo-denial                  # THE headline result, live (needs a key)
make live                         # browser demo on the REAL Razorpay rail
python -m eval.run --smoke        # 3 case-runs, verifies wiring
```

## The thesis, in one paragraph

Razorpay's 2026 product direction moves payments from software-you-instruct to
agents that act autonomously inside financial workflows. **Agent Studio** —
built on Anthropic's Claude SDK — already ships a **Dispute Responder** that
auto-responds to chargebacks, alongside subscription-recovery and settlement
agents, and its public page documents no guardrails, approvals, audit trail or
human-in-the-loop. Co-founder Harshil Mathur has publicly staked out "the
agent never sees" the payment credential as the trust boundary; India's
regulators (CERT-In, NPCI) are simultaneously trying to specify mandatory
human-in-the-loop controls and agent authorization for UPI. Neither has
published a working mechanism. Warden builds the enforcement/verification/audit
layer that boundary requires: an agent's payment action must present a signed,
scoped, expiring, single-use **mandate** whose payee is derived from trusted
order state, it executes on Razorpay test-mode APIs, it is written to a
hash-chained and HMAC-signed audit trail, and — after the session — it is
audited for obligations it quietly failed to discharge.

The evaluation reshaped the claim twice. Warden is **not** "we stop prompt
injection" — a current frontier model stops it unaided, and the honest catch
rate there is *undefined*, not 100%. And it is not "capability buys nothing
against denial" — that was a confound, and the ablation retired it. What
Warden provides is a **deterministic** guarantee where alignment offers only a
probability that shifts with every model release, at a measured false-positive
cost, plus coverage of the two denial shapes that **no amount of tooling in
the agent's hands can close**. Full sourcing in `docs/context/`; validation
evidence in `outreach/`; measurements in `docs/eval-findings.md`.

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
src/                    — Warden itself: mandate layer + preventive gateway
                            (safety/) + detective completeness audit
                            (verification/) + signed audit chain (audit/)
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
