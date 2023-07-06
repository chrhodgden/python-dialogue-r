import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    # suite = loader.loadTestsFromName("tests.test_assign_variable.TestAssignVariable.test_assign_double")
    # suite = loader.loadTestsFromName("tests.test_assign_variable.TestAssignVariable")
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
