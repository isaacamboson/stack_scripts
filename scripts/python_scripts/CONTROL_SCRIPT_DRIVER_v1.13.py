#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_13 as sm
import time

if __name__ == "__main__":

	#variables

	count_args = len(sys.argv) - 1
	
	if count_args == 0:
		function = input("Please select operation to perform: 'backup', 'database_backup', 'disk_utilization', 'database_import' or 'database_migration'? ")
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

		elif function == "database_import":
			runner = input("Please provide runner: ")
			schema = input("Please provide schema name: ")
			dmp_file = input("Please provide dump file name: ")
			directory1 = input("Please provide directory where dump file is located: ")

			#calling the database import function
			sm.database_import(runner, schema, dmp_file, directory1)		
	
		elif function == "database_migration":
			runner = input("Please provide runner: ")
			schema = input("Please provide schema name: ")
			directory1 = input("Please provide directory where dump file for import will be located: ")
			backup_base = input("Please provide the directory where dump file from export will be placed: ")

			#calling the database migration function
			sm.database_migration(runner, schema, directory1, backup_base)

		else:
			print("Please select operation to perform: 'backup', 'disk_utilization', 'database_backup', 'database_import' or 'database_migration'.")

	elif sys.argv[1] == "database_backup" and count_args == 4:
		runner = sys.argv[2]
		schema = sys.argv[3]
		directory1 = sys.argv[4]
		backup_base = sys.argv[5]

		function = sys.argv[1]

		#calling the database backup function from the stack_modules_v1_4 module
		sm.database_backup(runner, schema, directory1, backup_base)
		sm.stack_email(rcp_email, status, function, runner)

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

	elif sys.argv[1] == "untar_unzip" and count_args == 3:
		tarz_file = sys.argv[2]
		untar_path = sys.argv[3]
		sm.unzip_untar(tarz_file, untar_path)	

	elif sys.argv[1] == "untar_unzip" and count_args != 3:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *file to untar/unzip* *dest path for the untarred/unzipped files*")

	elif sys.argv[1] == "database_import" and count_args == 5:
		runner = sys.argv[2]
		schema = sys.argv[3]
		dmp_file = sys.argv[4]
		directory1 = sys.argv[5]

		function = sys.argv[1]

		sm.database_import(runner, schema, dmp_file, directory1)
		sm.stack_email(rcp_email, status, function, runner)

	elif sys.argv[1] == "database_import" and count_args != 5:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *runner* *dmp file* *directory for dmp file*")

	elif sys.argv[1] == "stack_email" and count_args == 4:
		TO_EMAIL = sys.argv[2]
		SUBJECT = sys.argv[3]
		BODY = sys.argv[4]

		sm.stack_email(TO_EMAIL, SUBJECT, BODY)

	elif sys.argv[1] == "stack_email" and count_args != 4:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *recipient email* *email subject* *email body*")

	elif sys.argv[1] == "database_migration" and count_args == 5:
		runner = sys.argv[2]
		schema = sys.argv[3]
		directory1 = sys.argv[4]
		backup_base = sys.argv[5]

		sm.database_migration(runner, schema, directory1, backup_base)		

	elif sys.argv[1] == "database_migration" and count_args != 5:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *runner* *schema name* *directory for dump file* *directory for backup*")

	else:
		print("Please select operation to perform: 'backup' or 'database_backup'")



