import unittest
import dialoguer


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
		bin_2 = dialoguer.binary_conversion.convert_to_binary(2)
		self.assertEqual(bin_1, bin_2)

	def test_convert_from_binary(self):
		bin_1 = b'\x00\x00\x00\x00\x00\x00\x01\x00'
		var_1 = 2
		var_2 = dialoguer.binary_conversion.convert_from_binary(bin_1, type(var_1))
		self.assertEqual(var_1, var_2)

	def test_integer_conversion(self):
		for i in range(1000):
			bin_i = dialoguer.binary_conversion.convert_to_binary(i)
			var_i = dialoguer.binary_conversion.convert_from_binary(bin_i, type(i))
			self.assertEqual(i, var_i)

	# this test currently fails. 
	# the binary conversions for strings work with R's tendancy to reverse the sockets i/o
	def test_string_conversion(self):
		str_base = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
		str_base += str_base.upper()
		for i in range(1000):
			str_i = str(i)
			bin_i = dialoguer.binary_conversion.convert_to_binary(str_i)
			print(bin_i)
			var_i = dialoguer.binary_conversion.convert_from_binary(bin_i, type(str_i))
			self.assertEqual(str_i, var_i)
		for s in str_base:
			bin_s = dialoguer.binary_conversion.convert_to_binary(s)
			var_s = dialoguer.binary_conversion.convert_from_binary(bin_s, type(s))
			self.assertEqual(s, var_s)


if __name__ == '__main__':
	unittest.main()
