import socket

HEADER = 64
PORT = 6011
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b'!DISSCONNECT'

CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONN.connect(ADDR)

def display_msg(msg):
    print(
        '\033[93m', 
        msg, 
        sep='', 
        end='\033[0m\n'
    )

def send_msg(conn, msg):
	data = bytes(msg, FORMAT)
	data += b' ' * (HEADER - len(data))
	conn.send(data)

def recv_msg(conn):
	msg = conn.recv(HEADER).strip()
	msg = msg.decode(FORMAT)
	return msg

msg = "Initializing Client - Python"
display_msg(msg)

msg = "Initialized Client - Python"
send_msg(CONN, msg)

while msg != '!DISCONNECT':
	msg = recv_msg(CONN)
	display_msg(msg)

CONN.close()