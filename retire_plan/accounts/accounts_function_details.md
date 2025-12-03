# retire_plan – Accounts Module Function Details (Short)

This document summarizes the public interface you implemented, aligned with the current code:

- `retire_plan/__init__.py`
- `retire_plan/accounts/__init__.py`
- `retire_plan/accounts/models.py`
- `retire_plan/accounts/profile.py`

---

## 1. Package structure

Top-level package: `retire_plan`

- Re-exports:
  - Subpackages: `accounts`, `simulation`, `strategies`
  - Classes: `AccountBase`, `TaxDeferredAccount`, `TaxFreeAccount`, `TaxableAccount`, `PersonProfile`
  - Metadata: `__version__ = "0.1.0"`

Example imports:

```python
from retire_plan import TaxDeferredAccount, TaxFreeAccount, TaxableAccount, PersonProfile
# or
from retire_plan.accounts import TaxDeferredAccount, PersonProfile
```

---

## 2. Account classes (`retire_plan.accounts.models`)

### 2.1 `AccountBase`

Abstract base class for all account types.

- **Attributes**
  - `name: str` – account label.
  - `balance: float = 0.0` – current market value.
  - `annual_return: float = 0.0` – annual growth rate (e.g. `0.05`).

- **Methods**
  - `deposit(amount: float) -> None`  
    - Add cash; raises `ValueError` if `amount < 0`.
  - `grow() -> None`  
    - `balance *= (1 + annual_return)`.
  - `withdraw(amount: float) -> (taxable_income, cash_to_spend)`  
    - Abstract; implemented in subclasses.
  - `_clamp_withdrawal(amount: float) -> float`  
    - Clamp to `[0, balance]`, update `balance`, return actual.
  - `is_empty -> bool`  
    - `True` if `balance <= 1e-6`.

### 2.2 `TaxDeferredAccount(AccountBase)`

- Example: RRSP, RRIF, LIRA, LIF.
- Tax rule: withdrawals are **fully taxable**.
- `withdraw(amount)`:
  - Uses `_clamp_withdrawal`.
  - Returns `(taxable_income=actual, cash_to_spend=actual)`.

### 2.3 `TaxFreeAccount(AccountBase)`

- Example: TFSA.
- Tax rule: withdrawals are **not taxable**.
- `withdraw(amount)`:
  - Uses `_clamp_withdrawal`.
  - Returns `(taxable_income=0.0, cash_to_spend=actual)`.

### 2.4 `TaxableAccount(AccountBase)`

- Example: non-registered investment account.
- Tax rule (simplified placeholder): withdrawals treated as **fully taxable**.
- `withdraw(amount)`:
  - Uses `_clamp_withdrawal`.
  - Returns `(taxable_income=actual, cash_to_spend=actual)`.

---

## 3. Person profile (`retire_plan.accounts.profile`)

### 3.1 `PersonProfile`

Represents one retiree / household and bundles three accounts.

- **Attributes**
  - `name: str`
  - `current_age: int`
  - `end_age: int`
  - `tax_deferred: AccountBase`
  - `tax_free: AccountBase`
  - `taxable: AccountBase`
  - `cpp_annual: float = 0.0`
  - `oas_annual: float = 0.0`

- **Methods**
  - `all_balances() -> dict`  
    - `{"tax_deferred": ..., "tax_free": ..., "taxable": ...}`.
  - `total_balance() -> float`  
    - Sum of all three balances.
  - `retirement_horizon() -> int`  
    - `max(0, end_age - current_age)`.
  - `annual_gov_benefits() -> float`  
    - `cpp_annual + oas_annual`.
  - `snapshot() -> dict`  
    - Flat dict with age, CPP/OAS and balances (for logging / DataFrame).

---

## 4. Minimal usage example

```python
from retire_plan.accounts import (
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
    PersonProfile,
)

# Create accounts
rrsp = TaxDeferredAccount(name="RRSP", balance=100_000, annual_return=0.05)
tfsa = TaxFreeAccount(name="TFSA", balance=50_000, annual_return=0.05)
taxable = TaxableAccount(name="Taxable", balance=20_000, annual_return=0.04)

# Create profile
profile = PersonProfile(
    name="Demo",
    current_age=60,
    end_age=95,
    tax_deferred=rrsp,
    tax_free=tfsa,
    taxable=taxable,
    cpp_annual=12_000,
    oas_annual=8_000,
)

# Quick checks
profile.total_balance()
profile.annual_gov_benefits()
profile.snapshot()
```
