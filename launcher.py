import os
from subprocess import *
import threading

def execute_source_file(file_name):
	ext = file_name.split('.')
	if ext[1] == 'py': cmd = 'Python'
	elif ext[1] == 'r': cmd = 'RScript'
	run(
		f'{cmd} {file_name}',
		cwd = os.getcwd(),
		start_new_session = True
		)

src_fil_py = threading.Thread(target=execute_source_file, args=['source_file.py'])
src_fil_r = threading.Thread(target=execute_source_file, args=['source_file.r'])

src_fil_r.start()
src_fil_py.start()

src_fil_r.join()
src_fil_py.join()

print("end launcher")

