import unittest
from retire_plan.accounts.models import TaxDeferredAccount, TaxFreeAccount, TaxableAccount
from retire_plan.accounts.profile import PersonProfile

class TestPersonProfile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Starting PersonProfile tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Completed PersonProfile tests")

    def setUp(self):
        print("  setUp: Creating PersonProfile")
        self.profile = PersonProfile(
            name="Alex",
            current_age=40,
            end_age=95,
            tax_deferred=TaxDeferredAccount("RRSP", 200000),
            tax_free=TaxFreeAccount("TFSA", 100000),
            taxable=TaxableAccount("Savings", 50000),
            cpp_annual=15000,
            oas_annual=8000
        )

    def tearDown(self):
        print("  tearDown: Done with profile")

    def test_total_balance(self):
        print("    Running test_total_balance")
        total = self.profile.total_balance()
        self.assertEqual(total, 350000)
        self.assertEqual(self.profile.all_balances()["tax_deferred"], 200000)
        self.assertEqual(self.profile.all_balances()["tax_free"], 100000)
        self.assertEqual(self.profile.all_balances()["taxable"], 50000)

    def test_horizon_and_benefits(self):
        print("    Running test_horizon_and_benefits")
        self.assertEqual(self.profile.retirement_horizon(), 55)
        self.assertEqual(self.profile.annual_gov_benefits(), 23000)
        self.assertEqual(self.profile.name, "Alex")
        self.assertEqual(self.profile.current_age, 40)

    def test_snapshot(self):
        print("    Running test_snapshot")
        snap = self.profile.snapshot()
        self.assertIn("balance_tax_deferred", snap)
        self.assertIn("balance_tax_free", snap)
        self.assertEqual(snap["cpp_annual"], 15000)
        self.assertEqual(snap["current_age"], 40.0)
        self.assertEqual(snap["end_age"], 95.0)