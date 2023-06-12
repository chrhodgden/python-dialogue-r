import os
import subprocess
import threading
import socket

HEADER = 256
PORT = 6011
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b'!DISSCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

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
		msg = self.recv()
		self.active = (msg == b'TRUE')
	
	def open(self, wait = True):
		self._open = threading.Thread(target=self.launch_and_connect)
		if wait: self._open.run()
		else: self._open.start()

	def send(self, msg):
		data = bytes(msg, FORMAT)
		data += b' ' * (HEADER - len(data))
		self.conn.send(data)

	def recv(self):
		msg = self.conn.recv(HEADER).strip()
		while msg == b'\x00':
			msg = self.conn.recv(HEADER).strip()
		return msg

	def import_variable(self, var_name):
		self.send(var_name)
		val = self.recv()
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

