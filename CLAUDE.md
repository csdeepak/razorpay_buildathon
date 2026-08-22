# CLAUDE.md — Operating Manual for This Repo

This repo is Deepak's campaign to become a Razorpay **AI Builder Intern** via two
reinforcing tracks: the **Razorpay AI Buildathon** (student-only, no resume
screening, apply-by-deadline in `docs/gate-0-tracker.md`) and a **Founder's
Office** email that stays parked until the Buildathon project thesis is locked.

Read this file first in any new session. It is the condensed operating manual —
full historical research lives in `docs/context/`, do not re-derive it.

## Non-negotiable rules of engagement

These come from `docs/context/Razorpay_16_Day_Battle_Plan.md` §6 and are binding
on every session, not suggestions:

1. **No new problem after the Day 5 lock.** Once `docs/decisions/` has an ADR
   locking the problem, do not reopen problem selection.
2. **No feature that isn't in `submission/demo-script.md`.** If it's not on
   screen for 90 seconds, it doesn't earn build time.
3. **Ship the ugly working version before the elegant half-built one.**
4. **Cut UI before cutting evaluation.** The evaluation numbers are the moat.
5. **Never cite a synthetic/AI-roleplayed user as validation evidence.** Ever.
   Personas may only be used to rehearse a pitch before it goes to a real
   human — never cited, never in a deliverable. See `outreach/README.md`.
6. **Track percentage completion daily** in `docs/progress-tracker.md`. A
   slipping gate means cut scope, not extend the phase.
7. **Do not add a feature "because ASMOS already has it."** That specific
   impulse is Deepak's identified failure mode — scope creep dressed as
   technical ambition.
8. **The founder email stays parked** (`submission/founder-email.md`) until
   the project thesis is locked.

## The workflow rule for this repo: log every invention

Whenever a new architectural decision, mechanism, or approach is invented —
a chosen problem, a system design, a safety/verification scheme, an evaluation
method, anything a future session or a Razorpay judge would need to understand
*why* — create a new file in `docs/decisions/` using the template in
`docs/decisions/README.md`. Use `/new-decision` to scaffold one. Don't
retroactively edit an old decision record to reflect a new choice — superseding
decisions get their own new file that references the one it replaces.

## Repo map

See `docs/REPO_MAP.md` for the full navigable mind map. Short version:

| Path | What lives here | When it's touched |
|---|---|---|
| `docs/context/` | Frozen historical research (transfer note, Phase 1 research, battle plan) **plus** the scoring spreadsheet, which is a living working tool | The three `.md` files are read-only — supersede via a new ADR instead. The `.xlsx` is meant to be edited directly (its own header says so); log anything that changes the problem thesis as an ADR too. |
| `docs/decisions/` | ADRs — one file per invented thing | Every time something new is decided |
| `docs/gate-0-tracker.md` | The 6 unresolved Buildathon-mechanics questions blocking everything | Update the moment Deepak opens the real buildathon page |
| `docs/progress-tracker.md` | Day-by-day % completion against the 16-day plan | Daily |
| `submission/` | Everything that ships to Razorpay: one-pagers, demo script, final narrative, parked founder email | Days 3, 5, 14–15 |
| `outreach/` | Real validation conversation notes only — never synthetic | Day 4 |
| `src/` | Warden itself — locked, built: agent/tool/memory/safety/verification/audit | Built Days 6–9 equivalent |
| `eval/` | Adversarial evaluation harness + corpus, multi-model results in `docs/eval-findings.md` | Built; $10.27 of $74 spent |

## Current status

**Read `transfer.md` (repo root) first** — it's the running handoff note for
this build session: every phase completed, exact file map, budget remaining,
and the prioritized next actions. Check `docs/gate-0-tracker.md` and
`docs/progress-tracker.md` for the live gate state, but do not infer overall
status from memory of a past session — `transfer.md` is kept current for
exactly that reason.
