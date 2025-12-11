"""
Person profile model for the retire_plan package.

Defines:
- PersonProfile: holds life horizon, government benefits (CPP/OAS),
  and three account objects (tax-deferred, tax-free, taxable).
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
    name : str
        Name or label for this profile (e.g., "Sage" or "Household A").
    current_age : int
        Starting age of the simulation (in years).
    end_age : int
        Ending age for the simulation (e.g., 95).
        Whether this is inclusive or exclusive is up to the simulation
        engine (e.g., simulate from current_age up to end_age - 1).
    tax_deferred : AccountBase
        Tax-deferred account (RRSP/RRIF/LIRA/LIF).
    tax_free : AccountBase
        Tax-free account (TFSA).
    taxable : AccountBase
        Taxable non-registered account.
    cpp_annual : float
        Baseline annual CPP benefit (in today's dollars).
    oas_annual : float
        Baseline annual OAS benefit (in today's dollars).
    """

    name: str
    current_age: int
    end_age: int

    tax_deferred: AccountBase
    tax_free: AccountBase
    taxable: AccountBase

    cpp_annual: float = 0.0
    oas_annual: float = 0.0

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

    def total_balance(self) -> float:
        """Total wealth across all three accounts."""
        balances = self.all_balances()
        return float(sum(balances.values()))

    def retirement_horizon(self) -> int:
        """Number of years in the simulation horizon.

        Returns
        -------
        int
            max(0, end_age - current_age)
        """
        diff = self.end_age - self.current_age
        if diff < 0:
            # 这里选择“防御性处理”：返回 0，而不是抛异常
            return 0
        return diff


    def annual_gov_benefits(self) -> float:
        """Total annual government pension income (CPP + OAS)."""
        return float(self.cpp_annual + self.oas_annual)

    def snapshot(self) -> Dict[str, float]:
        """Convenience method: one-line snapshot of this profile.

        Returns a flat dict that can be logged or turned into a DataFrame.
        """
        data: Dict[str, float] = {
            "current_age": float(self.current_age),
            "end_age": float(self.end_age),
            "cpp_annual": float(self.cpp_annual),
            "oas_annual": float(self.oas_annual),
        }
        data.update({f"balance_{k}": v for k, v in self.all_balances().items()})
        return data
