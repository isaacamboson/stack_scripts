#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_12 as sm
import time

if __name__ == "__main__":

	#variables
#	timestring = time.localtime()
#	TS = time.strftime("%d%m%Y%H%M%S", timestring)

	count_args = len(sys.argv) - 1
	
	if count_args == 0:
		function = input("Please select operation to perform: 'backup', 'database_backup', 'disk_utilization' or 'database_import'? ")
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

		else:
			print("Please select operation to perform: 'backup', 'disk_utilization', 'database_backup' or 'database_import'")

	elif sys.argv[1] == "database_backup" and count_args == 5:
		runner = sys.argv[2]
		backup_base = sys.argv[3]
		schema = sys.argv[4]
		rcp_email = sys.argv[5]
		
		function = sys.argv[1]
		
		#calling the database backup function from the stack_modules_v1_4 module
		status = sm.database_backup(p1=runner, p2=schema, p3=backup_base)
		sm.stack_email(p1=rcp_email, p2=status, p3=function, p4=runner)

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

		status = sm.database_import(p1=runner, p2=schema, p3=dmp_file, p4=directory1)
		sm.stack_email(p1=rcp_email, p2=status, p3=function, p4=runner)

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

	else:
		print("Please select operation to perform: 'backup' or 'database_backup'")



