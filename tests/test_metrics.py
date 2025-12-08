# tests/test_metrics.py
import unittest
from retire_plan.simulation.metrics import TaxCalculator, calculate_shortfall_years, project_tax_efficiency

class TestMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass: Starting Metrics tests")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: Finished Metrics tests")

    def setUp(self):
        print("  setUp: Creating TaxCalculator")
        self.calc = TaxCalculator(province="ON")

    def tearDown(self):
        print("  tearDown: Done with calc")

    def test_tax_brackets_progression(self):
        print("    Running test_tax_brackets_progression")
        rate40k = self.calc.effective_rate(40000)
        rate150k = self.calc.effective_rate(150000)
        rate300k = self.calc.effective_rate(300000)

        # Realistic Canadian effective rates (2025 brackets + ON tax)
        self.assertGreater(rate40k, 0.22)      # ~26-28%
        self.assertLess(rate40k, 0.35)
        self.assertGreater(rate150k, 0.30)     # ~31-32%
        self.assertLess(rate150k, 0.40)
        self.assertGreater(rate300k, 0.35)     # ~36.3% → this is correct!
        self.assertLess(rate300k, 0.45)        # marginal hits ~44.5%, effective stays under 45%

    def test_shortfall_and_efficiency(self):
        print("    Running test_shortfall_and_efficiency")
        history = [100000, 90000, 80000, 120000, 70000]
        shortfalls = calculate_shortfall_years(history, 95000)
        self.assertEqual(shortfalls, 3)  # 90k, 80k, 70k → 3 years

        efficiency = project_tax_efficiency(20000, 100000)
        self.assertAlmostEqual(efficiency, 0.2, places=3)
        self.assertEqual(project_tax_efficiency(0, 100), 0.0)
        self.assertGreaterEqual(efficiency, 0)