import unittest
from retire_plan.strategies.policies import (
    contrib_max_tfsa_first, contrib_max_rrsp_first,
    strategy_spend_taxable_first, strategy_spend_rrsp_first
)

class TestPolicies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Starting Policy tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Done with policies")

    def setUp(self):
        print("  setUp: Preparing state dicts")
        self.contrib_state = {"annual_savings_available": 50000}
        self.withdraw_state = {
            "target_net_cash": 80000,
            "cpp_income": 15000,
            "oas_income": 8000,
            "balances": {"tax_deferred": 200000, "tax_free": 100000, "taxable": 50000}
        }

    def tearDown(self):
        print("  tearDown: Policy test complete")

    def test_contribution_strategies(self):
        print("    Running test_contribution_strategies")
        plan1 = contrib_max_tfsa_first(self.contrib_state)
        self.assertEqual(plan1["tax_free"], 7500)
        self.assertGreater(plan1["tax_deferred"], 0)
        self.assertIn("taxable", plan1)

        plan2 = contrib_max_rrsp_first(self.contrib_state)
        self.assertGreater(plan2["tax_deferred"], plan2["tax_free"])
        self.assertLessEqual(plan2["tax_free"], 7500)

    def test_withdrawal_ordering(self):
        print("    Running test_withdrawal_ordering")
        plan_taxable = strategy_spend_taxable_first(self.withdraw_state)
        # Shortfall = 80k - 23k gov = 57k needed
        # Taxable has 50k → takes all → still needs 7k → takes from RRSP
        self.assertEqual(plan_taxable["taxable"], 50000)
        self.assertEqual(plan_taxable["tax_deferred"], 7000)
        self.assertEqual(plan_taxable["tax_free"], 0.0)   # ← TFSA untouched

        plan_rrsp = strategy_spend_rrsp_first(self.withdraw_state)
        self.assertGreater(plan_rrsp["tax_deferred"], 50000)  # Takes most from RRSP first