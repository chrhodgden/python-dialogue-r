import os
from subprocess import *

print(os.getcwd())

tar_fil = os.path.join(os.getcwd(),'source_file.py')
print(tar_fil)
if os.path.exists(tar_fil):
	python_cmd = 'Python'
	run(
		f'{python_cmd} {tar_fil}',
		cwd = os.getcwd(),
		start_new_session = True
		)
	
print("end launcher")

