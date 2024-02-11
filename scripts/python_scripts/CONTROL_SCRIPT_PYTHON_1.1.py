#!/usr/bin/python

#importing modules
import os
import shutil
import sys

#creating variables for the source and destination for copying files
source_fd = sys.argv[1]
destination_fd = sys.argv[2]

#calling the function that copies file from source to destination
if os.path.isfile(source_fd):
	shutil.copy(source_fd, destination_fd)
elif os.path.isdir(source_fd):
	shutil.copytree(source_fd, destination_fd)



