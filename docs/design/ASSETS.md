# ASSETS.md — asset manifest

Per the playbook: every production asset has a known source and usage note,
and Claude implements approved asset IDs rather than inventing image URLs.

---

## Status: five panels generated, one used ✅

Generated 2026-08-22 from the prompts in `IMAGE-PROMPTS.md`, all five accepted
on the first or second attempt. Stored in `submission/demo/img/` as WebP and
inlined as data URIs at build time.

| File | Panel | Slot | Size |
|---|---|---|---:|
| `p1-asks.webp` | 1 — looking at the screen | **persistent ambient ground, ~58% of viewport** | 49 KB |
| `p2-note.webp` | 2 — the forged record | generated, not used | 22 KB |
| `p3-block.webp` | 3 — diverted and stopped | generated, not used | 4 KB |
| — | 4 — **empty frame** | **Act IV strip** | 0 (CSS) |
| `p5-waits.webp` | 5 — closed laptop, waiting | generated, not used | 48 KB |
| `p6-audit.webp` | 6 — the sweep | generated, not used | 7 KB |

### Panel 1 is now a persistent ground, not a scene figure

Rhea appears in **every act** — which was the story's own rule from the start
(`submission/demo-story.md`: "she is the continuity; the models change around
her"). Making her a fixed background rather than an Act 0 illustration is the
literal implementation of that rule, and it retired the need for Panel 5:
her constant presence plus a frozen `₹0` carries "she is never paid" without
a second drawing.

**Tuned against contrast, not taste.** She sits behind the prose column, so
the binding constraint is secondary text at 55% cream — 13px labels and the
Wilson intervals, which have far less headroom than a headline. Measured
across all ten scenes at 1440px:

| Setting | Worst text ratio | Verdict |
|---|---|---|
| opacity .30, fade to 62% | 2.45 | badly failing |
| opacity .22, fade to 52% | 4.45 | failing by a hair |
| opacity .17, fade to 52%, captions to 80% cream | 4.74 | passed, but small |
| opacity .34, 72vw, radial mask | 4.01 | too hot |
| **opacity .25, 80vw, radial mask, lifted text ladder** | **3.72\*** | **passes — final** |

\* 3.72 is against a **3:1** floor (56px counters); every small-text element
clears 4.5. Getting there took three coupled changes rather than one: the
text ladder lifted to 100 / 90 / 78 % cream so secondary text had room to
give, the alarm red brightened to `#EE7A6B`, and the radial mask retuned so
it reaches zero exactly at the spine's left edge — the mechanism column and
evidence rail are completely untouched by the figure.

The horizontal mask reaches zero well before the spine, so the mechanism
column and the evidence rail are completely unaffected — measured mask alpha
is 0 at the spine's left edge.

### Three of six were cut, and the page is better for it

Panels 2, 3 and 6 were generated, wired in, seen in place, and removed on
Deepak's call. The pattern behind all three cuts is the same and worth
stating, because it generalises: **each illustrated a beat the page was
already animating live.** Panel 3 drew a token diverting and being stopped
next to a spine that does exactly that in motion; Panel 6 drew a sweep beside
a live sweep; Panel 2 drew a record next to the poisoned note rendered as
real text. A still picture of a thing happening argues less well than the
thing happening.

Panel 6 also exposed a bug: `has-fig` hides the spine rail, so the
illustrated version left the CSS sweep rising over nothing.

**What survived is what the animation genuinely could not do** — the two
bench panels. A person is not a state machine and the spine cannot draw her.
That is the honest test for any future panel: if the page can animate it, it
should, and the illustration should be cut.

All six files stay in `submission/demo/img/` in case stills are wanted for
the deck or the pitch video. Only `p1` and `p5` are inlined at build time;
the page dropped 269 KB → 193 KB.

**The bookend is now the whole storyboard.** Panels 1 and 5 are the same shot twice — same bench,
tree, paving, camera and figure — differing only in that her laptop is open
and she's looking down at it in Panel 1, and closed with her hands resting on
it in Panel 5. The closed laptop was the stronger of the two options
considered; it survives being viewed small in a way a turned head does not.

### Two processing decisions worth recording

**Screen blending instead of hex-matching.** The generator returned pure
black backgrounds rather than the page's warm `#0E0B08`. Rather than burn
re-rolls chasing the exact ground colour, the page composites every panel
with `mix-blend-mode: screen`, which discards dark pixels entirely and floats
only the linework on the page's own ground. Any near-black or transparent
background now works, for these and any future panel.

**5.08 MB → 130 KB, with no visual cost.** The panels arrived as
truecolour PNGs carrying film grain across their large black fields — noise
that compresses terribly and that `screen` throws away anyway. Crushing
everything below luminance 34 to true black, resizing to 1280px and
quantising to a 32-colour palette without dithering gives a 97% reduction.
Dithering was tried first and made things *worse*: it scatters noise across
exactly the flat areas that should compress to nothing. Verified afterwards
that peak luminance is still 255 and the per-panel colour signatures survive
(p6 reads amber, p3 warm, p1/p5 neutral cream).

---

## Decision: this page uses no photography

The playbook's own test is *"determine whether imagery materially improves
comprehension or brand perception"* and *"do not use imagery merely to fill
empty space."* Applying it honestly:

| Argument | Verdict |
|---|---|
| The reference (`razorpay.com/buildathon`) uses **zero photography** — pure type and motion on warm black | Matching it is both on-brand and the stronger design |
| A stock photo of a person at a laptop is the most generic image on the internet | It would cheapen a page whose whole claim is rigour |
| Every other element is measured data | A decorative photo is the one unfalsifiable thing on the page |
| Licensing/attribution pipeline (Unsplash/Pexels API, manifest, credits) | Real cost, zero return here |

**So: no Unsplash, no Pexels, no asset-fetch step.** This removes a whole
workstream the playbook would otherwise require.

### On the "person on a bench with a laptop"

Deepak's original instinct was to open on a person on a bench — to ground the
abstraction in a human. **The instinct is right and is preserved**; only the
execution changes.

Rhea is made present through:

- her message, typed in, in her own words
- her name and account handle, `upi:rmehta@okaxis`
- **her balance**, fixed bottom-left, present in every single act

A balance that reads `₹0` for twenty percent of the page is a more affecting
image of a person than a stock photograph of a stranger. It is also the one
element the entire narrative resolves around.

**If a human figure is still wanted**, the fallback is a commissioned or
self-drawn single-weight line illustration in `--cream-30`, used once in Act
0 and never again — not a photograph. That would be added here as an asset
with a source note before use.

---

## Approved assets

```json
[
  {
    "id": "font-display",
    "type": "webfont",
    "family": "Plus Jakarta Sans",
    "weights": [400, 500, 700, 800],
    "source": "Google Fonts",
    "source_url": "https://fonts.google.com/specimen/Plus+Jakarta+Sans",
    "license": "SIL Open Font License 1.1",
    "usage": "display, UI, body",
    "note": "Substitute for Satoshi, which the reference uses but ships from Fontshare. A published Artifact can only load Google Fonts.",
    "status": "approved"
  },
  {
    "id": "font-mono",
    "type": "webfont",
    "family": "JetBrains Mono",
    "weights": [400, 500, 700],
    "source": "Google Fonts",
    "source_url": "https://fonts.google.com/specimen/JetBrains+Mono",
    "license": "SIL Open Font License 1.1",
    "usage": "hashes, UPI handles, amounts, rule names, timestamps",
    "note": "Tabular figures required for the balance and counters.",
    "status": "approved"
  },
  {
    "id": "data-ui",
    "type": "data",
    "source": "eval/runs/*.json",
    "usage": "every number, quote and outcome on the page",
    "note": "Reduced at build time into a single ui-data.json. Raw runs are gitignored and too large to embed. See SCREEN_MAP.md section H.",
    "status": "build-step-required"
  }
]
```

**Icons:** none from a library. The handful of marks needed — chain link,
checkmark, arrow, flag — are inline SVG paths drawn to match the 1px hairline
weight of `--line`. Importing Lucide for four glyphs is not worth the weight
or the visual mismatch.

---

## Outstanding

- [x] Build script: reduce the three run JSONs → `ui-data.json`
- [x] Act 0 illustration — resolved by the storyboard panels above, which are
      line illustration rather than photography and therefore never triggered
      the licensing pipeline this document exists to avoid.
