#!/usr/bin/python

#Module declaration
import sys
import stack_modules_v1_3 as sm

#variables

if __name__ == "__main__":

	#calling the database backup function from the stack_modules_v1_3 module
	sm.database_backup()

	#calling the copy function from the stack_modules_v1_3 module
	source = "/home/oracle/scripts/practicedir_isa_sep23/isaac_file.txt"
	destination = "/home/oracle/scripts/practicedir_isa_sep23/backup"
	sm.copy_fd(source, destination)


