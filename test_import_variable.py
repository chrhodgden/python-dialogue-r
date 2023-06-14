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
		self.src_fil_r.open()
	
	def tearDown(self):
		self.src_fil_r.close()

	def test_import_variable(self):
		msg_1 = self.src_fil_r.import_variable('msg_1')
		msg_2 = self.src_fil_r.import_variable('msg_2')
		self.assertEqual(msg_1, 'Initializing Client - R')
		self.assertEqual(msg_2, 'Initialized Client - R')


if __name__ == '__main__':
	unittest.main()
