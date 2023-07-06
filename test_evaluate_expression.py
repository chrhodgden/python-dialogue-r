import unittest
import dialoguer


class TestEvaluateExpression(unittest.TestCase):

	# @classmethod
	# def setUpClass(cls):
	# 	cls.src_fil_r = dialoguer.Dialogue('test_evaluate_expression.r')

	# @classmethod
	# def tearDownClass(cls):
	# 	cls.src_fil_r.close()

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

	def test_kwargs(self):
		kwargs = {
			'arg_1': 2,
			'arg_2': 3
		}
		res_1 = self.src_fil_r.evaluate_expression('test_kwargs', **kwargs)
		self.assertEqual(res_1, 6)

	def test_args_and_kwargs(self):
		args = [2, 3]
		kwargs = {
			'kwarg_1': 2,
			'kwarg_2': 3
		}
		res_1 = self.src_fil_r.evaluate_expression('test_args_and_kwargs', *args, **kwargs)
		res_ctrl = args[0] * args[1] * kwargs['kwarg_1'] * kwargs['kwarg_2']
		self.assertEqual(res_ctrl, res_1)

	def test_args_and_default_kwargs(self):
		args = [2, 3]
		kwargs = {
			'kwarg_2': 3
		}
		res_1 = self.src_fil_r.evaluate_expression('test_args_and_kwargs', *args, **kwargs)
		res_ctrl = args[0] * args[1] * 1 * kwargs['kwarg_2']
		self.assertEqual(res_ctrl, res_1)


if __name__ == '__main__':
	unittest.main()
