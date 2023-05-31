import os
import subprocess
import threading
import socket

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

def terminate_connection(conn):
	conn.close()

def execute_source_file(file_name):
	ext = file_name.split('.')
	if ext[1] == 'py': cmd = 'Python'
	elif ext[1] == 'r': cmd = 'RScript'

	subprocess.run(
		f'{cmd} {file_name}',
		cwd = os.getcwd(),
		start_new_session = True
		)

def launch_and_connect(file_name, CONN):
	mutable = {}
	connect_ = threading.Thread(target=establish_connection, args=[mutable])
	launch_ = threading.Thread(target=execute_source_file, args=[file_name])

	connect_.start()
	launch_.start()
	connect_.join()

	conn = mutable['conn']
	addr = mutable['addr']
	CONN['conn'] = mutable['conn']
	CONN['addr'] = mutable['addr']
	return conn, addr

def disconnect_and_close(file_name):
	pass

CONN_PY = {}
src_fil_py = threading.Thread(target=launch_and_connect, args=['source_file.py', CONN_PY])
#src_fil_r = threading.Thread(target=execute_source_file, args=['source_file.r'])

#src_fil_r.start()
src_fil_py.start()

#src_fil_r.join()
src_fil_py.join()
conn_py = CONN_PY['conn']

msg = recv_msg(conn_py)
print(msg)

msg = "goodbye"
send_msg(conn_py, msg)

print("end launcher")

