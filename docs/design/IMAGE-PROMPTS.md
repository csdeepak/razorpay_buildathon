# Image prompts — the storyboard strip

Six slots, five images to generate. **Each prompt below is complete and
copy-pasteable** — paste the whole block into the generator as-is. Don't
summarise them; the length is doing work.

Status: **Panel 5 is done** (the first image generated reads as *waiting*, so
it belongs there — see that section). Everything else is outstanding.

---

## Before you generate anything

**The one rule that keeps the set coherent: one accent colour per image, and
only where the prompt asks for it.** Cream `#F0E7D6` linework on a
near-black ground is the default. Amber `#D9A353` means the enforcement
layer acting. Red `#D9584A` means the attack. If a generator adds blue,
green, teal, purple, or a glow it invented, **regenerate** — don't accept it
and don't try to fix it in post. That discipline is the entire reason the
page reads as one system rather than five pictures.

**Don't worry about matching the background hex.** The first image came back
on pure black rather than the page's warm `#0E0B08`. That's fine — the page
applies `mix-blend-mode: screen`, which drops black out completely and floats
only the cream linework on the page's own ground. Any near-black background
works. **Transparent PNG also works.** Do not spend re-rolls on this.

**Keep the composition anchor consistent.** In the two bench panels the
figure sits at roughly 25% from the left edge with a bare branch entering
from the upper left, and the right ~55% of the frame stays empty for text.
The three schematic panels should feel like they were drawn by the same hand
at the same scale — similar margins, similar line weight.

**Aspect ratio: 16:9 for all of them.** Roughly 1600×900 is plenty; they
render at 600–760px wide on the page.

**Seed discipline for the bench pair.** Panels 1 and 5 must be the *same
drawing in two states*. Generate one, then re-roll the other from the same
seed changing only the sentence describing her posture. If your generator
can't hold composition across a re-roll, use img2img / "vary (subtle)" on
the finished one instead.

---

## Panel 1 — Rhea asks
**Slot:** Act 0, the opening image · **Status:** to generate · **Pairs with Panel 5**

### Prompt

```
A minimalist black-and-white line-art illustration in the style of a
technical storyboard or editorial ink drawing. A young woman sits alone on a
wooden slatted park bench, positioned in the left quarter of a wide frame,
seen from a low three-quarter angle at middle distance so she reads as small
within a large empty scene. An open laptop rests on her knees and she is
looking down at its screen, head tilted slightly forward, both hands resting
on the keyboard, mid-message — engaged and focused on the screen, not looking
away from it. A bare leafless tree stands at the far left edge with thin
branches reaching across the upper-left corner of the frame. Beneath the
bench, a simple grid of paving stones recedes gently toward the lower right.
The entire right half of the image is completely empty negative space with
nothing in it. Drawn entirely in fine, constant-weight cream-white ink lines
on a near-black background. Pure outline work only: no shading, no
cross-hatching, no gradients, no fill, no texture, no colour of any kind.
Calm, quiet, restrained, forensic. Wide 16:9 composition.
```

### Negative prompt

```
text, letters, numbers, watermark, signature, logo, speech bubble, caption,
colour, coloured accents, blue, green, red, orange, purple, gradient,
shading, cross-hatching, painterly, watercolour, 3D render, photorealistic,
cartoon, anime, cel shading, glow, lens flare, busy background, crowd,
buildings, city skyline, phone, coffee cup, dog, other people
```

### Accept it if

She is unmistakably **looking down at the screen**. That single detail is
what distinguishes this from Panel 5, and the whole bookend device collapses
if she's gazing off into the distance in both.

---

## Panel 2 — the forged note
**Slot:** Act II, the setup · **Status:** to generate · **One accent: red**

This is the attacker's only physical presence in the entire piece. There is
no person in it, and that is deliberate: the thesis is that attacks arrive as
**data**, not as someone at a keyboard.

### Prompt

```
A minimalist black-and-white line-art illustration in the style of a
technical diagram or evidence photograph rendered as clean ink linework. A
neat stack of about eight plain rectangular document cards or record sheets,
viewed from a slightly elevated three-quarter angle, sitting centred-left in
a wide frame. Each card is drawn as a simple outlined rectangle in fine
constant-weight cream-white ink on a near-black background, with three or
four short horizontal rules inside suggesting lines of writing — no actual
text or legible characters anywhere. The cards are stacked squarely and
neatly, except for one single card roughly two-thirds of the way down the
stack which sits very slightly rotated and pushed a few millimetres out from
the others, as though it was inserted later by a different hand. That one
misaligned card, and only that card, is outlined in muted red #D9584A;
every other line in the image is cream-white. No people, no hands, no
furniture, no room. The right portion of the frame is empty negative space.
Pure outline work: no shading, no gradients, no fill, no texture. Cold,
procedural, evidentiary. Wide 16:9 composition.
```

### Negative prompt

```
text, letters, numbers, readable writing, watermark, signature, logo, person,
hand, hands, hooded figure, hacker, mask, skull, padlock, warning triangle,
virus, bug icon, shield, danger symbol, colour except muted red, blue, green,
orange, purple, gradient, shading, painterly, 3D render, photorealistic,
glow, dramatic lighting
```

### Reject it if

It contains **any** threat iconography — a hooded figure, a padlock, a skull,
a warning triangle, a shadowy hand placing the card. Every one of those
breaks the argument the page is making. The card is just slightly out of
line, and that is the whole point: it looks ordinary.

---

## Panel 3 — the block
**Slot:** Act II, the payoff · **Status:** to generate · **Two accents: red and amber**

This is the only image that carries the mechanism, and the only one where
both accents appear together.

### Prompt

```
A minimalist technical schematic diagram drawn as clean ink linework, in the
style of a mechanical or engineering drawing. A single strong vertical line
runs from the top edge to the bottom edge through the centre of a wide frame,
drawn in fine constant-weight cream-white ink on a near-black background,
representing a rail or conduit. Two small square nodes sit on this vertical
line, one near the top and one near the bottom, each drawn as a simple
outlined square. A small circular token, drawn as a clean outlined circle,
has left the vertical line at the midpoint and travelled outward to the right
along a smoothly curving path — that curved path is drawn in muted red
#D9584A. The token has come to a complete stop, pressed flat against a
horizontal barrier plate that blocks its way: a plain rectangular bar drawn
in warm amber #D9A353, oriented perpendicular to the token's path, spanning
enough width to clearly stop it. The token sits motionless against the
barrier, not passing it. Everything else in the image is cream-white
linework. Generous empty space around the diagram. No people, no machinery,
no arrows, no icons. Pure outline work: no shading, no gradients, no fill,
no glow. Precise, calm, diagrammatic. Wide 16:9 composition.
```

### Negative prompt

```
text, labels, letters, numbers, watermark, signature, logo, arrows,
arrowheads, icons, gears, machinery, robot, person, hand, glow, lens flare,
sparks, explosion, impact lines, motion blur, speed lines, gradient, shading,
3D render, isometric, perspective, photorealistic, cartoon, colour other than
muted red and warm amber, blue, green, purple
```

### Accept it if

You can read the causality without a caption: *something came down the line,
turned off it, and was stopped.* If the barrier looks decorative rather than
obstructive, or the token looks like it's passing through, re-roll.

---

## Panel 4 — the silence
**Slot:** Act IV · **Status:** GENERATE NOTHING

**This panel is deliberately empty and must stay that way.**

It's drawn in CSS: a thin cream hairline rectangle, identical in size to the
other panels, containing nothing. Optionally a single small cream `₹0` in the
monospace face in the lower-left corner, and nothing else.

Placed fourth in a strip where the reader has learned that every frame
carries an event, an empty frame says *something has gone wrong* before a
single word explains it. That's comic closure — the reader supplies the
meaning in the gutter — and no illustration can beat it.

**Do not generate an image for this slot.** If it feels too bare when you see
it in place, that feeling is the panel working.

---

## Panel 5 — Rhea waits
**Slot:** Act IV coda · **Status:** ✅ **DONE — the first image you generated**

The image already generated belongs here, not in Panel 1. She is looking away
from the screen, and that reads unmistakably as *waiting*, which is this
panel's entire job. It's a good drawing: correct line weight, no stray
colour, right negative space, good restraint.

**If you ever need to regenerate it**, or if the Panel 1 companion won't hold
the composition and you'd rather flip which is which:

### Prompt

```
A minimalist black-and-white line-art illustration in the style of a
technical storyboard or editorial ink drawing. A young woman sits alone on a
wooden slatted park bench, positioned in the left quarter of a wide frame,
seen from a low three-quarter angle at middle distance so she reads as small
within a large empty scene. A laptop rests on her knees but she is not
looking at it — her head is turned up and away toward the empty right side of
the frame, her shoulders slightly slack, her hands resting still and idle
rather than typing. Her posture reads as waiting for something that has not
come. A bare leafless tree stands at the far left edge with thin branches
reaching across the upper-left corner of the frame. Beneath the bench, a
simple grid of paving stones recedes gently toward the lower right. The
entire right half of the image is completely empty negative space. Drawn
entirely in fine, constant-weight cream-white ink lines on a near-black
background. Pure outline work only: no shading, no cross-hatching, no
gradients, no fill, no colour of any kind. Still, quiet, slightly deflated.
Wide 16:9 composition.
```

### Negative prompt

Same as Panel 1.

### The device, so it doesn't get lost

Panels 1 and 5 must be **the same shot twice**. Identical bench, identical
branch, identical camera, identical margins — only her state changes. The
reader doesn't need to be told that time passed and nothing arrived; the
repeated framing says it. If the two images don't match closely enough for
the repetition to register, the device fails and they're just two drawings of
a woman on a bench.

**Stronger alternative if gaze direction reads too subtly on the page:** give
her a **closed laptop** in Panel 5, hands resting on top of it. A closed
laptop is a much louder "nothing came" signal than a turned head, and it
survives being viewed small.

---

## Panel 6 — the audit finds it
**Slot:** Act IV resolution · **Status:** optional, generate last · **One accent: amber**

Only worth generating if the page feels like it needs it once the others are
in. The CSS sweep may already carry this beat.

### Prompt

```
A minimalist technical schematic diagram drawn as clean ink linework, in the
style of a mechanical or engineering drawing. A single strong vertical line
runs from the top edge to the bottom edge through the centre of a wide frame,
drawn in fine constant-weight cream-white ink on a near-black background,
with two small outlined square nodes on it — one near the top, one near the
bottom. The line is completely empty: nothing is travelling on it, and there
is no circular token anywhere in the image. Rising from the bottom edge of
the frame, a wide soft horizontal band of warm amber #D9A353 light sweeps
upward across the lower third of the diagram, as though something is scanning
the empty rail from below. Where the amber light meets the vertical line, a
single small amber bracket or caret marks a specific point on the line,
indicating an absence. Everything else is cream-white linework on near-black.
Generous empty space. No people, no barrier, no red, no arrows, no icons.
Pure outline work: no gradients except the soft amber band, no shading, no
fill. Quiet, investigative. Wide 16:9 composition.
```

### Negative prompt

```
text, labels, letters, numbers, watermark, signature, logo, arrows, icons,
person, hand, circular token, ball, sphere, barrier, wall, red, blue, green,
purple, explosion, glow burst, lens flare, 3D render, photorealistic,
cartoon, shading, cross-hatching
```

### Accept it if

It looks like a **different kind of action** from Panel 3. Panel 3 is a
barrier stopping a thing; this is a light revealing that a thing is missing.
If they look like the same mechanism in two colours, the distinction between
preventing and detecting — which is the whole architectural point — is lost.

---

## Delivering them

Drop finished files into `submission/demo/img/` with these exact names:

| File | Panel |
|---|---|
| `p1-asks.png` | 1 — looking at screen |
| `p2-note.png` | 2 — the forged record |
| `p3-block.png` | 3 — the block |
| `p5-waits.png` | 5 — waiting *(the one already generated)* |
| `p6-audit.png` | 6 — optional |

PNG, ~1600×900, transparent or any near-black background. Each gets recorded
in `ASSETS.md` with its generator and prompt before it goes on the page, per
the playbook's manifest rule.

**Five restrained panels beat six decorated ones.** If one comes back busy,
over-rendered, or carrying a colour it invented, re-roll it rather than
accepting it — and remember the most important panel in the strip is Panel 4,
the one that costs nothing to make.
