"""
Analysis utilities for retire_plan strategies.

All functions operate only on the results list returned by run_simulation().
Implementation details are left to Student C.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def summarize_results(name: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute high-level summary metrics from a simulation result list.

    Expected result keys per year:
    - 'age'
    - 'gross_income'
    - 'taxable_income'
    - 'tax_paid'
    - 'net_cash_flow'
    - 'end_balances'

    Student C: implement summary calculations here (total tax, ruin age, etc.).
    """
    raise NotImplementedError("summarize_results() is not implemented yet.")


def compare_strategies(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare multiple strategy summaries.

    This may return, for example:
    - the name of the lowest-tax strategy
    - the highest-final-wealth strategy
    - any other comparison metrics Student C decides.

    Student C: implement comparison logic here.
    """
    raise NotImplementedError("compare_strategies() is not implemented yet.")


def income_profile_by_age(
    results: List[Dict[str, Any]],
) -> List[Tuple[int, float]]:
    """Extract a simple (age, net_cash_flow) profile from simulation results.

    Student C: implement how to transform the raw results into a sequence
    of (age, net_cash_flow) tuples.
    """
    raise NotImplementedError("income_profile_by_age() is not implemented yet.")
