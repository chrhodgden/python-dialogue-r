import unittest
import dialoguer


class TestImportVariable(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		self.src_fil_r = dialoguer.Dialogue('test_import_variable.r')
	
	def tearDown(self):
		self.src_fil_r.close()

	def test_import_string(self):
		msg_1 = self.src_fil_r.import_variable('msg_1')
		msg_2 = self.src_fil_r.import_variable('msg_2')
		self.assertEqual(msg_1, 'Initializing Client - R')
		self.assertEqual(msg_2, 'Initialized Client - R')

	def test_import_integer(self):
		int_1 = self.src_fil_r.import_variable('int_1')
		int_2 = self.src_fil_r.import_variable('int_2')
		self.assertEqual(int_1, 3)
		self.assertEqual(int_2, 155)

	def test_import_boolean(self):
		chk_1 = self.src_fil_r.import_variable('chk_1')
		chk_2 = self.src_fil_r.import_variable('chk_2')
		self.assertEqual(chk_1, True)
		self.assertEqual(chk_2, False)


if __name__ == '__main__':
	unittest.main()
