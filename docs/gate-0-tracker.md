# Gate 0 — Buildathon Mechanics (blocks everything)

Source: `docs/context/transfer.md` §3 for the original six questions.
**Resolved 2026-08-21** by opening `razorpay.com/buildathon/` directly in a
real browser (a scroll-animated single-page site — automated fetch tools had
previously only ever returned SEO metadata) and the linked Google Form
(`forms.gle/d9r2gvxp8cmoZhon9`, "Razorpay AI Builder Internship 2026").

Status: **RESOLVED** — see `docs/decisions/0001-gate-0-resolved.md` for the
full decision record. Answers below are the source data that ADR is built on.

## The six questions — answered

- [x] 1. **Deadline:** "Applications close 5 September." No time-of-day or
      timezone stated anywhere on the page or the form. Treat as end-of-day
      IST (Razorpay is Bangalore-based) but this specific detail is
      **inferred, not confirmed** — don't bet the last hour on it.
- [x] 2. **Full track list (all 5, previously only 1 was known):**
      1. **AI Growth & Agentic Commerce** — grow merchant revenue or make a
         merchant transactable by an AI buyer, on **Razorpay test-mode APIs**.
         Bar: "every money action explainable, bounded and gated," show the
         audit trail and one failure handled gracefully.
      2. **AI Risk Manager** — detector/verifier/auto-responder for one class
         of fraud/returns/chargeback loss, measured precision/recall on a
         held-out test set. **Strictly defense-only — offense-capable work is
         disqualified.**
      3. **AI Revenue Recovery** — detect revenue at risk (failed payments,
         abandoned checkout, overdue receivables) and execute a bounded
         recovery workflow. Bar: measured money recovered across a batch,
         compliant escalation, stopping rules, audit trail.
      4. **AI Finance Controller** — close one finance-ops loop (reconciliation,
         settlement Q&A, forecasting) over a 50+ record synthetic batch,
         report match rate and unresolved exceptions.
      5. **Open Track** — any real problem, meaningful use of AI, same bar
         for execution/reliability/depth.
- [x] 3. **Submission format — confirmed, not a repo/video/deck choice, it's
      all of them plus specifics:** apply via a Google Form asking for 12
      things — full name, college, graduation year, in-person-from-September
      yes/no, 6-or-12-month preference, resume file, chosen track, project
      name, what it solves, **public GitHub repo URL**, **5-minute pitch
      video (unlisted is fine)**, and "what broke, and how you got out."
      Explicitly stated: **"the last one is the one we read first."**
- [x] 4. **Pre-built-work rule — resolved, and it resolves World A/B/C
      outright:** the application form itself asks for a public repo URL and
      a finished pitch video *at the time of applying*. There is no separate
      "build after selection" phase — you cannot fill out this form without
      already having a working, demoed project. Pre-built work isn't just
      allowed, it's required.
- [x] 5. **Sandbox access:** confirmed for Track 01 specifically — "Razorpay
      test-mode APIs" named explicitly in that track's brief. Not stated for
      tracks 2–4 (Risk Manager, Revenue Recovery, Finance Controller name
      "synthetic data" / "held-out test set," implying you bring or construct
      your own datasets rather than hitting live Razorpay endpoints). No
      mention of Agent Studio or Vulcan access anywhere — assume no access
      to either.
- [x] 6. **Team or solo:** everything on the page and the form's first page
      ("Full name," "College," one resume) is singular, individual framing.
      No team-size or teammate field anywhere in the 12 listed form items.
      **Solo**, with reasonable confidence — only page 1 of the actual form
      was inspected directly (didn't proceed further to avoid entering data
      into an official application form), but the buildathon page's own
      itemized 12-question list corroborates it independently.

## Which world are we in?

**World A, confirmed.** Apply by 5 September with a working project already
built, repo public, video recorded. The 16-day build plan in
`docs/context/Razorpay_16_Day_Battle_Plan.md` is correct as originally
scoped — no rework needed on structure, only on target-track alignment (see
the ADR).

## New information the original six questions didn't anticipate

- **Judging rubric, stated explicitly:** problem taste, build quality, AI
  judgment ("the right tool in the right place, and where you chose not to
  use one"), and failure recovery. This maps closely onto the plan's existing
  emphasis on evaluation and honest scope-cutting.
- **The offer is fixed, not competitive:** ₹75,000/month confirmed exactly
  (matches the previously-unconfirmed X post), 6 or 12 months (applicant's
  choice, not Razorpay's), in-person Bangalore from September.
- **Track 01's bar language ("explainable, bounded, gated," "audit trail,"
  "one failure handled gracefully") reads as a close match to the
  prompt-injection-defence / policy-enforcement-gateway / verifiable-intent
  candidates already scored in `docs/context/Razorpay_Landscape_and_Problem_Scoring.xlsx`**
  — worth weighing during Day 2/3 problem scoring, not a decision made here.
  Track 02 (defense-only fraud/risk) is a plausible secondary fit for a
  narrower framing. This is an observation for Deepak's own scoring pass, not
  a pre-lock of the problem.

## Once resolved — done

1. ~~Fill in the checkboxes and answers above.~~ Done.
2. ADR written: `docs/decisions/0001-gate-0-resolved.md`.
3. `docs/progress-tracker.md` updated with the confirmed deadline.
