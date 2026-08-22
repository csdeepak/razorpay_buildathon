# Image prompts — the storyboard strip

Five illustrations for the demo page. Generate these and hand them back; the
page has slots waiting.

---

## The rule that governs all five: comic **grammar**, not comic **aesthetics**

Deepak's instinct — comic-book interpretation for understandability — is
right, and it resolves the earlier no-photography decision rather than
contradicting it. But the distinction matters and it is easy to get wrong:

| Take this from comics | Leave this out |
|---|---|
| **Panels and gutters** — sequential frames reading left to right | Superhero rendering, dynamic foreshortening |
| **Closure** — the reader infers what happens *between* panels | Speech balloons with tails, sound effects |
| **Repeated framing** — the same shot, changed state | Halftone/Ben-Day dots as decoration |
| **The empty panel** — a frame where action should be and isn't | Bright primaries, cel shading, gloss |

A page whose entire claim is rigour cannot look like a cartoon. What we want
is closer to **technical storyboard / editorial line illustration** — the
register of an accident-investigation diagram, not a graphic novel.

**Why comics earn their place here:** the gutter between panels is literally
how sequential art expresses elapsed time and absence. That is precisely the
Act IV mechanic. Panel 4 below is *an empty frame*, and it will do more work
than any drawing on this page.

---

## Shared style spec — put this in every prompt

```
Flat two-tone technical line illustration in the style of an editorial
storyboard or accident-investigation diagram. Single-weight clean linework,
no gradients, no cel shading, no gloss. Warm near-black background #0E0B08.
Line work and figures in warm cream #F0E7D6. Restrained, forensic, calm.
Slight print grain acceptable. Generous negative space.
NO TEXT, NO LETTERING, NO SPEECH BUBBLES, NO WATERMARK, NO LOGOS.
Wide 16:9 composition.
```

**Accent rule — do not let the generator improvise colour.** Only one accent
appears per image, and only where the brief says so:
- amber `#D9A353` = the enforcement layer acting
- red `#D9584A` = the attack
- everything else stays cream on near-black

If a generator adds blues, greens, purples or a second accent, regenerate.
That palette discipline is the whole reason the page reads as one system.

---

## Panel 1 — Rhea asks
**Slot:** Act 0 · **Aspect:** 16:9

> Shared style spec, then:
>
> A young woman sits alone on a public park bench, seen from a low
> three-quarter angle at middle distance, small in the frame. An open laptop
> rests on her knees. Her posture is upright and expectant — she has just
> sent a message and is waiting for a reply. Sparse surroundings: the bench,
> a suggestion of pavement, one bare tree branch entering from the upper
> left. Wide empty space on the right two-thirds of the frame for text
> overlay. Cream linework on near-black. No accent colour in this panel at
> all.

**Why:** grounds the abstraction in a person before any machinery appears.
Note the empty right side — the headline sits there.

---

## Panel 2 — the forged note
**Slot:** Act II setup · **Aspect:** 16:9

> Shared style spec, then:
>
> A close-up of a stack of plain document cards or record sheets seen at a
> slight angle, drawn as clean flat linework. All cards are cream outline on
> near-black. One card in the middle of the stack is subtly different — it
> sits very slightly askew and is outlined in red #D9584A, as though slipped
> in by someone else. No text on any card; suggest lines of writing with
> simple horizontal rules. Nobody is present. Cold, procedural, evidentiary.

**Why:** the attacker's only physical presence in the entire piece is a
foreign record in a stack. Drawing a person here would break the thesis that
attacks arrive as data.

**Do not include:** a hooded figure, a hacker, a hand placing the card, a
skull, a padlock, any threat iconography.

---

## Panel 3 — the block
**Slot:** Act II payoff · **Aspect:** 16:9

> Shared style spec, then:
>
> A schematic diagram: a single strong vertical line running top to bottom
> through the centre of the frame, drawn like a rail or conduit. A small
> circular token travels down it. Partway down, the token has veered sharply
> off the vertical line to the right along a curved path drawn in red
> #D9584A — and has stopped dead against a horizontal barrier plate drawn in
> amber #D9A353 that spans the width of the diverted path. The token is
> pressed against the barrier, motionless. Clean draughtsman's linework,
> like a mechanical drawing. No people. Both accents appear here and only
> here.

**Why:** this is the one image that carries the mechanism. The red path is
the attack; the amber plate is the enforcement layer. Both accents together,
once.

---

## Panel 4 — the silence · **THE EMPTY PANEL**
**Slot:** Act IV · **Aspect:** 16:9

**Generate nothing.** This panel is an empty frame drawn in CSS: a thin cream
hairline rectangle on the near-black ground, the same dimensions as the other
four, containing nothing at all.

Placed fourth in a strip where the reader has learned that each frame carries
an event, an empty frame reads as *something has gone wrong* before a single
word explains it. That is comic closure doing the work, and no illustration
can beat it.

If you want one small mark inside it, the strongest option is a single
cream `₹0` in the mono face, bottom-left, and nothing else. Resist adding
more.

---

## Panel 5 — Rhea waits
**Slot:** Act IV coda · **Aspect:** 16:9

> Shared style spec, then:
>
> **The exact same composition, framing, camera angle and distance as Panel
> 1** — the same woman, the same bench, the same laptop, the same bare
> branch entering upper left, the same empty right two-thirds. The only
> differences: her posture has slackened slightly, she is looking away from
> the screen rather than at it, and the light is flatter. Everything else
> must match Panel 1 as closely as possible. Cream linework on near-black.
> No accent colour.

**Why:** repeated framing with a changed state is one of the oldest and most
effective devices in sequential art. The reader does not need to be told time
passed and nothing happened — the identical composition says it. **Generate
this from Panel 1's seed or as a variation of it**, so the match is close
enough that the difference reads as change rather than a different drawing.

---

## Panel 6 — the audit finds it *(optional)*
**Slot:** Act IV resolution · **Aspect:** 16:9

> Shared style spec, then:
>
> The same schematic vertical rail as Panel 3, but empty — no token anywhere
> on it. Rising from the bottom of the frame, a wide horizontal band of soft
> amber #D9A353 light sweeps upward across the diagram, illuminating the
> empty rail. Where the light meets the empty rail, a small amber bracket or
> caret marks the vacancy. Clean mechanical linework. No people, no red.

**Why:** the detective control must look and move differently from the gate.
The gate is a barrier across a path; this is a light revealing an absence.

---

## Delivery notes

- **PNG with transparent background** preferred — the page paints `#0E0B08`
  behind them, so transparency avoids a visible rectangle edge. Solid
  `#0E0B08` is an acceptable fallback.
- **~1600×900** is plenty. They render at roughly 600–760px wide.
- Name them `p1-asks.png`, `p2-note.png`, `p3-block.png`, `p5-waits.png`,
  `p6-audit.png` and drop them in `submission/demo/img/`.
- Each will be added to `ASSETS.md` with its generator and prompt before use,
  per the playbook's manifest rule.
- If a panel comes back busy, over-rendered or with a second accent colour,
  regenerate rather than accepting it. **Five restrained panels beat six
  decorated ones**, and Panel 4 — the one that costs nothing — is the most
  important of them.
