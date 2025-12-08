"""
Unit tests for the retire_plan.accounts subpackage.

Covers:
- models.py: AccountBase, TaxDeferredAccount, TaxFreeAccount, TaxableAccount
- profile.py: PersonProfile
"""

import unittest

from retire_plan.accounts.models import (
    AccountBase,
    TaxDeferredAccount,
    TaxFreeAccount,
    TaxableAccount,
)
from retire_plan.accounts.profile import PersonProfile


# ==============================
# AccountBase behavior (via subclass)
# ==============================

class TestAccountBaseDeposit(unittest.TestCase):
    """Test shared deposit behavior on AccountBase via a concrete subclass."""

    def setUp(self) -> None:
        self.acc = TaxDeferredAccount(name="RRSP", balance=10_000.0, annual_return=0.05)

    def test_deposit_positive_amount_increases_balance(self) -> None:
        self.acc.deposit(1_000.0)
        self.assertAlmostEqual(self.acc.balance, 11_000.0)

    def test_deposit_negative_amount_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.acc.deposit(-1.0)


# ==============================
# TaxDeferredAccount
# ==============================

class TestTaxDeferredAccount(unittest.TestCase):
    """Tests for tax-deferred accounts (e.g., RRSP/RRIF)."""

    def setUp(self) -> None:
        self.account = TaxDeferredAccount(
            name="RRSP",
            balance=100_000.0,
            annual_return=0.05,
        )

    def test_is_subclass_of_account_base(self) -> None:
        self.assertIsInstance(self.account, AccountBase)

    def test_grow_uses_annual_return(self) -> None:
        before = self.account.balance
        self.account.grow()
        expected = before * (1.0 + self.account.annual_return)
        self.assertAlmostEqual(self.account.balance, expected, places=6)

    def test_withdraw_positive_reduces_balance_and_is_fully_taxable(self) -> None:
        taxable, cash = self.account.withdraw(10_000.0)
        self.assertAlmostEqual(taxable, 10_000.0)
        self.assertAlmostEqual(cash, 10_000.0)
        self.assertAlmostEqual(self.account.balance, 90_000.0)

    def test_withdraw_more_than_balance_clamps_to_balance(self) -> None:
        taxable, cash = self.account.withdraw(200_000.0)
        self.assertAlmostEqual(taxable, 100_000.0)
        self.assertAlmostEqual(cash, 100_000.0)
        self.assertAlmostEqual(self.account.balance, 0.0)

    def test_withdraw_zero_or_negative_does_nothing(self) -> None:
        before = self.account.balance
        taxable, cash = self.account.withdraw(0.0)
        self.assertAlmostEqual(taxable, 0.0)
        self.assertAlmostEqual(cash, 0.0)
        self.assertAlmostEqual(self.account.balance, before)

        taxable2, cash2 = self.account.withdraw(-5_000.0)
        self.assertAlmostEqual(taxable2, 0.0)
        self.assertAlmostEqual(cash2, 0.0)
        self.assertAlmostEqual(self.account.balance, before)


# ==============================
# TaxFreeAccount
# ==============================

class TestTaxFreeAccount(unittest.TestCase):
    """Tests for tax-free accounts (e.g., TFSA)."""

    def setUp(self) -> None:
        self.account = TaxFreeAccount(
            name="TFSA",
            balance=50_000.0,
            annual_return=0.10,
        )

    def test_is_subclass_of_account_base(self) -> None:
        self.assertIsInstance(self.account, AccountBase)

    def test_grow_uses_annual_return(self) -> None:
        before = self.account.balance
        self.account.grow()
        expected = before * (1.0 + self.account.annual_return)
        self.assertAlmostEqual(self.account.balance, expected, places=6)

    def test_withdraw_not_taxable(self) -> None:
        taxable, cash = self.account.withdraw(10_000.0)
        self.assertAlmostEqual(taxable, 0.0)
        self.assertAlmostEqual(cash, 10_000.0)
        self.assertAlmostEqual(self.account.balance, 40_000.0)

    def test_withdraw_more_than_balance_clamps_to_balance(self) -> None:
        taxable, cash = self.account.withdraw(100_000.0)
        self.assertAlmostEqual(taxable, 0.0)
        self.assertAlmostEqual(cash, 50_000.0)
        self.assertAlmostEqual(self.account.balance, 0.0)

    def test_withdraw_zero_or_negative_does_nothing(self) -> None:
        before = self.account.balance
        taxable, cash = self.account.withdraw(0.0)
        self.assertAlmostEqual(taxable, 0.0)
        self.assertAlmostEqual(cash, 0.0)
        self.assertAlmostEqual(self.account.balance, before)

        taxable2, cash2 = self.account.withdraw(-1_000.0)
        self.assertAlmostEqual(taxable2, 0.0)
        self.assertAlmostEqual(cash2, 0.0)
        self.assertAlmostEqual(self.account.balance, before)


# ==============================
# TaxableAccount
# ==============================

class TestTaxableAccount(unittest.TestCase):
    """Tests for taxable non-registered accounts."""

    def setUp(self) -> None:
        self.account = TaxableAccount(
            name="Taxable",
            balance=20_000.0,
            annual_return=0.03,
        )

    def test_is_subclass_of_account_base(self) -> None:
        self.assertIsInstance(self.account, AccountBase)

    def test_grow_uses_annual_return(self) -> None:
        before = self.account.balance
        self.account.grow()
        expected = before * (1.0 + self.account.annual_return)
        self.assertAlmostEqual(self.account.balance, expected, places=6)

    def test_withdraw_treated_as_taxable_placeholder(self) -> None:
        taxable, cash = self.account.withdraw(5_000.0)
        self.assertAlmostEqual(taxable, 5_000.0)
        self.assertAlmostEqual(cash, 5_000.0)
        self.assertAlmostEqual(self.account.balance, 15_000.0)

    def test_withdraw_more_than_balance_clamps_to_balance(self) -> None:
        taxable, cash = self.account.withdraw(50_000.0)
        self.assertAlmostEqual(taxable, 20_000.0)
        self.assertAlmostEqual(cash, 20_000.0)
        self.assertAlmostEqual(self.account.balance, 0.0)

    def test_withdraw_zero_or_negative_does_nothing(self) -> None:
        before = self.account.balance
        taxable, cash = self.account.withdraw(0.0)
        self.assertAlmostEqual(taxable, 0.0)
        self.assertAlmostEqual(cash, 0.0)
        self.assertAlmostEqual(self.account.balance, before)

        taxable2, cash2 = self.account.withdraw(-500.0)
        self.assertAlmostEqual(taxable2, 0.0)
        self.assertAlmostEqual(cash2, 0.0)
        self.assertAlmostEqual(self.account.balance, before)


# ==============================
# PersonProfile
# ==============================

class TestPersonProfile(unittest.TestCase):
    """Integration tests for PersonProfile and the three accounts."""

    def setUp(self) -> None:
        self.acc_td = TaxDeferredAccount(
            name="RRSP",
            balance=100_000.0,
            annual_return=0.05,
        )
        self.acc_tf = TaxFreeAccount(
            name="TFSA",
            balance=50_000.0,
            annual_return=0.10,
        )
        self.acc_taxable = TaxableAccount(
            name="Taxable",
            balance=20_000.0,
            annual_return=0.03,
        )

        self.profile = PersonProfile(
            name="Demo",
            current_age=60,
            end_age=95,
            tax_deferred=self.acc_td,
            tax_free=self.acc_tf,
            taxable=self.acc_taxable,
            cpp_annual=12_000.0,
            oas_annual=8_000.0,
        )

    def test_profile_holds_account_objects(self) -> None:
        self.assertIsInstance(self.profile.tax_deferred, AccountBase)
        self.assertIsInstance(self.profile.tax_free, AccountBase)
        self.assertIsInstance(self.profile.taxable, AccountBase)

    def test_all_balances_keys_and_values(self) -> None:
        balances = self.profile.all_balances()
        self.assertEqual(set(balances.keys()),
                         {"tax_deferred", "tax_free", "taxable"})
        self.assertAlmostEqual(balances["tax_deferred"], 100_000.0)
        self.assertAlmostEqual(balances["tax_free"], 50_000.0)
        self.assertAlmostEqual(balances["taxable"], 20_000.0)

    def test_all_balances_reflect_updated_accounts(self) -> None:
        self.acc_td.grow()
        self.acc_tf.grow()
        self.acc_taxable.grow()

        balances = self.profile.all_balances()
        self.assertAlmostEqual(balances["tax_deferred"], self.acc_td.balance)
        self.assertAlmostEqual(balances["tax_free"], self.acc_tf.balance)
        self.assertAlmostEqual(balances["taxable"], self.acc_taxable.balance)

    def test_total_balance_is_sum_of_all_accounts(self) -> None:
        total = self.profile.total_balance()
        self.assertAlmostEqual(total, 100_000.0 + 50_000.0 + 20_000.0)

    def test_retirement_horizon_basic(self) -> None:
        self.assertEqual(self.profile.retirement_horizon(), 95 - 60)

    def test_retirement_horizon_never_negative(self) -> None:
        p = PersonProfile(
            name="TooLate",
            current_age=80,
            end_age=75,
            tax_deferred=self.acc_td,
            tax_free=self.acc_tf,
            taxable=self.acc_taxable,
            cpp_annual=0.0,
            oas_annual=0.0,
        )
        self.assertEqual(p.retirement_horizon(), 0)

    def test_annual_gov_benefits(self) -> None:
        self.assertAlmostEqual(self.profile.annual_gov_benefits(), 20_000.0)

    def test_snapshot_structure_and_values(self) -> None:
        snap = self.profile.snapshot()

        for key in ["current_age", "end_age", "cpp_annual", "oas_annual"]:
            self.assertIn(key, snap)

        for key in [
            "balance_tax_deferred",
            "balance_tax_free",
            "balance_taxable",
        ]:
            self.assertIn(key, snap)

        self.assertAlmostEqual(snap["current_age"], 60.0)
        self.assertAlmostEqual(snap["end_age"], 95.0)
        self.assertAlmostEqual(snap["cpp_annual"], 12_000.0)
        self.assertAlmostEqual(snap["oas_annual"], 8_000.0)

        self.assertAlmostEqual(snap["balance_tax_deferred"], 100_000.0)
        self.assertAlmostEqual(snap["balance_tax_free"], 50_000.0)
        self.assertAlmostEqual(snap["balance_taxable"], 20_000.0)


if __name__ == "__main__":
    unittest.main()
