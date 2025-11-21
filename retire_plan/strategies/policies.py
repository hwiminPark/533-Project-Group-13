"""
Withdrawal strategies for the retire_plan package.

Each strategy has the signature:
    strategy_xxx(state: dict[str, Any]) -> dict[str, float]

where state includes (at minimum):
- 'age'
- 'target_net_cash'
- 'cpp_income'
- 'oas_income'
- 'balances': dict with keys 'tax_deferred', 'tax_free', 'taxable'

Implementation details are left to Student C.
"""

from __future__ import annotations

from typing import Any, Dict


def strategy_spend_taxable_first(state: Dict[str, Any]) -> Dict[str, float]:
    """Strategy: spend from taxable account first, then others.

    Parameters
    ----------
    state : dict
        Current-year state, including target spending and account balances.

    Returns
    -------
    Dict[str, float]
        Withdrawal amounts by account:
        - 'tax_deferred'
        - 'tax_free'
        - 'taxable'

    Notes
    -----
    Student C: please implement the logic for this strategy.
    """
    raise NotImplementedError("strategy_spend_taxable_first() is not implemented yet.")


def strategy_spend_rrsp_first(state: Dict[str, Any]) -> Dict[str, float]:
    """Strategy: spend from tax-deferred (RRSP/RRIF) first, then others."""
    raise NotImplementedError("strategy_spend_rrsp_first() is not implemented yet.")


def strategy_smooth_with_tfsa(state: Dict[str, Any]) -> Dict[str, float]:
    """Strategy: use TFSA to smooth taxes and net cash flow over time."""
    raise NotImplementedError("strategy_smooth_with_tfsa() is not implemented yet.")

