"""
accounts subpackage

This subpackage defines:

- AccountBase: abstract base class for all investment / savings accounts
- TaxDeferredAccount: e.g., RRSP / RRIF / LIRA / LIF (withdrawals fully taxable)
- TaxFreeAccount: e.g., TFSA (withdrawals not taxable)
- TaxableAccount: non-registered account (simplified tax behavior for now)
- PersonProfile: container for a single retiree / household, holding
  all three account types plus basic demographic and benefit info.

Typical usage
-------------
>>> from retire_plan.accounts import (
...     TaxDeferredAccount,
...     TaxFreeAccount,
...     TaxableAccount,
...     PersonProfile,
... )
>>> rrsp = TaxDeferredAccount(name="RRSP", balance=300_000)
>>> tfsa = TaxFreeAccount(name="TFSA", balance=80_000)
>>> taxable = TaxableAccount(name="Taxable", balance=50_000)
>>> profile = PersonProfile(
...     name="Demo",
...     current_age=60,
...     end_age=95,
...     tax_deferred=rrsp,
...     tax_free=tfsa,
...     taxable=taxable,
...     cpp_annual=12_000,
...     oas_annual=8_000,
... )
>>> profile.total_balance()
430000.0
"""

from __future__ import annotations

from .models import (
    AccountBase,
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
)
from .profile import PersonProfile

# What we export when someone does:
#   from retire_plan.accounts import *
__all__ = [
    "AccountBase",
    "TaxDeferredAccount",
    "TaxFreeAccount",
    "TaxableAccount",
    "PersonProfile",
]
