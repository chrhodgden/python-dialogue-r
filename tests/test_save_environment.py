import unittest
import dialoguer


class TestSaveEnvironment(unittest.TestCase):

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

	def test_save_environment(self):
		str_1 = 'Test string 1'
		self.src_fil_r.assign_variable('str_1', str_1)
		str_ret_1 = self.src_fil_r.save_environment()
