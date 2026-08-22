"""Model pricing, so every eval run reports what it actually cost.

Budget is a hard constraint on this project ($74 of org credits, see
docs/eval-budget.md). An eval rig that doesn't report its own spend makes
that constraint impossible to manage.

Prices are USD per 1M tokens, as of 2026-08-22. NOTE the Sonnet 5 introductory
rate expires 2026-08-31 -- mid-project. Front-load Sonnet runs before then.
"""

from __future__ import annotations

from datetime import date

# (input_per_1m, output_per_1m)
STANDARD_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-fable-5": (10.00, 50.00),
    "claude-opus-4-8": (5.00, 25.00),
    # --- cross-lab arm (ADR 0011) ---
    # Free tiers are genuinely $0, and must record as $0. Falling through to
    # the Opus default would write a fabricated cost into the run file and
    # into docs/eval-budget.md, which is the one ledger that has to be exact.
    "gemini-3.7-flash": (0.0, 0.0),
    "gemini-3.6-flash": (0.0, 0.0),
    "gemini-3.5-flash": (0.0, 0.0),
    "gemini-3.1-flash-lite": (0.0, 0.0),
    "gemini-3.1-pro-preview": (0.0, 0.0),
    "nvidia/nemotron-3-super-120b-a12b:free": (0.0, 0.0),
    "nvidia/nemotron-3-ultra-550b-a55b:free": (0.0, 0.0),
    "nvidia/nemotron-3-nano-30b-a3b:free": (0.0, 0.0),
    "nvidia/nemotron-nano-9b-v2:free": (0.0, 0.0),
    # Paid OpenRouter models, listed so a future run prices correctly rather
    # than silently inheriting Opus rates. Not currently reachable -- see
    # docs/decisions/0011-cross-lab-evaluation.md.
    "openai/gpt-5.1": (1.25, 10.00),
    "openai/gpt-5-mini": (0.25, 2.00),
    "google/gemini-3.1-pro-preview": (2.00, 12.00),
    "meta-llama/llama-4-maverick": (0.20, 0.80),
}


def is_free(model: str) -> bool:
    return STANDARD_PRICING.get(model) == (0.0, 0.0) or model.endswith(":free")

# Sonnet 5 introductory pricing, through 2026-08-31 inclusive.
SONNET_5_INTRO = (2.00, 10.00)
SONNET_5_INTRO_LAST_DAY = date(2026, 8, 31)


def rates_for(model: str, on: date | None = None) -> tuple[float, float]:
    """Returns (input_per_1m, output_per_1m) for a model on a given date."""
    on = on or date.today()
    if model == "claude-sonnet-5" and on <= SONNET_5_INTRO_LAST_DAY:
        return SONNET_5_INTRO
    if model.endswith(":free"):
        return (0.0, 0.0)
    return STANDARD_PRICING.get(model, STANDARD_PRICING["claude-opus-5"])


def cost_usd(model: str, input_tokens: int, output_tokens: int, on: date | None = None) -> float:
    in_rate, out_rate = rates_for(model, on)
    return (input_tokens / 1_000_000) * in_rate + (output_tokens / 1_000_000) * out_rate


def estimate_run_cost(
    model: str,
    n_case_runs: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    on: date | None = None,
) -> float:
    """Forecast the cost of a planned run. Feed it the measured averages from
    a previous run's report rather than a guess -- see docs/eval-budget.md."""
    return cost_usd(model, avg_input_tokens * n_case_runs, avg_output_tokens * n_case_runs, on)
