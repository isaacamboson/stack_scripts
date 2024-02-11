#!/usr/bin/python

import gzip


with gzip.open("stack_mike_isaac_011224023743_2.dmp.gz", "rb") as f:
	file_content = f.read()
	print(file_content)

un_zipp()
