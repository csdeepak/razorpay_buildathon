# ASSETS.md — asset manifest

Per the playbook: every production asset has a known source and usage note,
and Claude implements approved asset IDs rather than inventing image URLs.

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

- [ ] Build script: reduce the three run JSONs → `ui-data.json`
- [ ] Decide whether the Act 0 line illustration is wanted (default: no)
