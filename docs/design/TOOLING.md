# TOOLING.md — which playbook tools we actually use, and why

The playbook (`Buildathon_UI_Design_Workflow_Playbook.md`) recommends a
stack. It also warns, correctly, in §10 and §17: *"Do not install every
resource… more installed skills can become context noise"* and *"do not use
five different UI libraries because each has one attractive component."*

So this is a deliberate subset, not the whole list.

---

## The constraint that drives every choice below

**Delivery target: a single self-contained HTML page.**

It has to be (a) screen-recorded for the 5-minute pitch video, (b) openable
by a judge from the repo with no build step, and (c) publishable as an
Artifact — where a strict CSP blocks every external request **except Google
Fonts**.

That rules out a React + Tailwind + shadcn build pipeline before we even
evaluate it on merit. Inline CSS and a small amount of vanilla JS is not a
compromise here; it is the only thing that satisfies the target.

---

## Playbook layer → what we're actually doing

| Playbook layer | Its recommendation | What we use | Status |
|---|---|---|---|
| **Design spec** | `xiaopu-ai/web-design` (PRD → DESIGN.md → code) | **The method, applied by hand.** `DESIGN.md`, `SCREEN_MAP.md`, `ASSETS.md` already follow its nine-section structure | ✅ done, no install |
| **Browser QA** | Playwright MCP | **Claude Browser tools** — same loop: navigate, read DOM, resize viewport, read console. Already used to measure the reference's live tokens | ✅ available now |
| **Design reference** | Figma MCP | **Figma MCP is connected** in this session | ✅ available, optional — see the fork below |
| **Visual direction** | `taste-skill` (reference-driven) | **Done differently and better:** we measured the actual reference's computed styles instead of describing it | ✅ done |
| **Artifact quality** | — | **`artifact-design` skill** — mandatory load before writing the page | ✅ will use |
| **Data display** | — | **`dataviz` skill** — for the counters, intervals and the 8×3 grid | ✅ will use |
| **Motion** | `emil-design-eng` | Hand-specified in `DESIGN.md` §7 | ⚠️ optional install |
| **Critique** | `impeccable` | Playbook §16 checklist, run manually against the built page in a real browser | ⚠️ optional install |
| **Components** | shadcn/ui + Tailwind, or DaisyUI | **None. Deliberately.** See below | ❌ skipped |
| **Images** | Unsplash / Pexels API | **None needed** — `ASSETS.md` eliminated photography | ❌ eliminated |

---

## Why no component library

The playbook's advice to use mature UI kits is right **for dashboard-heavy
products**. This page is not one. Take an honest inventory of what it needs:

| Conventional component | Needed here? |
|---|---|
| Forms, inputs, validation | No |
| Modals, drawers, toasts | No |
| Tabs, accordions, dropdowns | One expandable card in WIDEN 3 |
| Data tables, pagination | No |
| Nav bar, breadcrumbs | No — scroll is the only navigation |
| Segmented control | Yes — one, the model selector |

Everything else is bespoke: a spine, a travelling token, a gate that fires,
an audit rail that chains, an 8×3 grid. **No library ships those.**

Importing Tailwind + shadcn to obtain one segmented control and one
expandable card is precisely the anti-pattern in playbook §17. The component
set in `DESIGN.md` §6 is twelve hand-built pieces, all of which are specific
to this narrative.

---

## What's worth installing, if you want it

Both need a Claude Code restart afterward (playbook §11), so they're your
call, not something I can do mid-session:

```bash
npx impeccable install
```

Then `/impeccable init` inside Claude Code. **This is the one I'd actually
recommend** — a second-pass critique with deterministic UI-smell detection is
genuinely useful on a page this bespoke, precisely because there's no
component library enforcing consistency for us.

```bash
npx skills add https://github.com/emilkowalski/skills --skill emil-design-eng
```

Motion judgment. Lower value here only because `DESIGN.md` §7 already commits
to specific durations, easings and the two rules that matter. Worth it if you
want a second opinion on the choreography.

**Skipping the rest** — `taste-skill`, `claude-design-skill`,
`ui-ux-skill`, `design-skills`, DaisyUI, Flowbite, Preline, TailAdmin,
TailGrids. Each solves a problem this page doesn't have, and the playbook's
own warning about context noise applies.

---

## The fork: who designs the pixels

Figma MCP is connected, which makes two workflows possible. This is your
call:

**Option A — I build straight from the specs.** I implement `DESIGN.md` +
`SCREEN_MAP.md` directly as HTML/CSS/JS, then we iterate in the browser
together. Fastest path to something running and screen-recordable.

**Option B — you design in Figma, I read and implement it.** You lay out
frames with real variables and auto-layout; I pull them through Figma MCP
(`get_design_context` gives me variables, components, spacing tokens) and
implement against your actual design rather than my written spec. Slower,
but the pixels are yours — and given you said you want to design the UI,
this may be what you actually meant.

The specs already written serve both paths: in Option B they become the
brief you design against, rather than the thing I build from.

---

## Definition of done (playbook §18, applied)

| Check | How we'll verify |
|---|---|
| Storyboard fidelity | Every verb in `demo-story.md` maps to a visible state |
| Flow | Full scroll, no dead ends, replay works from every act |
| Design system | Tokens only — no hard-coded hex outside `:root` |
| Assets | `ASSETS.md` manifest; no invented URLs |
| Responsive | Browser tools at 1280 / 768 / 375 |
| Accessibility | Contrast pass, keyboard nav on grid + selector, S06's non-visual equivalent present |
| States | Reduced-motion reading tested as a real path, not a checkbox |
| Motion | Every animation traces to an action verb |
| Browser QA | Actually exercised, not assumed |
| Demo | First 90 seconds carry the strongest story |
