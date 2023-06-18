import os
import subprocess
import threading
import socket
from . import binary_conversion

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
		data = self.recv()
		data = binary_conversion.convert_from_binary(data, type('s'))
		self.active = (data == 'TRUE')
	
	def open(self, wait = True):
		self._open = threading.Thread(target=self.launch_and_connect)
		if wait: self._open.run()
		else: self._open.start()

	# Could I add an optional data_type argument that sends the data type as string?
	# Would be used for steps for when data_type is expected by R.
	def send(self, data):
		# I should probably put this reversal in the convert_to_binary method.
		bin_data = reversed(data)
		bin_data = "".join(bin_data)
		bin_data = binary_conversion.convert_to_binary(bin_data)
		self.conn.send(bin_data)

	# Could add an optional boolean expect_data_type argument that receives data type as string.
	# should there be an expected data type arg that specifies a known data type?
	def recv(self):
		data = self.conn.recv(HEADER)
		while data == b'\x00':
			data = self.conn.recv(HEADER)			
		return data

	def import_variable(self, var_name):
		self.send(var_name)
		val = self.recv()
		val = binary_conversion.convert_from_binary(val, type('s'))
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

