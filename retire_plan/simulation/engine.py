"""
Simulation engine for the retire_plan package.

Defines:
- StrategyFn type
- run_simulation() main function

Implementation is intentionally left to Student B.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from retire_plan.accounts import PersonProfile
from .tax_system import TaxSystem

# Strategy function type:
# input: state dict (current year info)
# output: plan dict with withdrawals by account
StrategyFn = Callable[[Dict[str, Any]], Dict[str, float]]


def run_simulation(
    profile: PersonProfile,
    tax_system: TaxSystem,
    strategy_fn: StrategyFn,
    target_net_cash: float,
) -> List[Dict[str, Any]]:
    """Run year-by-year retirement simulation.

    Parameters
    ----------
    profile : PersonProfile
        Person profile with age range, accounts, and CPP/OAS.
    tax_system : TaxSystem
        Tax system used to compute annual tax.
    strategy_fn : StrategyFn
        Withdrawal strategy function, operating on a state dict and
        returning a plan dict with keys:
        - 'tax_deferred'
        - 'tax_free'
        - 'taxable'
    target_net_cash : float
        Desired annual after-tax spending.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dicts, one per year. Each record should include at least:
        - 'age'
        - 'gross_income'
        - 'taxable_income'
        - 'tax_paid'
        - 'net_cash_flow'
        - 'end_balances' (dict with three account balances)

    Notes
    -----
    Student B: please implement the year-by-year loop here. This function
    should:
    - build the state dict for each year
    - call strategy_fn(state) to get withdrawals
    - apply growth, benefits, and tax
    - append annual results to the list
    """
    raise NotImplementedError("run_simulation() is not implemented yet.")

