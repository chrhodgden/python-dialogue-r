import unittest
import dialoguer


class TestEvaluateExpression(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		self.src_fil_r = dialoguer.Dialogue('test_evaluate_expression.r')

	def tearDown(self):
		self.src_fil_r.close()

	def test_built_in_method(self):
		res_1 = self.src_fil_r.evaluate_expression('sum', 1, 2)
		self.assertEqual(res_1, 3)

	def test_defined_method(self):
		res_1 = self.src_fil_r.evaluate_expression('test_method', 1, 2)
		self.assertEqual(res_1, 3)


if __name__ == '__main__':
	unittest.main()
