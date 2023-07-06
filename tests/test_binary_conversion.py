import unittest
from dialoguer.binary_conversion import bin_conv

class TestBinaryConversion(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		pass
	
	def tearDown(self):
		pass

	def test_convert_boolean(self):
		data_0 = False
		data_1 = True
		conv_data_0 = bin_conv(data_0)
		conv_data_1 = bin_conv(data_1)
		conv_data_0 = bin_conv(conv_data_0, type(data_0))
		conv_data_1 = bin_conv(conv_data_1, type(data_1))
		self.assertEqual(data_0, conv_data_0)
		self.assertEqual(data_1, conv_data_1)

	def test_integer_conversion(self):
		for i in range(1000):
			bin_i = bin_conv(i)
			var_i = bin_conv(bin_i, type(i))
			self.assertEqual(i, var_i)

	def test_string_conversion(self):
		str_base = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
		str_base += str_base.upper()
		for i in range(1000):
			str_i = str(i)
			bin_i = bin_conv(str_i)
			var_i = bin_conv(bin_i, type(str_i))
			self.assertEqual(str_i, var_i)
		for s in str_base:
			bin_s = bin_conv(s)
			var_s = bin_conv(bin_s, type(s))
			self.assertEqual(s, var_s)

	def test_float_conversion(self):
		for i in range(0, 1000):
			flt_i = i + 0.5
			bin_i = bin_conv(flt_i)
			var_i = bin_conv(bin_i, type(flt_i))
			self.assertEqual(flt_i, var_i)


if __name__ == '__main__':
	unittest.main()
