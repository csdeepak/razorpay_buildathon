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
}

# Sonnet 5 introductory pricing, through 2026-08-31 inclusive.
SONNET_5_INTRO = (2.00, 10.00)
SONNET_5_INTRO_LAST_DAY = date(2026, 8, 31)


def rates_for(model: str, on: date | None = None) -> tuple[float, float]:
    """Returns (input_per_1m, output_per_1m) for a model on a given date."""
    on = on or date.today()
    if model == "claude-sonnet-5" and on <= SONNET_5_INTRO_LAST_DAY:
        return SONNET_5_INTRO
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
