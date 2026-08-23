# 0011 — Cross-lab evaluation: one adapter, and an honestly bounded claim

Date: 2026-08-23
Status: accepted (adapter built; runs executed 2026-08-23 — Findings 18 and 20)

## Context

Every number in `docs/eval-findings.md` came from three Claude models. The
project's sharpest claim — *every model resists diversion and fails 100% of
denial attacks* — therefore means **every Anthropic model**, and a reviewer is
entitled to ask the obvious question:

> Is the denial gap a property of agents, or a property of one lab's
> post-training?

That question currently has no answer, and it sits directly under Finding 11
and Finding 15, the two results the submission leans on hardest.

Budget context: `$63.73` of the `$74` Anthropic allocation is unspent, but
that allocation is not transferable. Cross-lab access needs either a different
free tier or out-of-pocket spend, and out-of-pocket spend is not available.

## Decision

### 1. One adapter for every non-Anthropic model

`eval/backends.py` puts a normalized interface in front of two wire formats.
The backend **owns its own message list**, and the agent loop drives it with
format-free verbs (`add_user_text`, `add_tool_results`, `complete`).
Normalizing the message history itself would have meant inventing a third
format and translating twice.

`OpenAICompatBackend` covers **both** OpenRouter and Google AI Studio, since
Google publishes an OpenAI-compatible endpoint. One adapter, every reachable
model. Routing is by model id: `claude-*` → Anthropic, `gemini-*` → Google,
`vendor/model` → OpenRouter.

### 2. The Anthropic path is a lift, not a rewrite

The pre-refactor loop produced every recorded result. `AnthropicBackend` is
that code moved, not changed, and `TestAnthropicPathUnchanged` pins the call
kwargs, the native `input_schema` tool format, the raw-content-block assistant
echo, and the `tool_result` message shape. If those move, the existing runs
stop being comparable and the cross-lab comparison is void before it starts.

### 3. Malformed tool arguments are a third outcome

Anthropic returns tool inputs pre-parsed. OpenAI-format returns
`function.arguments` as a **string**, and weaker models emit invalid JSON.
That is neither compromise nor resistance, and scoring it as either would
corrupt the headline number. It surfaces as `ToolCall.malformed` and is
counted separately as `malformed_tool_calls`. Crucially it is **not** recorded
as a proposed action.

### 4. Provider pinning, because quantization is a confound

OpenRouter routes to whichever host is available and hosts differ in
quantization. "The model failed" and "someone's 4-bit re-host failed" must not
be the same data point. `provider_order` pins routing with
`allow_fallbacks: false` — a hard failure beats a silent mid-run reroute — and
`ModelTurn.provider` records who actually served every call.

### 5. Rate limits are distinguishable from bad requests

`ModelBackendError` carries the status, with `is_rate_limit` (429) and
`is_out_of_credit` (402). A run that dies partway is not *less* data, it is
**biased** data: the cases that completed are whichever ones got through.
Finding 16 already records a forecast miss caused by prefix-vs-sample
reasoning; this is the same error with the headline number as its blast
radius, so the classification exists to make it impossible to ignore.

## What the free tier actually offers

Probed directly rather than assumed. Of 19 free tool-calling models on
OpenRouter, a cold first attempt with no load gave:

| Model | Result |
|---|---|
| `nvidia/nemotron-3-super-120b-a12b:free` | tool call fired, arguments parsed |
| `z-ai/glm-5.2:free` | HTTP 429 |
| `google/gemma-4-31b-it:free` | HTTP 429 |
| `thinkingmachines/inkling:free` | HTTP 403, agentic harnesses only |

One in four. The headline evaluation will not be run on that.

**Google AI Studio** is the answer instead: a free key, no billing account,
serving real Gemini rather than a community re-host — which removes the
quantization confound entirely for the one model that most needs to be
credible. NVIDIA Nemotron supplies a second free lab, and its 9B/30B/120B/550B
range adds a capability axis for free.

## The claim this supports — and the one it does not

Planned set: 3 Claude + Gemini + 2–3 Nemotron sizes = **three labs, 9B to
frontier.**

That supports: *"seven models, three labs, spanning 9B to frontier — 100%
denial failure, every one."*

It does **not** support *"every frontier model."* GPT-5.1 and Gemini 3.1 Pro
are ~$0.90 and ~$1.19 for the planned subset and remain unreachable without
out-of-pocket spend. The adapter keeps them a config change rather than a
rewrite, and the writeup must state the bound rather than imply the stronger
claim.

## Alternatives considered

**Run the headline on free OpenRouter models anyway.** Rejected — see the
probe table and §5.

**Skip cross-lab entirely.** Rejected: it leaves the single-lab confound
sitting under the project's best result.

**Reimplement the client per provider instead of a shared adapter.** Rejected —
per-lab SDK differences become a confound of their own. One code path for
every non-Anthropic model means differences observed are differences in the
model.

## Consequences

- Verified end-to-end against a real provider, not only the fake:
  Nemotron 120B via OpenRouter, provider recorded as `Nvidia`, 0 malformed
  calls, ~1.7–2.8k input / 0.8–1.1k output tokens per case — consistent with
  the Finding 16 measurements the cost forecast is built on.
- **Observed immediately: the same model, same prompt, ran twice gave
  opposite outcomes** — one `close_case` ("shows as delivered"), one correct
  `issue_refund`. n=1 is worthless here, exactly as Findings 3 and 6 recorded
  for Haiku. Multi-seed is *more* necessary for these models, not less, and
  the run plan must budget for it.
- `eval/fake_openai.py` scripts turns rather than simulating a model: what
  needs proving is that the adapter carries whatever a real provider returns,
  including the ugly cases.
- Tests: 47 → 83.
- **Runs executed 2026-08-23 — see Findings 18 and 20.** Widened the same day
  to every free tier that would serve tool calls: **32/32 denial leaks, 32/32
  detections, 0/32 false alarms** across eleven non-Anthropic models from five
  additional labs, **$0.00 spent**. Combined: **71/71 across fourteen models
  and six labs, 2.6B to frontier.** The narrative's `PENDING` marker is closed.
- **The capability spread turned out to be the load-bearing part.** Liquid's
  LFM 2.5 is 2.6B and NVIDIA's Nemotron Ultra is 550B — a 200x spread with an
  identical outcome, and no thinning at scale. That is the evidence separating
  a structural finding from a benchmark artifact.
- Gemini **Pro** proved unreachable on the free tier (20 requests/day/model),
  so the bound in §"The claim this supports" holds as written and tightened:
  the non-Claude models are Flash-tier and open-weight.
