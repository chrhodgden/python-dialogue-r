def bin_conv(data, data_type = None):
	conv_data = None
	#convert to binary 
	if type(data) == str and data_type == None:
		conv_data = reversed(data)
		conv_data = ''.join(conv_data)
		n = ''
		for s in conv_data:
			m = ord(s)
			m = hex(m)
			n += m.lstrip('0x')
		conv_data = n
		conv_data = int(conv_data, 16)
		conv_data = bin(conv_data)
		conv_data = conv_data.replace('b', '')
		conv_data = ''.join(reversed(conv_data))
		conv_data = conv_data.zfill(8)
		n = b''
		for b in conv_data:
			m = int(b)
			m = chr(m)
			m = bytes(m, 'utf-8')
			n += m
		conv_data = n
	elif type(data) == int and data_type == None:
		conv_data = bin(data)
		conv_data = conv_data.lstrip('0b')
		conv_data = conv_data.zfill(8)
		n = b''
		for b in conv_data:
			m = int(b)
			m = chr(m)
			m = bytes(m, 'utf-8')
			n += m
		conv_data = n
	
	#convert from binary 
	elif type(data) == bytes and data_type == str:
		n = ''
		for b in data: n = f'{b}{n}'
		conv_data = n
		conv_data = int(conv_data, 2)
		conv_data = hex(conv_data)
		conv_data = conv_data.lstrip('0x')
		conv_data = bytearray.fromhex(conv_data)	
		conv_data = conv_data.decode()
		conv_data = ''.join(reversed(conv_data))
	elif type(data) == bytes and data_type == int:
		n = ''
		for b in data: n = f'{b}{n}'
		conv_data = n
		conv_data = int(conv_data, 2)
	elif type(data) == bytes and data_type == bool:
		conv_data = bool(data[0])

	return conv_data