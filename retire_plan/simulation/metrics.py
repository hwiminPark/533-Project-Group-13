"""
simulation.metrics – Tax calculator + simulation metrics in one file
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TaxCalculator:
    """Realistic Canadian tax model for retirement planning (2025 brackets)."""
    province: str = "ON"

    # Federal brackets (approx 2025)
    FEDERAL_BRACKETS = [
        (0, 57_000, 0.15),
        (57_000, 114_000, 0.205),
        (114_000, 177_000, 0.26),
        (177_000, 246_000, 0.29),
        (246_000, float("inf"), 0.33),
    ]

    PROVINCIAL_RATES = {
        "ON": 0.115, "BC": 0.105, "QC": 0.185, "AB": 0.12, "MB": 0.13,
        "SK": 0.125, "NS": 0.14, "NB": 0.14, "NL": 0.14, "PE": 0.14,
    }

    def effective_rate(self, taxable_income: float) -> float:
        if taxable_income <= 0:
            return 0.0
        federal_tax = 0.0
        remaining = taxable_income
        prev = 0
        for low, high, rate in self.FEDERAL_BRACKETS:
            bracket_size = high - max(low, prev)
            if remaining <= 0:
                break
            taxable_in_bracket = min(remaining, bracket_size)
            federal_tax += taxable_in_bracket * rate
            remaining -= taxable_in_bracket
            prev = high

        provincial_rate = self.PROVINCIAL_RATES.get(self.province, 0.12)
        provincial_tax = taxable_income * provincial_rate
        total_tax = federal_tax + provincial_tax
        return total_tax / taxable_income

    def tax_on(self, taxable_income: float) -> float:
        return taxable_income * self.effective_rate(taxable_income)


# Metrics functions
def calculate_shortfall_years(net_worth_history: list[float], target: float) -> int:
    return sum(1 for nw in net_worth_history if nw < target)


def project_tax_efficiency(total_tax: float, total_withdrawn: float) -> float:
    return total_tax / total_withdrawn if total_withdrawn > 0 else 0.0