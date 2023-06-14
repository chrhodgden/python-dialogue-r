cls_str = type("string")
cls_int = type(1)
cls_byt = type(b'\x00')

def convert_to_binary(data):
	bin_data = None
	if type(data) == cls_str:
		n = ''
		for s in data:
			m = ord(s)
			m = hex(m)
			n += m.lstrip('0x')
		bin_data = n
		bin_data = int(bin_data, 16)
		bin_data = bin(bin_data)
		#bin_data = bin_data.lstrip('0b')
		bin_data = bin_data.replace('b', '')
		bin_data = ''.join(reversed(bin_data))
		bin_data = bin_data.zfill(8)
		n = b''
		for b in bin_data:
			m = int(b)
			m = chr(m)
			m = bytes(m, 'utf-8')
			n += m
		bin_data = n
	elif type(data) == cls_int:
		bin_data = bin(data)
		bin_data = bin_data.lstrip('0b')
		bin_data = bin_data.zfill(8)
		n = b''
		for b in bin_data:
			m = int(b)
			m = chr(m)
			m = bytes(m, 'utf-8')
			n += m
		bin_data = n

	return bin_data

def convert_from_binary(bin_data, cls_type):
	
	if cls_type == cls_str:
		n = ''
		for b in bin_data: n = f'{b}{n}'
		#for b in bin_data: n = f'{n}{b}'
		data = n
		data = int(data, 2)
		data = hex(data)
		data = data.lstrip('0x')
		data = bytearray.fromhex(data)	
		data = data.decode()
		data = ''.join(reversed(data))
	elif cls_type == cls_int:
		n = ''
		for b in bin_data: n = f'{n}{b}'
		data = n
		data = int(data, 2)

	return data

if __name__ == '__main__':
	print(convert_to_binary(3))	
	print(convert_to_binary('3'))
	
	int_3 = b'\x00\x00\x00\x00\x00\x00\x01\x01'
	str_3 = b'\x00\x00\x01\x01\x00\x00\x01\x01'

	print(convert_from_binary(int_3, cls_int))	
	print(convert_from_binary(str_3, cls_str))