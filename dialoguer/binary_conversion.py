def convert_to_binary(data):
	bin_data = None
	if type(data) == str:
		bin_data = reversed(data)
		bin_data = "".join(bin_data)
		n = ''
		for s in bin_data:
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
	elif type(data) == int:
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
	
	if cls_type == str:
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
	elif cls_type == int:
		n = ''
		for b in bin_data: n = f'{b}{n}'
		data = n
		data = int(data, 2)
	elif cls_type == bool:
		data = bool(bin_data[0])

	return data
