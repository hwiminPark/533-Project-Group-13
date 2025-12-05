"""
retire_plan – A modular retirement planning simulation package.

Subpackages
-----------
accounts     : Account models (RRSP, TFSA, Taxable) + PersonProfile
simulation   : Core engine, tax calculator, metrics
strategies   : Withdrawal policies and analysis tools

Quick start example
-------------------
>>> from retire_plan import create_demo_profile, run_demo
>>> run_demo()
"""

from __future__ import annotations

# Make the most common things available at package level
from retire_plan.accounts import (
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
    PersonProfile,
)
from retire_plan.strategies.policies import (
    strategy_spend_taxable_first,
    strategy_spend_rrsp_first,
    strategy_smooth_with_tfsa,
)

__version__ = "0.1.0"
__all__ = [
    "TaxDeferredAccount",
    "TaxFreeAccount",
    "TaxableAccount",
    "PersonProfile",
    "strategy_spend_taxable_first",
    "strategy_spend_rrsp_first",
    "strategy_smooth_with_tfsa",
    "create_demo_profile",
    "run_demo",
]


# ------------------------------------------------------------------
# Helper functions that live at top level for easy demo access
# ------------------------------------------------------------------
def create_demo_profile() -> PersonProfile:
    """Realistic profile starting at age 30 with modest savings."""
    return PersonProfile(
        name="Alex & Taylor (Age 30 Start)",
        current_age=30,      # ← NOW STARTS AT 30
        end_age=96,
        tax_deferred=TaxDeferredAccount("RRSP", balance=50_000, annual_return=0.07),
        tax_free=TaxFreeAccount("TFSA", balance=20_000, annual_return=0.07),
        taxable=TaxableAccount("Non-registered", balance=10_000, annual_return=0.07),
        cpp_annual=15_000,
        oas_annual=8_184,
    )


def run_demo() -> None:
    """Run the full demo (identical to demo_runner.py)."""
    from retire_plan.demo_runner import main
    main()
