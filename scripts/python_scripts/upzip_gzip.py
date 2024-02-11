#!/usr/bin/python

import gzip
import shutil

with gzip.open("/home/oracle/scripts/practicedir_isa_sep23/stack_mike_isaac_011224023743.tar.gz", "rb") as file_in:
	with open("stack_mike_isaac_011224023743.tar", "wb") as file_out:
		shutil.copyfileobj(file_in, file_out)


