#!/usr/bin/python

import os
import subprocess
import time

while True:
	file_name = "testloop.txt"
	dir = os.getcwd()
	full_path = os.path.join(dir, file_name)

	if file_name not in os.listdir():
		print("checking for file - {}".format(file_name))
		time.sleep(2)
	else:
		print("file found")
		list = subprocess.run("ls -ltr {}".format(full_path), shell=True)
		print(list)
		

#		list = os.system("ls -ltr {}".format(full_path))
#		print(list)
		break


