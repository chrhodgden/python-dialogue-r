import os
import subprocess
import threading
import socket
import time

HEADER = 64
PORT = 6011
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b'!DISSCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def establish_connection(mutable = {}):
	server.listen()
	conn, addr = server.accept()
	mutable['conn'] = conn
	mutable['addr'] = addr
	return conn, addr

def send_msg(conn, msg):
	data = bytes(msg, FORMAT)
	data += b' ' * (HEADER - len(data))
	conn.send(data)

def recv_msg(conn):
	msg = conn.recv(HEADER).strip()
	return msg

def execute_source_file(file_name):
	ext = file_name.split('.')
	if ext[1] == 'py': cmd = 'Python'
	elif ext[1] == 'r': cmd = 'Rscript'

	subprocess.run(
		f'{cmd} {file_name}',
		cwd = os.getcwd(),
		start_new_session = True
		)
	print(f'{file_name} executed')

def launch_and_connect(file_name, CONN):
	connect_ = threading.Thread(target=establish_connection, args=[CONN])
	launch_ = threading.Thread(target=execute_source_file, args=[file_name])

	connect_.start()
	launch_.start()
	connect_.join()

	conn = CONN['conn']
	addr = CONN['addr']
	CONN['launch_'] = launch_
	return conn, addr

def disconnect_and_close(CONN):
	conn = CONN['conn']
	launch_ = CONN['launch_']
	send_msg(conn, '!DISCONNECT')
	print(f'closing {CONN["addr"]}')
	launch_.join()
	print(f'closed {CONN["addr"]}')
	conn.close()

CONN_R = {}
CONN_PY = {}
src_fil_r = threading.Thread(target=launch_and_connect, args=['source_file.r', CONN_R])
src_fil_py = threading.Thread(target=launch_and_connect, args=['source_file.py', CONN_PY])
disc_r = threading.Thread(target=disconnect_and_close, args=[CONN_R])
disc_py = threading.Thread(target=disconnect_and_close, args=[CONN_PY])

src_fil_r.run()
src_fil_py.run()

conn_r = CONN_R['conn']
conn_py = CONN_PY['conn']

msg = recv_msg(conn_r)
print(msg)
msg = recv_msg(conn_py)
print(msg)

for i in range(255):
	msg = f'message {i}'
	send_msg(conn_r, msg)
	send_msg(conn_py, msg)

disc_r.start()
disc_py.start()
disc_r.join()
disc_py.join()

print("end launcher")

