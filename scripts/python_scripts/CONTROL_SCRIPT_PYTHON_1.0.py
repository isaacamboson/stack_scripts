#!/usr/bin/python

#importing the shutil module
import shutil

#creating variables for the source and destination for copying files
source_file = "/home/oracle/scripts/practicedir_isa_sep23/isaac_file.txt"
destination_file = "/home/oracle/scripts/practicedir_isa_sep23/backup"

#creating variables for the source and the destination for the copying directories
source_dir = r"/home/oracle/scripts/practicedir_isa_sep23/backup"
destination_dir = r"/home/oracle/scripts/practicedir_isa_sep23/isaac_main/backup"

#calling the function that copies file from source to destination
shutil.copy(source_file, destination_file)

#calling the function that copies directories from source to destination
shutil.copytree(source_dir, destination_dir)



