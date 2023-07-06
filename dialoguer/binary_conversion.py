def bin_conv(data, data_type = None):
	conv_data = None
	#convert to binary 
	if type(data) == str and data_type == None:
		conv_data = bytes(data, 'utf-8')
	elif type(data) == int and data_type == None:
		conv_data = data.to_bytes(32, 'little')
		#print(conv_data)
		# conv_data = bin(data)
		# conv_data = conv_data.lstrip('0b')
		# conv_data = conv_data.zfill(8)
		# conv_data = ''.join(reversed(conv_data))
		# n = b''
		# for b in conv_data:
		# 	m = int(b)
		# 	m = chr(m)
		# 	m = bytes(m, 'utf-8')
		# 	n += m
		# conv_data = n
	
	#convert from binary 
	elif type(data) == bytes and data_type == str:
		conv_data = data.decode()
		conv_data = conv_data.rstrip('\x00')
	elif type(data) == bytes and data_type == int:
		conv_data = int.from_bytes(data, 'little')
	elif type(data) == bytes and data_type == bool:
		conv_data = bool(data[0])

	return conv_data