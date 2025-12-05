"""
strategies.policies – All contribution and withdrawal strategies in one place
"""

from __future__ import annotations

from typing import Dict, Any


# ========================
# CONTRIBUTION STRATEGIES
# ========================
def contrib_max_tfsa_first(state: Dict[str, Any]) -> Dict[str, float]:
    """Maximize TFSA → RRSP → Taxable."""
    avail = state["annual_savings_available"]
    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    # TFSA first
    to_tfsa = min(avail, 7500)  # 2025 limit
    plan["tax_free"] = to_tfsa
    avail -= to_tfsa

    # Then RRSP
    to_rrsp = min(avail, 35000)
    plan["tax_deferred"] = to_rrsp
    avail -= to_rrsp

    plan["taxable"] = avail
    return plan


def contrib_max_rrsp_first(state: Dict[str, Any]) -> Dict[str, float]:
    """Maximize RRSP → TFSA → Taxable."""
    avail = state["annual_savings_available"]
    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    to_rrsp = min(avail, 35000)
    plan["tax_deferred"] = to_rrsp
    avail -= to_rrsp

    to_tfsa = min(avail, 7500)
    plan["tax_free"] = to_tfsa
    avail -= to_tfsa

    plan["taxable"] = avail
    return plan


# ========================
# WITHDRAWAL STRATEGIES
# ========================
def _shortfall(state: Dict[str, Any]) -> float:
    target = float(state.get("target_net_cash", 0))
    cpp = float(state.get("cpp_income", 0))
    oas = float(state.get("oas_income", 0))
    return max(target - (cpp + oas), 0)


def strategy_spend_taxable_first(state: Dict[str, Any]) -> Dict[str, float]:
    remaining = _shortfall(state)
    balances = state.get("balances", {})
    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    # 1. Taxable
    from_taxable = min(remaining, balances.get("taxable", 0))
    plan["taxable"] = from_taxable
    remaining -= from_taxable

    # 2. Tax-deferred
    if remaining > 0:
        from_td = min(remaining, balances.get("tax_deferred", 0))
        plan["tax_deferred"] = from_td
        remaining -= from_td

    # 3. Tax-free
    if remaining > 0:
        plan["tax_free"] = min(remaining, balances.get("tax_free", 0))

    return plan


def strategy_spend_rrsp_first(state: Dict[str, Any]) -> Dict[str, float]:
    remaining = _shortfall(state)
    balances = state.get("balances", {})
    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    from_td = min(remaining, balances.get("tax_deferred", 0))
    plan["tax_deferred"] = from_td
    remaining -= from_td

    from_taxable = min(remaining, balances.get("taxable", 0))
    plan["taxable"] = from_taxable
    remaining -= from_taxable

    if remaining > 0:
        plan["tax_free"] = min(remaining, balances.get("tax_free", 0))

    return plan


def strategy_smooth_with_tfsa(state: Dict[str, Any]) -> Dict[str, float]:
    remaining = _shortfall(state)
    balances = state.get("balances", {})
    plan = {"tax_deferred": 0.0, "tax_free": 0.0, "taxable": 0.0}

    td_bal = balances.get("tax_deferred", 0)
    from_td = min(remaining, 0.04 * td_bal, td_bal)
    plan["tax_deferred"] = from_td
    remaining -= from_td

    if remaining > 0:
        plan["taxable"] = min(remaining, balances.get("taxable", 0))
        remaining -= plan["taxable"]

    if remaining > 0:
        plan["tax_free"] = min(remaining, balances.get("tax_free", 0))

    return plan