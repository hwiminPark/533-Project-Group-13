import unittest

# Import all test modules
from test_models import TestAccountModels
from test_profile import TestPersonProfile
from test_metrics import TestMetrics
from test_policies import TestPolicies
from test_engine import TestSimulator
from test_analysis import TestAnalysis

def create_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestAccountModels))
    suite.addTests(loader.loadTestsFromTestCase(TestPersonProfile))
    suite.addTests(loader.loadTestsFromTestCase(TestMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestPolicies))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalysis))

    print("Test suite created with all 6 test classes")
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_suite()
    runner.run(test_suite)