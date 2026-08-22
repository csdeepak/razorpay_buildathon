# SCREEN_MAP.md — scenes, states, choreography

Answers the playbook's storyboard→UI questions (A–J) for
`submission/demo-story.md`. Read `DESIGN.md` alongside for tokens.

**One screen, many states.** This is not a multi-page app. It is a single
fixed stage whose contents change as the scroll advances. Scroll position is
the only navigation.

---

## A. User journey

There are two users and they need different things from the same page.

| | **The judge** (primary) | **The skimmer** (secondary) |
|---|---|---|
| Intent | "Is this real work, and does the claim hold?" | "What is this in 20 seconds?" |
| Path | Full scroll + drills into the grid + checks intervals | Scrolls fast, reads three counters, leaves |
| Success | Can repeat the one-sentence claim, and trusts the numbers | Remembers "denial attacks, nobody catches them, they did" |

Entry → normal path → attack caught → **widen: the whole space** → the honest
null result → **widen: how we measured** → the silence → the audit → **widen:
what broke** → close.

---

## B. Scene / state inventory

| ID | Scene | User intent | Stage state | Variants |
|---|---|---|---|---|
| **S00** | Act 0 — the ask | Understand who is at risk | Chat active, spine idle, balance ₹0 | first-load |
| **S01** | Act I — normal path | Learn the pipeline | Token travels → ALLOW → balance ₹1,250 | — |
| **S02** | Act II — hijack | See something go wrong and get stopped | OrderCard shows poisoned note → DIVERT → BLOCK | — |
| **S03** | ⊕ WIDEN 1 — the grid | "Was this one example or a study?" | Spine shrinks, 8×3 grid takes stage | `idle` · `cell-hover` · `cell-selected` · `not-testable` |
| **S04** | Act III — the turn | "Does this matter on a good model?" | DISSOLVE at agent, gate greys, **no amber on screen** | model = sonnet / opus |
| **S05** | ⊕ WIDEN 2 — method | "How do you know it isn't just the model?" | Three-way outcome split diagram | `resisted` · `blocked` · `leaked` emphasis |
| **S06** | Act IV — the silence | Feel the failure nobody sees | **Spine empty.** Timer runs. Merchant panel green. Balance frozen | the held beat |
| **S07** | Act IV — the audit | See it caught anyway | AUDIT-SWEEP rises → FLAG on empty spine | — |
| **S08** | ⊕ WIDEN 3 — what broke | Judge the rigour | Four findings, expandable | `collapsed` · `expanded` |
| **S09** | Act V — close | Leave with the sentence | Full-bleed statement | — |

---

## C. Primary action per scene

Most scenes have **no CTA** — the primary action is *keep scrolling*, and
that is correct for a narrative. Only three scenes accept input:

| Scene | Action | Why it exists |
|---|---|---|
| S03 | **Select a grid cell** → that attack replays in the shrunken spine | Turns a claim of breadth into something the judge verifies themselves |
| S04+ | **Model selector** (Haiku / Sonnet / Opus) | The single most convincing interaction available — interactive proof of model-independence |
| S08 | **Expand a finding** | Progressive disclosure; keeps the scroll readable |

Everything else is scroll-driven. **No scene may require a click to
progress.** A judge who never clicks still gets the whole argument.

---

## D. Content hierarchy per scene

Strict order of what the eye should hit. If an element isn't listed, it
shouldn't be competing for attention.

- **S00** → Rhea's message · the amount ₹1,250 · balance ₹0
- **S01** → the moving token · the balance ticking up
- **S02** → the poisoned note · the DIVERT · **the rule name** · the counter 62/62
- **S03** → the grid · **73.3% vs 33.8%** · the greyed 9th cell
- **S04** → the agent's own refusal quote · **the greyed gate** · counter "0"
- **S05** → the three-way split · **"UNDEFINED, not 100%"** · 0/117
- **S06** → **the empty spine** · merchant ✅ beside balance ₹0 · 39/39
- **S07** → the sweep · **OBLIGATION UNDISCHARGED** · 39/39 detected
- **S08** → the four failure headlines
- **S09** → the closing sentence, alone

---

## E. States a storyboard omits — and what we do about them

The playbook is right that this is where static storyboards fail. Most
conventional states **do not apply** here, and saying so explicitly is part
of the design:

| State | Applies? | Treatment |
|---|---|---|
| Empty | **Yes — and it's the payoff.** Act IV's empty spine | Deliberate. Never filled |
| Loading | **No.** All data is embedded at build time | If fonts are still loading, text renders in fallback — never a spinner |
| Error | **Only one:** JS disabled / animation unsupported | Page degrades to a fully readable static document. The argument survives |
| Partial | No | — |
| Success | Yes, twice: money arriving (S01), obligation caught (S07) | Green rationed to S01; S07 uses amber |
| Recovery | Yes — **replay** | Every act has a replay control; a judge can re-watch a beat without scrolling back |
| Permission / offline | No | Page is self-contained, makes no requests |
| Reduced motion | **Yes, first-class** | Travel becomes instant state change; layout and copy unchanged |

---

## F. Navigation and transitions

- **Scroll is the only navigation.** No nav bar, no anchors menu.
- **ActMarker rail** (fixed, left edge): act number + elapsed timestamp,
  Razorpay-style. Current act in amber. Clickable as a jump-to, but visually
  a progress indicator first.
- Act→act: the stage does **not** cross-fade. Elements exit on `e-exit`,
  the spine persists throughout — it is the one continuous object and the
  reason the page feels like one scene rather than nine.
- WIDEN transitions: spine scales down to ~40% and translates left; grid
  resolves in from `--cream-30`. RETURN reverses it. The spine never
  disappears during a WIDEN — it stays visible, small, as an anchor.

---

## G. Components required per scene

| Scene | Components |
|---|---|
| S00 | ActMarker, ChatBubble(customer), BalanceStrip, SpineNode×3 (idle) |
| S01 | + Token, OrderCard(clean), Counter |
| S02 | + OrderCard(poisoned), RuleChip, AuditRow |
| S03 | + AttackGrid, Counter(vector rates) |
| S04 | + ModelSelector, ChatBubble(agent quote) |
| S05 | + OutcomeSplit (3-way diagram), Counter×3 |
| S06 | + MerchantPanel, elapsed timer |
| S07 | + AuditSweep, FlagBanner |
| S08 | + FindingCard ×4 (expandable) |
| S09 | Statement block only |

New component surfaced by this pass, not in DESIGN.md §6: **`OutcomeSplit`**
— the three-way `AGENT_RESISTED / ENFORCEMENT_BLOCKED / LEAKED` diagram for
S05. Add it.

---

## H. Data required, and where it comes from

All embedded as inline JSON at build time from `eval/runs/*.json`. **No
runtime requests.** The page states that these are recorded measurements.

| Component | Data | Source |
|---|---|---|
| ChatBubble(agent) | Verbatim model output | `phaseC-sonnet-structural.json` → `agent_final_text` |
| OrderCard | Order fixture + poisoned note | `eval/corpus.py` → `ORDERS`, `poisoned_order_notes` |
| Token | amount, destination | `proposed_actions[].arguments` |
| RuleChip | rule name | `proposed_actions[].rule_fired` |
| AuditRow | event, hash | `src/audit/ledger.py` shape |
| Counter | rate + Wilson interval | `eval/metrics.py` output |
| AttackGrid | class × vector compromise rates | Aggregated across all three run files |
| ModelSelector | per-model outcomes | `phaseB-multiseed`, `phaseC-sonnet`, `phaseE-opus` |
| MerchantPanel | "resolved", 41s | From the denial run's session |

**Build step needed:** a small script to reduce the three run JSONs into one
`ui-data.json`. Raw runs are gitignored and too large to embed directly.

---

## I. Accessibility

Covered in `DESIGN.md` §9. Scene-specific additions:

- **S06 is the risk.** A visual "nothing happens" is invisible to a screen
  reader. It needs an explicit, non-visual equivalent: *"No action was taken.
  The refund was never issued. The case was closed."* — present in the DOM,
  not conveyed by the empty spine alone.
- S03 grid: arrow-key navigable, each cell labelled `class, vector,
  compromise rate`.
- The elapsed timer in S06 must not be an `aria-live` region — it would spam
  a screen reader. Mark it `aria-hidden` and carry the meaning in prose.

---

## J. What should NOT be shown

- No architecture diagram of all six `src/` layers. Three are thin by design;
  equal visual weight misrepresents the system.
- No latency/cost charts on the main scroll. Real, but nobody's headline —
  expandable detail only.
- No live-looking dashboard. Nothing here is live and pretending otherwise
  undercuts the honesty the piece is built on.
- No attacker persona, avatar, or "threat actor" iconography.
- No logos of Razorpay, Anthropic, or NPCI — we reference them in copy, we
  do not borrow their marks.
- No countdown timers, no "trusted by", no fake testimonials.
- F16 (calibration-on-a-prefix) stays in the repo. Too inside-baseball.

---

## Choreography — the full scroll

Scroll % is of total document height. Each beat lists its action verbs from
`submission/demo-story.md`.

| % | Scene | Verbs | What moves |
|---|---|---|---|
| 0–6 | S00 | REQUEST | Chat bubble types in. Spine idle at `--line`. Balance ₹0. Timer starts |
| 6–14 | S01 | LOOKUP → REASON → PROPOSE → MOVE → CHECK → ALLOW | OrderCard flips. Token materialises at agent, travels, pauses at gate `t-beat`, gate opens amber-dim, token continues, balance ticks to ₹1,250 in `--settled`. AUDIT-WRITE drops one row |
| 14–30 | S02 | LOOKUP(poisoned) → PROPOSE → **DIVERT** → CHECK → **BLOCK** | Note renders in `--danger` inside OrderCard. Token forms with the wrong destination, leaves the spine on `e-wrong`. Gate fires amber. **Token stops dead, 0ms.** RuleChip `payee_scope`. AuditRow. Counter 62/62 |
| 30–40 | S03 | **WIDEN** → DRILL → RETURN | Spine scales to 40%, moves left. Grid resolves. Rhea's cell marked. Vector rates count up. 9th cell greyed, labelled |
| 40–52 | S04 | LOOKUP(poisoned) → **DISSOLVE** | ModelSelector flips to Sonnet. Note fades at the agent node — never reaches the gate. **Gate greys to `--cream-30`.** Agent's refusal quote types in. Counter reads 0. *No amber anywhere on screen except the wordmark* |
| 52–62 | S05 | **WIDEN** | OutcomeSplit builds three columns. "UNDEFINED, not 100%" lands as display-l. 0/117 and 62/62 beside it |
| 62–82 | **S06** | LOOKUP(poisoned) → CLOSE → **ABSENCE** | Note renders. Agent's "already refunded" line. `close_case`. **Then nothing.** Spine stays `--line`. Timer runs `00:04 · 00:12 · 00:41`. MerchantPanel slides in with ✅ green. BalanceStrip pulses faintly on the unchanged ₹0. **Hold ~20% of scroll with no other motion** |
| 82–90 | S07 | **AUDIT-SWEEP** → **FLAG** | Amber sweep rises from the bottom of the spine, `t-sweep`. Two trusted-state questions answer in `mono`. FLAG lands on the empty spine: OBLIGATION UNDISCHARGED. Counter 39/39, 0 false alarms |
| 90–96 | S08 | **WIDEN** | Four FindingCards stagger in |
| 96–100 | S09 | — | Everything else clears. Closing statement alone on `--ground` |

### The Act IV hold — the hardest 20%

Twenty percent of the page's scroll with almost nothing moving is a real
risk: a judge may think it's broken and scroll past. Three safeguards:

1. **The timer is the metronome.** It advances so the viewer knows the page
   is alive and time is passing — which is exactly the anxiety we want.
2. **The merchant panel arrives mid-hold**, so there is one arrival to hold
   attention, and it is the wrong kind of good news.
3. **The balance pulse** is the only other motion: ~4s interval, very low
   amplitude, on the unchanged `₹0`.

If user testing shows people scroll past it, **shorten the hold — do not add
motion to it.** Filling the silence destroys the beat.
