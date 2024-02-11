#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_4 as sm

if __name__ == "__main__":

	#variables
	function = sys.argv[1]
	count_args = len(sys.argv) - 1

	if function == "database_backup" and count_args == 4:
		runner = sys.argv[2]
		backup_base = sys.argv[3]
		schema = sys.argv[4]

		#calling the database backup function from the stack_modules_v1_4 module
		sm.database_backup(runner, schema, backup_base)

	elif function == "database_backup" and count_args != 4:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")	
		print("python *scriptname* *function* *runner* *backup location* *schema to be backed up*")

	elif function == "backup" and count_args == 3:
		source = sys.argv[2]
		dest = sys.argv[3]

		#calling the copy function from the stack_modules_v1_3 module
		sm.copy_fd(source, dest)

	elif function == "backup" and count_args != 3:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *source directory* *source file* *destination*")

	else:
		print("Please run this script in the format below:")
		print("python *scriptname* *runner* *backup location* *schema to be backed up* *directory name* *filename* *destination*")

	

