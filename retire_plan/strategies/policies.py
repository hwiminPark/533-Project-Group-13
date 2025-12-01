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


def _shortfall(state: Dict[str, Any]) -> float:
    """Compute remaining cash shortfall after CPP and OAS."""
    target = float(state.get("target_net_cash", 0.0))
    cpp = float(state.get("cpp_income", 0.0))
    oas = float(state.get("oas_income", 0.0))
    need = target - (cpp + oas)
    return max(need, 0.0)


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
    """
    balances = state.get("balances", {})
    remaining = _shortfall(state)

    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    # 1. withdraw from taxable first
    taxable_avail = float(balances.get("taxable", 0.0))
    from_taxable = min(remaining, taxable_avail)
    plan["taxable"] = from_taxable
    remaining -= from_taxable

    # 2. then tax-deferred (RRSP/RRIF)
    if remaining > 0:
        td_avail = float(balances.get("tax_deferred", 0.0))
        from_td = min(remaining, td_avail)
        plan["tax_deferred"] = from_td
        remaining -= from_td

    # 3. finally tax-free (TFSA)
    if remaining > 0:
        tf_avail = float(balances.get("tax_free", 0.0))
        from_tf = min(remaining, tf_avail)
        plan["tax_free"] = from_tf
        remaining -= from_tf

    return plan


def strategy_spend_rrsp_first(state: Dict[str, Any]) -> Dict[str, float]:
    """Strategy: spend from tax-deferred (RRSP/RRIF) first, then others."""
    balances = state.get("balances", {})
    remaining = _shortfall(state)

    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    # 1. withdraw from RRSP/RRIF first
    td_avail = float(balances.get("tax_deferred", 0.0))
    from_td = min(remaining, td_avail)
    plan["tax_deferred"] = from_td
    remaining -= from_td

    # 2. then taxable
    if remaining > 0:
        taxable_avail = float(balances.get("taxable", 0.0))
        from_taxable = min(remaining, taxable_avail)
        plan["taxable"] = from_taxable
        remaining -= from_taxable

    # 3. finally TFSA
    if remaining > 0:
        tf_avail = float(balances.get("tax_free", 0.0))
        from_tf = min(remaining, tf_avail)
        plan["tax_free"] = from_tf
        remaining -= from_tf

    return plan


def strategy_smooth_with_tfsa(state: Dict[str, Any]) -> Dict[str, float]:
    """Strategy: use TFSA to smooth taxes and net cash flow over time."""
    balances = state.get("balances", {})
    remaining = _shortfall(state)

    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    # 1. moderate RRSP withdrawal: 4% rule
    td_bal = float(balances.get("tax_deferred", 0.0))
    suggested = 0.04 * td_bal
    from_td = min(remaining, suggested, td_bal)
    plan["tax_deferred"] = from_td
    remaining -= from_td

    # 2. then taxable
    if remaining > 0:
        taxable_bal = float(balances.get("taxable", 0.0))
        from_taxable = min(remaining, taxable_bal)
        plan["taxable"] = from_taxable
        remaining -= from_taxable

    # 3. TFSA as flexible top-up
    if remaining > 0:
        tf_bal = float(balances.get("tax_free", 0.0))
        from_tf = min(remaining, tf_bal)
        plan["tax_free"] = from_tf
        remaining -= from_tf

    return plan
