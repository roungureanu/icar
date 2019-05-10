import unittest

import sample_test


if __name__ == '__main__':
    tests_to_run = [
        sample_test.BasicTest
    ]

    tests_loader = unittest.TestLoader()

    suites = []
    for test_class in tests_to_run:
        suites.append(
            tests_loader.loadTestsFromTestCase(test_class)
        )

    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(suite)
