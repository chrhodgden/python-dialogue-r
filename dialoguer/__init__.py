import os
import subprocess
import threading
import socket
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
	def __init__(self, file_name):
		self.file_name = file_name
		self.file_path = os.path.join(os.getcwd(), file_name)
		self.ext = file_name.split('.')[-1]
		self.conn = None
		self.addr = None
		self.active = False

	def execute_context_script(self):
		context_file = __file__.replace('__init__.py', 'context_script.r')

		# I believe it is possible to pass the R target file path as a system argument.
		# I might should pass the package directory instead/as-well so R can source-import modules from there
		subprocess.run(
			f'Rscript {context_file}',
			cwd = os.getcwd(),
			start_new_session = True
			)

	def establish_connection(self):
		server.listen()
		self.conn, self.addr = server.accept()
	
	def launch_and_connect(self):
		self._connect = threading.Thread(target=self.establish_connection)
		self._launch = threading.Thread(target=self.execute_context_script)

		self._connect.start()
		self._launch.start()
		self._connect.join()

		self.send(self.file_path)
		data = self.recv(True)
		self.active = (data == 'TRUE')
	
	def open(self, wait = True):
		self._open = threading.Thread(target=self.launch_and_connect)
		if wait: self._open.run()
		else: self._open.start()

	def send(self, data, send_data_type = False):
		if send_data_type:
			data_type_name = type(data)
			data_type_name = data_type_name.__name__
			data_type_name = bin_conv(data_type_name)
			self.conn.send(data_type_name)
		bin_data = bin_conv(data)
		self.conn.send(bin_data)

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

	def disconnect_and_close(self):
		self.send('!DISCONNECT')
		self._launch.join()
		self.conn.close()
		self.active = False

	def close(self, wait = True):
		self._close = threading.Thread(target=self.disconnect_and_close)
		if wait: self._close.run()
		else: self._close.start()

