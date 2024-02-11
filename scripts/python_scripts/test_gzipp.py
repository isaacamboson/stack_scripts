#!/usr/bin/python

import os
import gzip
import time
import shutil


def gzipp(a_path):

	timestring = time.localtime()
	TS = time.strftime("%d%m%Y%H%M%S", timestring)

	with open(a_path, 'rb') as file_in:
		new_path = a_path + ".gz"
		with gzip.open(new_path, 'wb') as file_out:
			shutil.copyfileobj(file_in, file_out)
		print(new_path)
gzipp("/home/oracle/scripts/practicedir_isa_sep23/stack_mike_isaac_011224023743_2.dmp")



