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
	def __init__(self, file_name, wait = True):
		self.file_name = file_name
		self.file_path = os.path.join(os.getcwd(), file_name)
		self.ext = file_name.split('.')[-1]
		self.uuid = str(uuid.uuid4())
		self.conn = None
		self.addr = None
		self.connected = False
		self.active = False
		if wait: 
			self.open()

	def execute_context_script(self):
		context_file = __file__.replace('__init__.py', 'context_script.r')

		subprocess.run(
			f'Rscript {context_file} {self.uuid} {self.file_path}',
			cwd = os.getcwd(),
			start_new_session = True
			)

	def establish_connection(self):
		while not self.connected:
			server.listen()
			self.conn, self.addr = server.accept()
			uuid_chk = self.recv()
			self.connected = self.uuid == uuid_chk
			self.send(self.uuid)
			if not self.connected:
				self.conn.close()
	
	def open(self):
		self._connect = threading.Thread(target=self.establish_connection)
		self._launch = threading.Thread(target=self.execute_context_script)

		self._connect.start()
		self._launch.start()
		self._connect.join()

		data = self.recv(set_data_type=bool)
		self.active = (data == True)
	
	def send(self, data, send_data_type = False):
		if send_data_type:
			data_type_name = type(data)
			data_type_name = data_type_name.__name__
			data_type_name = bin_conv(data_type_name)
			self.conn.send(data_type_name)
		bin_data = bin_conv(data)
		self.conn.send(bin_data)

	# I still want to consolidate the recv_data_type and set_data_type args
	def recv(self, recv_data_type = False, set_data_type = str):
		if recv_data_type:
			data_type_name = self.conn.recv(HEADER)
			while data_type_name == b'\x00':
				data_type_name = self.conn.recv(HEADER)
			data_type_name = bin_conv(data_type_name, str)
			data_type = data_type_dict[data_type_name]
		else:
			data_type = set_data_type

		data = self.conn.recv(HEADER)
		while data == b'\x00':
			data = self.conn.recv(HEADER)
		
		data = bin_conv(data, data_type)

		return data

	def import_variable(self, var_name):
		self.send(var_name, False)
		val = self.recv(True)
		return val

	def evaluate_expression(self, expr):
		pass

	def close(self):
		self.send('!DISCONNECT')
		self._launch.join()
		self.conn.close()
		self.conn = None
		self.addr = None
		self.connected = False
		self.active = False

