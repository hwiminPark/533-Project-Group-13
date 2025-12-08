import unittest
from retire_plan.accounts.models import (
    AccountBase, TaxDeferredAccount, TaxFreeAccount, TaxableAccount
)

class TestAccountModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Initializing AccountBase tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Finished AccountBase tests")

    def setUp(self):
        print("  setUp: Creating fresh accounts")
        self.deferred = TaxDeferredAccount("RRSP", balance=100000, annual_return=0.05)
        self.tfsa = TaxFreeAccount("TFSA", balance=50000, annual_return=0.05)
        self.taxable = TaxableAccount("Non-reg", balance=30000, annual_return=0.05)

    def tearDown(self):
        print("  tearDown: Cleaning up accounts")

    def test_deposit_and_growth(self):
        print("    Running test_deposit_and_growth")
        self.deferred.deposit(10000)
        self.deferred.grow()
        expected = 110000 * 1.05
        self.assertAlmostEqual(self.deferred.balance, expected, places=2)
        self.assertGreater(self.deferred.balance, 100000)
        self.assertEqual(self.deferred.name, "RRSP")
        self.assertEqual(self.deferred.annual_return, 0.05)

    def test_withdraw_tax_deferred(self):
        print("    Running test_withdraw_tax_deferred")
        taxable, cash = self.deferred.withdraw(20000)
        self.assertAlmostEqual(taxable, 20000, places=2)
        self.assertAlmostEqual(cash, 20000, places=2)
        self.assertAlmostEqual(self.deferred.balance, 80000, places=2)
        self.assertFalse(self.deferred.is_empty)

    def test_withdraw_tax_free(self):
        print("    Running test_withdraw_tax_free")
        taxable, cash = self.tfsa.withdraw(30000)
        self.assertAlmostEqual(taxable, 0.0, places=2)
        self.assertAlmostEqual(cash, 30000, places=2)
        self.assertAlmostEqual(self.tfsa.balance, 20000, places=2)
        self.assertFalse(self.tfsa.is_empty)

    def test_clamp_withdrawal_on_empty(self):
        print("    Running test_clamp_withdrawal_on_empty")
        empty = TaxFreeAccount("Empty", balance=0)
        taxable, cash = empty.withdraw(1000)
        self.assertEqual(taxable, 0)
        self.assertEqual(cash, 0)
        self.assertEqual(empty.balance, 0)
        self.assertTrue(empty.is_empty)