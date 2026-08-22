# DESIGN.md — Warden demo surface

The implementation contract. Per the playbook, this is written **before** any
code and the codebase becomes an implementation of it, not a place where
design gets invented on the fly.

Upstream: `submission/demo-story.md` (story, fixed) →
`docs/design/SCREEN_MAP.md` (scenes/states) → **this file** (visual system)
→ code.

---

## 1. Product identity — the visual thesis

A dark, quiet instrument panel that watches money move. It should feel like
**evidence**, not marketing: precise, unhurried, faintly forensic. The page
earns trust by being legible and by volunteering its own failures, so the
design must never oversell — no triumphant greens, no celebratory motion, no
dashboard chrome implying more machinery than exists.

Five adjectives: **precise · warm-dark · forensic · restrained · unhurried.**

The one visual idea everything hangs on: **a vertical spine down which money
travels.** Every act is a variation on what happens to a token on that spine.
When the spine is empty, that means something.

---

## 2. References — and what is actually borrowed

**Primary: `razorpay.com/buildathon` (measured, not guessed).**

| Token measured on the reference | Value | Borrowed? |
|---|---|---|
| Page ground | `rgb(14, 11, 8)` | **Yes, exactly.** The connective tissue to Razorpay |
| Text | `rgb(240, 231, 214)` warm cream | **Yes** |
| Accent | `rgb(217, 163, 83)` amber | **Yes — but repurposed semantically, see §3** |
| Display face | Satoshi, 700, tracking to −0.04em | Character borrowed; **substituted**, see §4 |
| Micro-labels | 15px / 700 / +0.32em / uppercase | **Yes** |
| Section markers | Timestamps (`06:31`, `07:20`) | **Yes, adapted** — ours mark session elapsed time, which Act IV then weaponises |
| Two-tone headlines | cream word + amber word | **Yes** |
| Numbered sections | `01 02 03 04 05` | **Yes** |
| Photography | none at all | **Yes — we also use none.** See `ASSETS.md` |

**Deliberately NOT borrowed:** their copy voice (punchy recruitment-marketing)
is wrong for an evidence document. Ours is flatter and more clinical.

**Why lean this close to their language:** the submission is *for* Razorpay,
and a page that feels native to their surface signals attention to detail.
The risk is reading as derivative — mitigated because our information design
(spine, gate, audit rail, grid) is entirely our own. We share a palette and a
typographic temperature, not a layout.

---

## 3. Color — semantic, not decorative

Ground and text come straight from the reference. **The semantic layer is
ours, and the key decision is what amber means.**

```
--ground        #0E0B08   page background (Razorpay's exact warm black)
--surface       #17130E   raised panels, cards
--surface-2     #211A13   inset wells, the audit rail
--line          #2E2419   hairlines, spine when idle
--cream         #F0E7D6   primary text, and MONEY IN MOTION
--cream-80      rgba(240,231,214,.80)   secondary text
--cream-55      rgba(240,231,214,.55)   tertiary, captions
--cream-30      rgba(240,231,214,.30)   disabled, idle nodes
--amber         #D9A353   WARDEN ACTING — see below
--amber-dim     rgba(217,163,83,.18)    amber wash, gate glow
--danger        #EE7A6B   the attack: DIVERT, poisoned notes
--danger-dim    rgba(238,122,107,.13)
--settled       #7FA37A   money that safely ARRIVED (used sparingly, once per act at most)
```

### The load-bearing decision: **amber = Warden acting**

Razorpay's accent becomes our "the enforcement layer just did something"
colour. Every time Warden fires, blocks, writes an audit row, or raises a
flag, the page lights up in **Razorpay's own colour**. That is a quiet,
deliberate piece of positioning — and it makes Act III legible at a glance,
because Act III is *the act with no amber in it*.

Consequences that must hold:

- **A block is amber, not red.** The gate firing is good news. Red is
  reserved for the attack itself.
- **Act III has essentially no amber** except the wordmark. The absence of
  the brand colour *is* the message: Warden did nothing.
- **Green (`--settled`) is rationed.** It marks money arriving, and it marks
  the merchant's deceptive "case resolved" checkmark in Act IV — which is the
  only place on the page where green lies. That collision is intentional and
  is the strongest single colour moment in the piece.

### On the alarm red being brighter than it started

`--danger` was `#D9584A` (5.09:1 on the ground). Once Panel 1 became a large
ambient figure, the big red counters sitting over her fell to 2.4:1 against a
3:1 large-text floor. Brightening to `#EE7A6B` (7.13:1) bought the headroom
without shrinking the figure, and it improved every other use of the colour
too — poisoned-note text on `--surface` went 4.79 → 6.72.

It also surfaced a failure that predated the figure entirely: the diverted
token was cream text on a `--danger` fill at **3.14:1**, under the 4.5 it
needed. It is now `--ground` on `--danger` at 7.13:1, which also matches the
normal token's dark-on-light treatment.

### Contrast

Every text/background pair must clear **4.5:1**; display type at 32px+ may
sit at 3:1. `--cream-30` is for non-text ornament only, never for words a
reader needs.

---

## 4. Typography

Satoshi is the reference face but ships from Fontshare, and a published
Artifact can only load **Google Fonts**. Substituting rather than pretending:

| Role | Face | Why |
|---|---|---|
| Display + UI | **Plus Jakarta Sans** (400/500/700/800) | Closest Google Fonts match to Satoshi's geometric-humanist proportions and tight apertures |
| Data + evidence | **JetBrains Mono** (400/500/700) | Hashes, UPI handles, amounts, rule names, timestamps. Tabular figures are mandatory here |

Fallback stack on both: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
and `ui-monospace, "SF Mono", Consolas, monospace`.

### Scale (fluid, `clamp()`)

| Token | Size | Weight | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | clamp(44px, 6vw, 76px) | 800 | −0.04em | Act titles |
| `display-l` | clamp(32px, 4vw, 48px) | 700 | −0.03em | Beat headlines |
| `display-m` | clamp(24px, 2.6vw, 34px) | 700 | −0.025em | Sub-beats |
| `body-l` | 19px | 500 | −0.005em | Narrative prose |
| `body` | 16px | 400 | 0 | Everything else |
| `micro` | 13px | 700 | **+0.30em** uppercase | Section labels, act markers |
| `mono-l` | 20px | 500 | 0 | Amounts, counters |
| `mono` | 14px | 400 | 0 | Hashes, handles, rules |

**Never below 16px for body text** — this gets screen-recorded at 1080p
(playbook: screen-recording first).

### Two-tone headline rule

Borrowed from the reference: one word in `--amber`, the rest `--cream`. The
amber word must be **the semantically loaded one** — `caught`, `nothing`,
`undischarged` — never a random noun for decoration.

---

## 5. Spacing, layout, depth

- **Base unit 4px.** Spacing scale: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128.
- **Stage:** full viewport, `100dvh`, fixed. Content moves; the frame doesn't.
- **Grid:** 12-col, max content width 1280px, gutter 24px.
- **Zones** (see `SCREEN_MAP.md` for what occupies them):
  `chat` left ~30% · `spine` centre ~34% · `evidence` right ~30%.
- **Radii:** 0 for the spine and rails (structural, engineered), 8px for
  panels, 4px for chips, **9999px for the travelling token only** — the one
  round thing on the page is the money.
- **Depth:** no drop shadows. Elevation is expressed by surface lightness
  (`--ground` → `--surface` → `--surface-2`) and 1px `--line` borders.
  Playbook anti-pattern: no glassmorphism, no gradient fills as hierarchy.

---

## 6. Components

Minimum set. Anything not listed needs a reason.

| Component | Notes |
|---|---|
| `ActMarker` | Fixed left edge. `micro` label + elapsed timestamp, Razorpay-style. Current act in amber |
| `ChatBubble` | Two variants: `customer` (cream on `--surface`), `agent` (cream-80, no fill, hairline left border) |
| `OrderCard` | Flips open on LOOKUP. Has a `notes` slot — the **only** element that can render `--danger` text |
| `SpineNode` | Agent · Gate · Rail. States: `idle` · `active` · `firing` · `greyed` |
| `Token` | The travelling money. Carries amount + destination. The only pill-shaped element |
| `RuleChip` | `mono`, amber, appears on BLOCK. Never generic — always names the rule |
| `AuditRow` | `mono`, drops into the evidence rail, shows 8 chars of hash + chain link glyph |
| `Counter` | Large `mono-l` figure + Wilson interval in `cream-55` beneath. **Interval is not optional** |
| `BalanceStrip` | Fixed bottom-left. Rhea's balance. The thing that must change — or conspicuously not |
| `ModelSelector` | 3 segmented options. Persistent from Act III onward |
| `AttackGrid` | 8×3 cells, WIDEN 1. Cells: `explored` · `current` · `not-testable` (greyed, labelled) |
| `MerchantPanel` | Appears only in Act IV. Deliberately reassuring. Green checkmark |

**Explicitly not building:** modals, toasts, tooltips, breadcrumbs, tabs,
a nav bar, or any card that only contains a number and an icon.

---

## 7. Motion

Motion here has one job: **make causality visible.** If an animation doesn't
show something causing something else, cut it.

### Durations

| Token | ms | Use |
|---|---|---|
| `t-flip` | 120 | State changes on a node |
| `t-enter` | 240 | Element appears |
| `t-travel` | 520 | Token moves one spine segment |
| `t-beat` | 900 | The held pause at the gate before a verdict |
| `t-sweep` | 1400 | AUDIT-SWEEP rising |

### Easing

| Token | Curve | Use |
|---|---|---|
| `e-enter` | `cubic-bezier(.2,0,0,1)` | Things arriving |
| `e-exit` | `cubic-bezier(.4,0,1,1)` | Things leaving |
| `e-travel` | `cubic-bezier(.35,0,.25,1)` | Token on the spine — barely eased. Money doesn't glide |
| `e-wrong` | `cubic-bezier(.5,-0.3,.7,1.4)` | **DIVERT only.** Slight overshoot. Should feel incorrect |
| **BLOCK** | **none — `0ms`** | See below |

### The two motion rules that matter

**1. The block has no easing.** Everything on this page eases except the
gate. When Warden blocks, the token stops **dead** — zero duration, no
deceleration, no bounce. Deterministic controls should not feel soft. It is
the only hard stop in the piece and it should read as a wall.

**2. Never fill the silence.** In Act IV there is no spinner, no shimmer, no
"processing" state, no reassuring pulse on the spine. The dead spine is the
content. The only things permitted to move are the elapsed timer and the
merchant's green counter — both of which make the stillness worse.

### `prefers-reduced-motion`

Not a degraded experience — a different one. All travel becomes instant
state changes; the argument must survive completely with motion off. Act
IV's ABSENCE is then carried by the frozen timestamp and the balance, which
still works. **Test this; it is a real reading of the page, not a checkbox.**

---

## 8. Responsive

| Breakpoint | Behaviour |
|---|---|
| ≥1200px | Three zones side by side. The design target — this is what gets recorded |
| 768–1199px | Evidence rail collapses to a strip under the spine; chat narrows |
| <768px | Single column. Spine runs full-width, chat above it, evidence below. **The AttackGrid becomes horizontally scrollable inside its own container — the page body never scrolls sideways** |

Act structure and copy are identical at every width. No mobile-only cuts —
if a beat isn't worth showing on mobile it isn't worth showing.

---

## 9. Accessibility

- Every act is a `<section>` with a real heading; the page is readable as a
  document with CSS off.
- Scroll-driven animation is **progressive enhancement**. Content is in the
  DOM from load, not injected on scroll — a screen reader gets the whole
  argument in order.
- Colour never carries meaning alone: BLOCK shows the rule name, DIVERT shows
  the wrong account, ABSENCE shows an explicit "no action taken" line.
- Focus visible on the model selector and grid cells, `2px --amber` outline,
  2px offset. Grid is arrow-key navigable.
- Counters use `aria-live="polite"` when they change.
- Contrast floor 4.5:1 for text.

---

## 10. DO / DON'T

**DO**
- Let the ground be empty. Negative space is the reference's main device.
- Name the mechanism every time — `payee_scope`, not "blocked".
- Show the interval next to every rate.
- Keep amber rare, so it means something when it appears.

**DON'T**
- No stock photography (see `ASSETS.md`).
- No hooded-figure attacker — the attacker is text on a record. Drawing a
  person breaks the thesis that attacks arrive as data.
- No six-box architecture diagram with equal weight. Three layers are
  deliberately thin.
- No gradient, glass, or 3D as a substitute for hierarchy.
- No celebratory motion on a block. It is a normal Tuesday for the gate.
- No invented metrics, no fake sparklines, no dashboard chrome.
- No number without provenance — every figure traces to `eval/runs/`.
