# retire_plan/__init__.py
"""
retire_plan – Canadian Retirement Planning Simulation Package
"""

# Import key classes so users can do: from retire_plan import PersonProfile, Simulator, etc.
from .accounts.profile import PersonProfile
from .accounts.models import (
    AccountBase,
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
)
from .simulation.engine import Simulator
from .simulation.metrics import TaxCalculator
from .strategies.policies import (
    contrib_max_tfsa_first,
    contrib_max_rrsp_first,
    strategy_spend_taxable_first,
    strategy_spend_rrsp_first,
    strategy_smooth_with_tfsa,
)
from .strategies.analysis import summarize_results, compare_strategies

__all__ = [
    "PersonProfile",
    "AccountBase",
    "TaxDeferredAccount",
    "TaxFreeAccount",
    "TaxableAccount",
    "Simulator",
    "TaxCalculator",
    "contrib_max_tfsa_first",
    "contrib_max_rrsp_first",
    "strategy_spend_taxable_first",
    "strategy_spend_rrsp_first",
    "strategy_smooth_with_tfsa",
    "summarize_results",
    "compare_strategies",
]

__version__ = "0.1.0"