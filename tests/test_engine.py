import unittest
from retire_plan.accounts.profile import PersonProfile
from retire_plan.accounts.models import TaxDeferredAccount, TaxFreeAccount, TaxableAccount
from retire_plan.simulation.engine import Simulator
from retire_plan.strategies.policies import contrib_max_tfsa_first, strategy_spend_taxable_first

class TestSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Starting Simulator tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Simulator tests complete")

    def setUp(self):
        print("  setUp: Creating test profile and simulator")
        profile = PersonProfile(
            name="Test", current_age=30, end_age=95,
            tax_deferred=TaxDeferredAccount("RRSP", 10000),
            tax_free=TaxFreeAccount("TFSA", 5000),
            taxable=TaxableAccount("Savings", 2000),
            cpp_annual=10000, oas_annual=7000
        )
        self.sim = Simulator(profile)

    def tearDown(self):
        print("  tearDown: Simulator test done")

    def test_accumulation_phase(self):
        print("    Running test_accumulation_phase")
        self.sim.run_accumulation(contrib_max_tfsa_first, years_to_retirement=2, annual_savings=20000)
        self.assertGreater(len(self.sim.history), 0)
        self.assertGreater(self.sim.profile.tax_free.balance, 5000)
        self.assertEqual(self.sim.profile.current_age, 32)

    def test_full_lifecycle(self):
        print("    Running test_full_lifecycle")
        result = self.sim.run_full_lifecycle(
            contrib_max_tfsa_first, strategy_spend_taxable_first,
            years_working=3, annual_savings=20000, annual_spending=50000
        )

    def test_run_accumulation_negative_years_raises(self):
        with self.assertRaises(ValueError):
            self.sim.run_accumulation(
                contrib_max_tfsa_first,
                years_to_retirement=-1,   # 注意：负数才触发
                annual_savings=20_000,
            )

    def test_run_accumulation_negative_savings_raises(self):
        """annual_savings < 0 应该报错。"""
        with self.assertRaises(ValueError):
            self.sim.run_accumulation(
                contrib_max_tfsa_first,
                years_to_retirement=1,
                annual_savings=-10_000,   # 负数才触发
            )

    def test_run_decumulation_non_positive_spending_raises(self):
        """annual_spending <= 0 应该报错。"""
        with self.assertRaises(ValueError):
            self.sim.run_decumulation(
                strategy_spend_taxable_first,
                annual_spending=0.0,      # 这里 0 或负数都行
            )

        
