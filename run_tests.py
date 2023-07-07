import unittest

if __name__ == "__main__":
	loader = unittest.TestLoader()
	suite = loader.discover("tests", pattern="test_*.py")
	# suite = loader.loadTestsFromName("tests.test_reliability.TestReliability.test_no_return")
	runner = unittest.TextTestRunner()
	result = runner.run(suite)
