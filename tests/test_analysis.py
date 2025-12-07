import unittest
from retire_plan.strategies.analysis import (
    summarize_results, compare_strategies, income_profile_by_age
)

class TestAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Starting Analysis tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Analysis tests done")

    def setUp(self):
        print("  setUp: Creating fake results")
        self.results = [
            {"age": 65, "tax_paid": 10000, "net_cash_flow": 60000, "end_balances": {"tax_deferred": 200000, "tax_free": 100000, "taxable": 50000}},
            {"age": 66, "tax_paid": 12000, "net_cash_flow": 62000, "end_balances": {"tax_deferred": 180000, "tax_free": 110000, "taxable": 40000}},
        ]

    def tearDown(self):
        print("  tearDown: Analysis test complete")

    def test_summarize_results(self):
        print("    Running test_summarize_results")
        summary = summarize_results("Strategy A", self.results)
        self.assertEqual(summary["lifetime_tax"], 22000)
        self.assertEqual(summary["final_wealth"], 330000)
        self.assertIn("avg_net_cash", summary)
        self.assertGreater(summary["avg_net_cash"], 60000)
        with self.assertRaises(ValueError):
            summarize_results("Strategy B", None)

    def test_compare_strategies(self):
        print("    Running test_compare_strategies")
        summaries = [
            {"name": "A", "lifetime_tax": 50000, "final_wealth": 1000000},
            {"name": "B", "lifetime_tax": 40000, "final_wealth": 900000},
        ]
        comparison = compare_strategies(summaries)
        self.assertEqual(comparison["lowest_tax_strategy"], "B")
        self.assertEqual(comparison["highest_wealth_strategy"], "A")
        with self.assertRaises(ValueError):
            compare_strategies(None)