#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_7 as sm

if __name__ == "__main__":

	#variables


#	function = sys.argv[1]
	count_args = len(sys.argv) - 1
	
	if count_args == 0:
		function = input("Please select operation to perform: 'backup', 'database_backup' or 'disk_utilization'? ")
		if function == "database_backup":
			runner = input("Please provide runner: ")
			schema = input("Please provide backup schema name: ")
			backup_base = input("Please provide backup location for exported schema: ")

			#calling the database backup function from the stack_modules_v1_4 module
			sm.database_backup(runner, schema, backup_base)

		elif function == "backup":
			source = input("Please provide the source file or directory to be copied: ")
			dest = input("Please provide the destination path for file or directory copy: ")

			#calling the copy function from the stack_modules_v1_3 module
			sm.copy_fd(source, dest)
		
		elif function == "disk_utilization":
			disk = input("Please provide disk name: ")
			threshold = input("Please provide the threshold for disk utilization: ")

			#calling the disk utilization function
			sm.disk_maintenance_check_on_prem(disk, threshold)

		else:
			print("Please select operation to perform: 'backup' or 'database_backup'")

	elif sys.argv[1] == "database_backup" and count_args == 4:
		runner = sys.argv[2]
		backup_base = sys.argv[3]
		schema = sys.argv[4]

		#calling the database backup function from the stack_modules_v1_4 module
		sm.database_backup(runner, schema, backup_base)

	elif sys.argv[1] == "database_backup" and count_args != 4:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *runner* *backup location* *schema to be backed up*")

	elif sys.argv[1] == "backup" and count_args == 3:
		source = sys.argv[2]
		dest = sys.argv[3]

		#calling the copy function from the stack_modules_v1_3 module
		sm.copy_fd(source, dest)

	elif sys.argv[1] == "backup" and count_args != 3:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *source directory* *source file* *destination*")

	elif sys.argv[1] == "disk_utilization" and count_args == 3:
		disk = sys.argv[2]
		threshold = sys.argv[3]

		#calling the disk utilization function
		sm.disk_maintenance_check_on_prem(disk, threshold)

	elif sys.argv[1] == "disk_utilization" and count_args != 3:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *disk* *threshold*")	

	else:
		print("Please select operation to perform: 'backup' or 'database_backup'")



