"""
strategies subpackage

Provides:
- Withdrawal strategy functions in policies.py
- Analysis / summary functions in analysis.py

Implementation is intentionally left to Student C.
"""


from .policies import (
    strategy_spend_taxable_first,
    strategy_spend_rrsp_first,
    strategy_smooth_with_tfsa,
)
from .analysis import (
    summarize_results,
    compare_strategies,
    income_profile_by_age,
)

__all__ = [
    "strategy_spend_taxable_first",
    "strategy_spend_rrsp_first",
    "strategy_smooth_with_tfsa",
    "summarize_results",
    "compare_strategies",
    "income_profile_by_age",
]
