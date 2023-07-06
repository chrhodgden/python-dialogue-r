import unittest
import dialoguer


class TestAssignVariable(unittest.TestCase):

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

	def test_assign_string(self):
		str_1 = 'Test string 1'
		str_2 = 'Test string 2'
		self.src_fil_r.assign_variable('str_1', str_1)
		self.src_fil_r.assign_variable('str_2', str_2)
		str_ret_1 = self.src_fil_r.import_variable('str_1')
		str_ret_2 = self.src_fil_r.import_variable('str_2')
		self.assertEqual(str_ret_1, str_1)
		self.assertEqual(str_ret_2, str_2)

	def test_assign_integer(self):
		int_1 = 20
		int_2 = 200
		self.src_fil_r.assign_variable('int_1', int_1)
		self.src_fil_r.assign_variable('int_2', int_2)
		int_ret_1 = self.src_fil_r.import_variable('int_1')
		int_ret_2 = self.src_fil_r.import_variable('int_2')
		self.assertEqual(int_ret_1, int_1)
		self.assertEqual(int_ret_2, int_2)

	def test_assign_boolean(self):
		chk_1 = True
		chk_2 = False
		self.src_fil_r.assign_variable('chk_1', chk_1)
		self.src_fil_r.assign_variable('chk_2', chk_2)
		chk_ret_1 = self.src_fil_r.import_variable('chk_1')
		chk_ret_2 = self.src_fil_r.import_variable('chk_2')
		self.assertEqual(chk_ret_1, chk_1)
		self.assertEqual(chk_ret_2, chk_2)

	def test_assign_double(self):
		dbl_1 = 20.5
		dbl_2 = 200.98
		self.src_fil_r.assign_variable('dbl_1', dbl_1)
		self.src_fil_r.assign_variable('dbl_2', dbl_2)
		dbl_ret_1 = self.src_fil_r.import_variable('dbl_1')
		dbl_ret_2 = self.src_fil_r.import_variable('dbl_2')
		self.assertEqual(dbl_ret_1, dbl_1)
		self.assertEqual(dbl_ret_2, dbl_2)



if __name__ == '__main__':
	unittest.main()
