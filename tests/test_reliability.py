import unittest
import dialoguer


class TestReliability(unittest.TestCase):

	# @classmethod
	# def setUpClass(cls):
	# 	source_file_path = __file__.replace('.py', '.r')
	# 	cls.src_fil_r = dialoguer.Dialogue(source_file_path)

	# @classmethod
	# def tearDownClass(cls):
	# 	cls.src_fil_r.close()

	def setUp(self):
		source_file_path = __file__.replace('.py', '.r')
		self.src_fil_r = dialoguer.Dialogue(source_file_path)

	def tearDown(self):
		self.src_fil_r.close()

	def test_integer(self):
		for i in range(20000):
			self.src_fil_r.assign_variable('int_i', i)
			chk_i = self.src_fil_r.import_variable('int_i')
			self.assertEqual(chk_i, i)

	def test_string(self):
		for i in range(20000):
			str_i = str(i)
			self.src_fil_r.assign_variable('str_i', str_i)
			chk_i = self.src_fil_r.import_variable('str_i')
			self.assertEqual(chk_i, str_i)

	def test_method(self):
		self.src_fil_r.assign_variable('vect_0', 1)
		for i in range(10000):
			chk = self.src_fil_r.evaluate_expression('add_to_vector', 'vect_0', i)
		self.src_fil_r.evaluate_expression('display_vector', 'vect_0')

	def test_vector(self):
		self.src_fil_r.assign_variable('vect_0', 1)
		self.src_fil_r.evaluate_expression('add_to_vector', 'vect_0', 2)
		vect_0 = self.src_fil_r.import_variable('vect_0')
		print(vect_0)

	def test_no_return(self):
		val = self.src_fil_r.evaluate_expression('no_return_method', 2)
		print(val)


if __name__ == '__main__':
	unittest.main()
