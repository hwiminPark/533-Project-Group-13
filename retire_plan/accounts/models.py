"""
Account models for the retire_plan package.

Defines:
- AccountBase: abstract base class
- TaxDeferredAccount: e.g., RRSP/RRIF/LIRA/LIF (fully taxable withdrawals)
- TaxFreeAccount: e.g., TFSA (withdrawals not taxable)
- TaxableAccount: non-registered account (simplified tax treatment for now)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass
class AccountBase(ABC):
    """Abstract base class for all account types.

    Attributes
    ----------
    name : str
        Human-readable account name.
    balance : float
        Current account balance (dollars).
    annual_return : float
        Assumed annual rate of return (e.g., 0.05 for 5%).
    """

    name: str
    balance: float = 0.0
    annual_return: float = 0.0

    def deposit(self, amount: float) -> None:
        """Deposit cash into the account.

        Parameters
        ----------
        amount : float
            Amount of cash to add to the balance.

        Raises
        ------
        ValueError
            If ``amount`` is negative.
        """
        if amount < 0:
            raise ValueError("Cannot deposit a negative amount.")
        self.balance += float(amount)

    def grow(self) -> None:
        """Apply one year of investment growth to this account.

        This is a simple compound growth:
        balance <- balance * (1 + annual_return)
        """
        self.balance *= 1.0 + self.annual_return

    @abstractmethod
    def withdraw(self, amount: float) -> Tuple[float, float]:
        """Withdraw a given amount from this account.

        Parameters
        ----------
        amount : float
            Target amount of cash to withdraw from this account (non-negative).

        Returns
        -------
        taxable_income : float
            Portion of the withdrawal that is taxable.
        cash_to_spend : float
            Actual cash delivered to the retiree (after any tax assumptions).

        Notes
        -----
        Concrete subclasses must implement the tax treatment and update
        self.balance in-place. They should also handle cases where the
        requested amount exceeds the available balance.
        """
        raise NotImplementedError("Subclasses must implement withdraw().")

    def _clamp_withdrawal(self, amount: float) -> float:
        """Utility: clamp withdrawal to [0, balance] and update balance.

        Parameters
        ----------
        amount : float
            Requested withdrawal amount.

        Returns
        -------
        actual : float
            Actual amount withdrawn (0 if account empty or amount <= 0).
        """
        # No negative withdrawals, and nothing if account empty
        if amount <= 0 or self.balance <= 0:
            return 0.0

        actual = float(min(amount, self.balance))
        self.balance -= actual
        return actual

    @property
    def is_empty(self) -> bool:
        """Whether the account has (effectively) zero balance."""
        return self.balance <= 1e-6


@dataclass
class TaxDeferredAccount(AccountBase):
    """Tax-deferred account (e.g., RRSP / RRIF / LIRA / LIF).

    Simplifying assumption for the skeleton:
    - 100% of withdrawals are taxable income.
    - No explicit withdrawal minimums/maximums yet (to be refined later).
    """

    def withdraw(self, amount: float) -> Tuple[float, float]:
        actual = self._clamp_withdrawal(amount)
        taxable_income = actual  # fully taxable
        cash_to_spend = actual   # tax is handled at the overall tax system level
        return taxable_income, cash_to_spend


@dataclass
class TaxFreeAccount(AccountBase):
    """Tax-free account (e.g., TFSA).

    Simplifying assumption:
    - Withdrawals are not taxable.
    """

    def withdraw(self, amount: float) -> Tuple[float, float]:
        actual = self._clamp_withdrawal(amount)
        taxable_income = 0.0
        cash_to_spend = actual
        return taxable_income, cash_to_spend


@dataclass
class TaxableAccount(AccountBase):
    """Taxable (non-registered) account.

    Skeleton assumption for now:
    - Treat withdrawals as fully taxable (very conservative).
    - Later we can refine to split principal vs. gains.

    TODO
    ----
    - Implement more realistic capital gains treatment if needed.
    """

    def withdraw(self, amount: float) -> Tuple[float, float]:
        actual = self._clamp_withdrawal(amount)
        taxable_income = actual  # SIMPLE placeholder
        cash_to_spend = actual
        return taxable_income, cash_to_spend
