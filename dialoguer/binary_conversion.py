def bin_conv(data, data_type = None):
	conv_data = None
	#convert to binary 
	if type(data) == str and data_type == None:
		conv_data = bytes(data, 'utf-8')
	elif type(data) == int and data_type == None:
		conv_data = data.to_bytes(32, 'little')
	
	#convert from binary 
	elif type(data) == bytes and data_type == str:
		conv_data = data.decode()
		conv_data = conv_data.rstrip('\x00')
	elif type(data) == bytes and data_type == int:
		conv_data = int.from_bytes(data, 'little')
	elif type(data) == bytes and data_type == bool:
		conv_data = bool(data[0])

	return conv_data