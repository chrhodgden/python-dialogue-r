import os
from subprocess import *

print(os.getcwd())

tar_fil = os.path.join(os.getcwd(),'source_file.r')
print(tar_fil)
if os.path.exists(tar_fil):
	rscript_path = 'C:/Program Files/R/R-4.2.2/bin/Rscript.exe'
	print(os.path.exists(rscript_path))
	rscript_cmd = 'Rscript'
	run(
		f'{rscript_cmd} "{tar_fil}"',
		cwd = os.getcwd(),
		start_new_session = True
		)
	
print("end launcher")

