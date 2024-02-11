#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_4 as sm


if __name__ == "__main__":

	#variables
	function = sys.argv[1]
	
	if function == "database_backup":
		runner = sys.argv[2]
		backup_base = sys.argv[3]
		schema = sys.argv[4]

		#calling the database backup function from the stack_modules_v1_4 module
		sm.database_backup(runner, schema, backup_base)
	
	elif function == "backup":
		source = sys.argv[2]
		dest = sys.argv[3]

		#calling the copy function from the stack_modules_v1_4 module
		sm.copy_fd(source, dest)

	else:
		print("Print choose 'backup' or 'database backup'")


