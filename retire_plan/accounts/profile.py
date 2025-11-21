"""
Person profile model for the retire_plan package.

Defines:
- PersonProfile: holds life horizon, government benefits (CPP/OAS),
  and three account objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .models import AccountBase


@dataclass
class PersonProfile:
    """Profile for a single retiree or household.

    Attributes
    ----------
    current_age : int
        Starting age of the simulation.
    end_age : int
        Ending age for the simulation (inclusive or exclusive depending
        on simulation design; see engine.run_simulation).
    cpp_annual : float
        Annual CPP benefit.
    oas_annual : float
        Annual OAS benefit.
    tax_deferred : AccountBase
        Tax-deferred account (RRSP/RRIF/LIRA/LIF).
    tax_free : AccountBase
        Tax-free account (TFSA).
    taxable : AccountBase
        Taxable non-registered account.
    """

    current_age: int
    end_age: int
    cpp_annual: float
    oas_annual: float

    tax_deferred: AccountBase
    tax_free: AccountBase
    taxable: AccountBase

    def all_balances(self) -> Dict[str, float]:
        """Return a dict of all account balances.

        Keys are exactly:
        - 'tax_deferred'
        - 'tax_free'
        - 'taxable'
        """
        return {
            "tax_deferred": self.tax_deferred.balance,
            "tax_free": self.tax_free.balance,
            "taxable": self.taxable.balance,
        }

    def retirement_horizon(self) -> int:
        """Number of years in the simulation horizon."""
        return max(0, self.end_age - self.current_age)

    def total_balance(self) -> float:
        """Total wealth across all three accounts."""
        balances = self.all_balances()
        return sum(balances.values())
