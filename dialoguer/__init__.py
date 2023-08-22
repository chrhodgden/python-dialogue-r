import os
import subprocess
import threading
import socket
import uuid
from .binary_conversion import bin_conv
from .data_type_ref import data_type_dict

HEADER = 2048
PORT = 6011
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# could there be a defined sub-class that has all the sockets connection functions?
# then the dialogue class launches and connects and loops
class Dialogue:
	def __init__(self, file_name, wait = False, clean_elements = True):
		self.file_name = os.path.basename(file_name)
		if bool(os.path.dirname(file_name)):
			self.file_path = file_name
		else:
			self.file_path = os.path.join(os.getcwd(), file_name)
		self.ext = file_name.split('.')[-1]
		self.uuid = str(uuid.uuid4())
		self.conn = None
		self.addr = None
		self.connected = False
		self.active = False
		# This attribute will be for 
		self.clean_elements = clean_elements
		if not wait: 
			self.open()

	def execute_context_script(self):
		context_file = __file__.replace('__init__.py', 'dialoguer.r')

		subprocess.run(
			f'Rscript {context_file} {self.uuid} {self.file_path}',
			cwd = os.getcwd(),
			start_new_session = True
			)

	def establish_connection(self):
		while not self.connected:
			server.listen()
			self.conn, self.addr = server.accept()
			uuid_chk = self.recv()[0]
			recv_chk = self.sub_recv(data_type=bool)
			self.connected = self.uuid == uuid_chk
			self.send(self.uuid)
			if not self.connected:
				self.conn.close()
	
	def open(self):
		self._connect = threading.Thread(target=self.establish_connection)
		self._launch = threading.Thread(target=self.execute_context_script)

		self._launch.start()
		self._connect.start()
		self._connect.join()

		data = self.recv(set_data_type=bool)[0]
		self.active = (data == True)

	def sub_send(self, data):
		bin_data = bin_conv(data)
		self.conn.send(bin_data)

	#need to send as vector or single element
	def send(self, data, send_data_type = False, send_length = False, send_element_names = False):
		
		if send_data_type:
		
			# we only have 1 data typer per data
			if type(data) == list:
				if all(type(elem)==type(data[0]) for elem in data):
					data_type = type(data[0])
			elif type(data) == dict:
				values = list(data.values())
				if all(type(elem)==type(values[0]) for elem in values):
					data_type = type(values[0])
			else:
				data_type = type(data)
			
			data_type_name = data_type.__name__
			self.sub_send(data_type_name)
			recv_chk = self.sub_recv(data_type=bool)
		
		if send_length:
			if type(data) == list or type(data) == dict:
				data_length = len(data)
			else:
				data_length = 1
			self.sub_send(data_length)
			recv_chk = self.sub_recv(data_type=bool)

		# data must be type dict
		if send_element_names:
			keys = data.keys()
			data_names_length = len(keys)
			self.sub_send(data_names_length)
			recv_chk = self.sub_recv(data_type=bool)
			for elem_name in keys:
				bin_elem_name = bin_conv(elem_name)
				self.conn.send(bin_elem_name)
				recv_chk = self.sub_recv(data_type=bool)

		if type(data) == list:
			for elem in data:
				self.sub_send(elem)
				recv_chk = self.sub_recv(data_type=bool)
		elif type(data) == dict:
			values = list(data.values())
			for elem in values:
				self.sub_send(elem)
				recv_chk = self.sub_recv(data_type=bool)
		else:
			self.sub_send(data)
			recv_chk = self.sub_recv(data_type=bool)
		
	def sub_recv(self, data_type = str):
		data = self.conn.recv(HEADER)
		while data == b'\x00':
			data = self.conn.recv(HEADER)
		data = bin_conv(data, data_type)
		return(data)

	# I still want to consolidate the recv_data_type and set_data_type args
	def recv(self, recv_data_type = False, set_data_type = str, recv_length = False, recv_element_names = False):
		data= []
		data_names = []
		if recv_data_type:
			data_type_name = self.sub_recv()
			self.sub_send(True)
			data_type = data_type_dict[data_type_name]
		else:
			data_type = set_data_type

		if recv_length:
			data_length = self.sub_recv(int)
			self.sub_send(True)
		else:
			data_length = 1

		if recv_element_names:
			data_names_length = self.sub_recv(int)
			self.sub_send(True)
			for _ in range(data_names_length):
				elem_name = self.sub_recv()
				self.sub_send(True)
				data_names.append(elem_name)
		else:
			data_names_length = 0

		for _ in range(data_length):
			elem = self.sub_recv(data_type)
			self.sub_send(True)
			data.append(elem)

		if data_length and data_names_length:
			data = dict(zip(data_names, data))

		return data

	def import_variable(self, var_name):
		self.send(1)
		recv_chk = self.recv(set_data_type=bool)[0]
		self.send(var_name, False)
		val = self.recv(True, recv_length=True, recv_element_names=True)
		return val

	def assign_variable(self, var_name, var_val):
		self.send(2)
		recv_chk = self.recv(set_data_type=bool)
		self.send(var_name, False)
		recv_chk = self.recv(set_data_type=bool)
		self.send(var_val, True)
		recv_chk = self.recv(set_data_type=bool)

	def evaluate_expression(self, method_name, *args, **kwargs):
		self.send(3)
		recv_chk = self.recv(set_data_type=bool)
		#send number of arguments
		self.send(len(args))
		recv_chk = self.recv(set_data_type=bool)
		#send number of keyword arguments
		self.send(len(kwargs))
		recv_chk = self.recv(set_data_type=bool)
		#send method name
		self.send(method_name)
		recv_chk = self.recv(set_data_type=bool)
		#send arguments
		for arg in args:
			self.send(arg, True)
			recv_chk = self.recv(set_data_type=bool)
		#send keyword arguments
		for kw in kwargs:
			self.send(kw)
			recv_chk = self.recv(set_data_type=bool)
			self.send(kwargs[kw], True)
			recv_chk = self.recv(set_data_type=bool)
		result = self.recv(True)
		return result

	def save_environment(self, file_name = None):
		self.send(4)
		recv_chk = self.recv(set_data_type=bool)
		
		if file_name == None:
			save_name = self.file_path.replace('.r', '.RData')
		elif bool(os.path.dirname(file_name)):
			save_name = file_name
		else:
			save_name = os.path.join(os.getcwd(), file_name)

		self.send(save_name, False)
		recv_chk = self.recv(set_data_type=bool)

	def close(self):
		self.send(0)
		self._launch.join()
		self.conn.close()
		self.conn = None
		self.addr = None
		self.connected = False
		self.active = False

