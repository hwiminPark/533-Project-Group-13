"""
simulation subpackage – Core engine and metrics.

Exports:
    Simulator
    TaxCalculator
    calculate_shortfall_years
    project_tax_efficiency
"""

from .engine import Simulator
from .metrics import (
    calculate_shortfall_years,
    project_tax_efficiency,
)

__all__ = [
    "Simulator",
    "TaxCalculator",
    "calculate_shortfall_years",
    "project_tax_efficiency",
]