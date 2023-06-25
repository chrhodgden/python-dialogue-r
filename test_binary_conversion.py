import unittest
from dialoguer.binary_conversion import bin_conv

# perhaps we can put reversals in this test
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

	def test_convert_to_binary(self):
		bin_1 = b'\x00\x00\x00\x00\x00\x00\x01\x00'
		bin_2 = bin_conv(2)
		self.assertEqual(bin_1, bin_2)

	def test_convert_from_binary(self):
		bin_1 = b'\x00\x01\x00\x00\x00\x00\x00\x00'
		var_1 = 2
		var_2 = bin_conv(bin_1, type(var_1))
		self.assertEqual(var_1, var_2)

	def test_integer_conversion(self):
		for i in range(1000):
			bin_i = bin_conv(i)
			bin_i = bytes(reversed(bin_i))
			var_i = bin_conv(bin_i, type(i))
			self.assertEqual(i, var_i)

	# this test currently fails because bytes are reversed. 
	# the binary conversions work with R's tendancy to reverse the sockets i/o
	def test_string_conversion(self):
		str_base = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
		str_base += str_base.upper()
		for i in range(1000):
			str_i = str(i)
			bin_i = bin_conv(str_i)
			print(bin_i, type(bin_i))
			var_i = bin_conv(bin_i, type(str_i))
			self.assertEqual(str_i, var_i)
		for s in str_base:
			bin_s = bin_conv(s)
			bin_s = bytes(reversed(bin_s))
			var_s = bin_conv(bin_s, type(s))
			self.assertEqual(s, var_s)


if __name__ == '__main__':
	unittest.main()
