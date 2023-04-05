import idlelib
import os
from subprocess import *

# If I can't find the R path, I could have a dedicated r procedure that finds R.home() and puts that into a text file.

print(os.getcwd())

#open demp.py
# demo_fil = os.path.join(os.getcwd(),'demo.py')
# if os.path.exists(demo_fil):
# 	idle_bat = idlelib.__file__.replace('__init__.py','idle.bat')
# 	Popen(f'{idle_bat} "{demo_fil}"')

tar_fil = os.path.join(os.getcwd(),'demo.r')
print(tar_fil)
if os.path.exists(tar_fil):
	rscript_exe = 'C:/Program Files/R/R-4.2.2/bin/Rscript.exe'
	rscript_exe = 'Rscript'
	print(os.path.exists(rscript_exe))
	run(
		f'{rscript_exe} "{tar_fil}"',
		cwd = os.getcwd(),
		start_new_session = True
		)

