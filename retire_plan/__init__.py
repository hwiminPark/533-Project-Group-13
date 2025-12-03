"""
retire_plan - Retirement planning toolkit for Canadian households.

Top-level package exposing three subpackages:

- accounts:   account models and person profile
- simulation: tax system and simulation engine
- strategies: withdrawal policies and analysis utilities

Typical usage
-------------
>>> from retire_plan import TaxDeferredAccount, TaxFreeAccount, TaxableAccount, PersonProfile
>>> rrsp = TaxDeferredAccount(name="RRSP", balance=300_000)
>>> tfsa = TaxFreeAccount(name="TFSA", balance=80_000)
>>> taxable = TaxableAccount(name="Taxable", balance=50_000)
>>> person = PersonProfile(
...     name="Demo",
...     current_age=60,
...     end_age=95,
...     tax_deferred=rrsp,
...     tax_free=tfsa,
...     taxable=taxable,
...     cpp_annual=12_000,
...     oas_annual=8_000,
... )
"""

from __future__ import annotations

# Subpackages
from . import accounts
from . import simulation
from . import strategies

# Re-export commonly used classes so that users can write:
#   from retire_plan import TaxDeferredAccount, PersonProfile
from .accounts import (
    AccountBase,
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
    PersonProfile,
)

# Simple manual version tag (can be updated by the group later)
__version__ = "0.1.0"

__all__ = [
    # Subpackages
    "accounts",
    "simulation",
    "strategies",
    # Core account models
    "AccountBase",
    "TaxDeferredAccount",
    "TaxFreeAccount",
    "TaxableAccount",
    # Profile model
    "PersonProfile",
    # Metadata
    "__version__",
]

