#!/usr/bin/python

#importing modules
import os
import shutil
import sys

#creating variables for the source and destination for copying files
source_fd = sys.argv[1]
destination_fd = sys.argv[2]

#calling the function that copies file or directory from source to destination
def copy_fd(src, dest):
	if os.path.isfile(src):
		shutil.copy(src, dest)
	elif os.path.isdir(src):
		shutil.copytree(src, dest)

copy_fd(source_fd, destination_fd)


