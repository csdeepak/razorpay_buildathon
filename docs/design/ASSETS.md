# ASSETS.md — asset manifest

Per the playbook: every production asset has a known source and usage note,
and Claude implements approved asset IDs rather than inventing image URLs.

---

## Status: five storyboard panels delivered ✅

Generated 2026-08-22 from the prompts in `IMAGE-PROMPTS.md`, all five accepted
on the first or second attempt. Stored in `submission/demo/img/` as WebP and
inlined as data URIs at build time.

| File | Panel | Slot | Size |
|---|---|---|---:|
| `p1-asks.webp` | 1 — looking at the screen | Act 0 | 49 KB |
| `p2-note.webp` | 2 — the forged record | WIDEN 1 + Act IV strip | 22 KB |
| `p3-block.webp` | 3 — diverted and stopped | WIDEN 1 strip | 4 KB |
| — | 4 — **empty frame** | Act IV strip | 0 (CSS) |
| `p5-waits.webp` | 5 — closed laptop, waiting | Act IV strip | 48 KB |
| `p6-audit.webp` | 6 — the sweep | Act IV audit | 7 KB |

**The bookend worked.** Panels 1 and 5 are the same shot twice — same bench,
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
