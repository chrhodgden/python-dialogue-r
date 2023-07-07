import unittest
import dialoguer
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


class TestAlt(unittest.TestCase):

	# @classmethod
	# def setUpClass(cls):
	# 	source_file_path = __file__.replace('.py', '.r')
	# 	cls.src_fil_r = dialoguer.Dialogue(source_file_path)

	# @classmethod
	# def tearDownClass(cls):
	# 	cls.src_fil_r.close()

	# def setUp(self):
	# 	source_file_path = __file__.replace('.py', '.r')
	# 	self.src_fil_r = dialoguer.Dialogue(source_file_path)

	# def tearDown(self):
	# 	self.src_fil_r.close()

	def test_integer(self):
		source_file_path = __file__.replace('.py', '.r')
		src_fil_r = dialoguer.Dialogue(source_file_path)
		for i in range(50000):
			src_fil_r.assign_variable('int_i', i)
			chk_i = src_fil_r.import_variable('int_i')
			self.assertEqual(chk_i, i)
		src_fil_r.close()

	def test_integer_alt(self):
		for i in range(50000):
			robjects.r(f'int_i <- {i}')    
			chk_i = int(robjects.r['int_i'][0])
			#chk_i = int(chk_i[0])
			self.assertEqual(chk_i, i)


if __name__ == '__main__':
	unittest.main()
