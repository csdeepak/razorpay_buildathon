# 0001 — Gate 0 resolved: World A, five real tracks, pre-built work required

Date: 2026-08-21
Status: locked

## Context

Everything the campaign knew about the Buildathon's actual mechanics came
from a single third-party X post, never verified against the primary page
(`docs/context/transfer.md` §3). Every prior automated attempt to read
`razorpay.com/buildathon/` (WebFetch, an earlier disconnected Chrome
extension attempt) returned only SEO metadata — the page is a scroll-animated
client-rendered single-page site. This blocked problem scoring from being
grounded in real constraints and left World A/B/C (see
`docs/gate-0-tracker.md`) unresolved, which is the single biggest risk named
in `docs/context/Razorpay_16_Day_Battle_Plan.md` §2.

## Decision

Opened the live page with a real browser session and its linked Google Form.
All six original gate-0 questions are now answered (full detail in
`docs/gate-0-tracker.md`). The load-bearing findings:

1. **World A is confirmed**, not assumed. The application form requires a
   public GitHub repo URL and a finished 5-minute pitch video *at the time of
   applying* — there is no post-selection build phase. Pre-built work is
   mandatory, not merely permitted.
2. **Five tracks exist, not one:** AI Growth & Agentic Commerce, AI Risk
   Manager, AI Revenue Recovery, AI Finance Controller, Open Track. Only the
   first was previously known.
3. **Track 01 grants Razorpay test-mode API access** explicitly; no other
   track mentions sandbox access, and no track mentions Agent Studio or
   Vulcan access.
4. **Solo application**, based on the form's individual-only field structure
   (full name, one college, one resume, no teammate field).
5. Deadline "5 September" confirmed in wording, but with **no time-of-day or
   timezone published** — treat as inferred, not verified.

## Alternatives considered

None — this was fact-finding, not a design choice with tradeoffs. The only
judgment call was how far to go into the actual Google Form: stopped after
page 1 (About You) rather than paging through with placeholder data, to avoid
entering data into an official application form under an assumed identity.
That means the "solo" answer (§6) rests on the buildathon page's own itemized
list plus form page 1, not a full form walkthrough — treated as high-
confidence, not certain.

## Consequences

- The 16-day plan's overall structure (`docs/context/Razorpay_16_Day_Battle_Plan.md`)
  needed no rework — it already assumed World A.
- Day 2–3 problem scoring (`docs/context/Razorpay_Landscape_and_Problem_Scoring.xlsx`)
  should now be weighed against the five *named* tracks and their stated
  bars, not against a hypothetical single track. In particular, Track 01's
  bar language ("explainable, bounded and gated," "audit trail," "one
  failure handled gracefully") reads close to the already-scored
  prompt-injection-defence / policy-enforcement-gateway / verifiable-intent
  candidates — a real signal for the Day 3 cut, not a pre-lock. The actual
  problem lock still happens at Gate 2 (Day 5), after real conversations.
- Because Track 01 is the only track with confirmed sandbox access, choosing
  a different track means committing to fully mocked or self-constructed
  data (Track 02–04 imply synthetic/held-out datasets by design).
- `docs/gate-0-tracker.md` status is now RESOLVED; `docs/progress-tracker.md`
  updated accordingly.
