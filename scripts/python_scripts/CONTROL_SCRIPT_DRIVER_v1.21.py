#!/usr/bin/python

#Module declaration
import os
import sys
import stack_modules_v1_21 as sm
import time
import datetime
import cx_Oracle
import boto3, botocore
from botocore.exceptions import ClientError
import creds as c

if __name__ == "__main__":

	#variables declaration

	count_args = len(sys.argv) - 1
	
	if count_args == 0:
		function = input("Please select operation to perform: 'backup', 'database_backup', 'disk_utilization', 'database_import' or 'database_migration'? ")
		if function == "database_backup":
			inp_runner = input("Please provide runner: ")
			inp_schema = input("Please provide backup schema name: ")
			inp_directory1 = input("Please provide database logical directory for export: ")
			inp_backup_base = input("Please provide backup location for exported schema: ")
			inp_OP_NAME = input("Please provide the name of this operation: ")
			inp_OP_STATUS = input("Please provide the operation status: ")

			#calling the database backup function from the stack_modules_v1_4 module
			sm.database_backup(runner=inp_runner, schema=inp_schema, directory1=inp_directory1, backup_base=inp_backup_base, OP_NAME=inp_OP_NAME, OP_STATUS=inp_OP_STATUS)

		elif function == "backup":
			source = input("Please provide the source file or directory to be copied: ")
			dest = input("Please provide the destination path for file or directory copy: ")

			#calling the copy function from the stack_modules_v1_3 module
			sm.copy_fd(source, dest)
		
		elif function == "disk_utilization":
			inp_disk = input("Please provide disk name: ")
			inp_thresh_sm = input("Please provide the threshold for 'WARNING' alert: ")
			inp_thresh_bg = input("Please provide the threshold for 'CRITICAL' alert: ")
			# inp_schema = input("Please provide schema name: ")
			inp_runner = input("Please provide runner name: ")
			inp_OP_NAME = input("Please provide the name of this operation: ")
			inp_OP_STATUS = input("Please provide the operation status: ")

			#calling the disk utilization function
			sm.disk_maintenance_check_on_prem(disk=inp_disk, thresh_sm=inp_thresh_sm, thresh_bg=inp_thresh_bg, runner = inp_runner, OP_NAME=inp_OP_NAME, OP_STATUS=inp_OP_STATUS)

		elif function == "database_import":
			inp_runner = input("Please provide runner: ")
			inp_schema = input("Please provide schema name: ")
			inp_dmp_file = input("Please provide dump file name: ")
			inp_directory1 = input("Please provide database logical directory for export: ")
			inp_backup_base = input("Please provide the directory where dump file from export will be placed: ")
			inp_OP_NAME = input("Please provide the name of this operation: ")
			inp_OP_STATUS = input("Please provide the operation status: ")
			
			#calling the database migration function
			sm.database_import(runner=inp_runner, schema=inp_schema, dmp_file=inp_dmp_file, directory1=inp_directory1, backup_base=inp_backup_base, OP_NAME=inp_OP_NAME, OP_STATUS=inp_OP_STATUS)		

		elif function == "database_migration":
			inp_runner = input("Please provide runner: ")
			inp_schema = input("Please provide schema name: ")
			inp_directory1 = input("Please provide database logical directory for export: ")
			inp_backup_base = input("Please provide the directory where dump file from export will be placed: ")
			inp_OP_NAME = input("Please provide the name of this operation: ")
			inp_OP_STATUS = input("Please provide the operation status: ")

			#calling the database migration function
			sm.database_migration(runner=inp_runner, schema=inp_schema, directory1=inp_directory1, backup_base=inp_backup_base, OP_NAME=inp_OP_NAME, OP_STATUS=inp_OP_STATUS)		

		else:
			print("Please select operation to perform: 'backup', 'disk_utilization', 'database_backup', 'database_import' or 'database_migration'.")

	elif sys.argv[1] == "database_backup" and count_args == 7:
		runner = sys.argv[2]
		schema = sys.argv[3]
		directory1 = sys.argv[4]
		backup_base = sys.argv[5]
		OP_NAME = sys.argv[6]
		OP_STATUS = sys.argv[7]		

		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = sys.argv[7], OP_STARTTIME=OP_STARTTIME)

		#assigning the return value from the database export/backup run
		OP_STATUS = sm.database_backup(runner=sys.argv[2], schema=sys.argv[3], directory1=sys.argv[4], backup_base=sys.argv[5])

		#checking the condition of the return value from database export/backup
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "database_backup" and count_args != 7:
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

	elif sys.argv[1] == "disk_utilization" and count_args == 7:
		disk = sys.argv[2]
		thresh_sm = sys.argv[3]
		thresh_bg = sys.argv[4]
		runner = sys.argv[5]
		OP_NAME = sys.argv[6]
		OP_STATUS = sys.argv[7]

		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[5], OP_NAME = sys.argv[6], OP_STATUS = sys.argv[7], OP_STARTTIME=OP_STARTTIME)

		#calling the disk utilization function
		OP_STATUS = sm.disk_maintenance_check_on_prem(disk=sys.argv[2], thresh_sm=sys.argv[3], thresh_bg=sys.argv[4], runner = sys.argv[5])

		#checking the condition of the return value from database export/backup
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[5], OP_NAME = sys.argv[6], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "disk_utilization" and count_args != 7:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *disk* *threshold 1* *threshold 2*")	


	elif sys.argv[1] == "untar_unzip" and count_args == 3:
		tarz_file = sys.argv[2]
		untar_path = sys.argv[3]
		sm.unzip_untar(tarz_file, untar_path)	


	elif sys.argv[1] == "untar_unzip" and count_args != 3:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *file to untar/unzip* *dest path for the untarred/unzipped files*")


	elif sys.argv[1] == "database_import" and count_args == 8:
		runner = sys.argv[2]
		schema = sys.argv[3]
		dmp_file = sys.argv[4]
		directory1 = sys.argv[5]
		backup_base = sys.argv[6]
		OP_NAME = sys.argv[7]
		OP_STATUS = sys.argv[8]
				
		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[7], OP_STATUS = sys.argv[8], OP_STARTTIME=OP_STARTTIME)

		#assigning the return value from the database export/backup run
		OP_STATUS = sm.database_import(runner=sys.argv[2], schema=sys.argv[3], dmp_file=sys.argv[4], directory1=sys.argv[5], backup_base=sys.argv[6])

		#checking the condition of the return value from database export/backup
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[7], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[7], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "database_import" and count_args != 8:
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


	elif sys.argv[1] == "database_migration" and count_args == 7:
		runner = sys.argv[2]
		schema = sys.argv[3]
		directory1 = sys.argv[4]
		backup_base = sys.argv[5]
		OP_NAME = sys.argv[6]
		OP_STATUS = sys.argv[7]

		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = sys.argv[7], OP_STARTTIME=OP_STARTTIME)

		#assigning the return value from the database export/backup run
		OP_STATUS = sm.database_migration(runner=sys.argv[2], schema=sys.argv[3], directory1=sys.argv[4], backup_base=sys.argv[5])

		#checking the condition of the return value from database export/backup
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			sm.db_connection(runner = sys.argv[2], OP_NAME = sys.argv[6], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "database_migration" and count_args != 7:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *runner* *schema name* *directory for dump file* *directory for backup*")


	elif sys.argv[1] == "db_connection" and count_args == 6:
		OP_ID = sys.argv[2]
		OP_NAME = sys.argv[3]
		runner = sys.argv[4]
		STATUS = sys.argv[5]
		OP_TYPE = sys.argv[6]

		sm.db_connection(OP_ID=sys.argv[2], OP_NAME=sys.argv[3], runner=sys.argv[4], STATUS = sys.argv[5], OP_TYPE=sys.argv[6])

	
	elif sys.argv[1] == "db_connection" and count_args != 6:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *function* *OP_ID* *OP_NAME* *runner* *STATUS* *OP_TYPE*")


	elif sys.argv[1] == "create_aws_user" and count_args == 6:
		service = sys.argv[2]
		aws_user = sys.argv[3]
		runner = sys.argv[4]
		OP_NAME = sys.argv[5]
		OP_STATUS = sys.argv[6]

		#declaring the initial operation starttime
		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = sys.argv[6], OP_STARTTIME=OP_STARTTIME)

		#calling the AWS create-user function
		OP_STATUS = sm.aws_create_user(service = sys.argv[2], aws_user = sys.argv[3])

		#checking the condition of the return value from create_aws_user function to determine OP_STATUS and OPENDTIME for DB update
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "COMPLETED" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		#checking for errors in the aws_create_user function 
		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "ERROR" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "create_aws_user" and count_args != 6:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *operation* *service* *aws_user* *runner* *OP_NAME* *OP_STATUS*")


	elif sys.argv[1] == "create_aws_group" and count_args == 6:
		service = sys.argv[2]
		group_name = sys.argv[3]
		runner = sys.argv[4]
		OP_NAME = sys.argv[5]
		OP_STATUS = sys.argv[6]

		#declaring the initial operation starttime
		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = sys.argv[6], OP_STARTTIME=OP_STARTTIME)

		#calling the AWS create-group function
		OP_STATUS = sm.aws_create_group(service = sys.argv[2], group_name = sys.argv[3])

		#checking the condition of the return value from create_aws_user function to determine OP_STATUS and OPENDTIME for DB update
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "COMPLETED" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "ERROR" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "create_aws_group" and count_args != 6:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *operation* *service* *group name* *runner* *OP_NAME* *OP_STATUS*")


	elif sys.argv[1] == "add_user_to_group" and count_args == 7:
		service = sys.argv[2]
		user_name = sys.argv[3]
		group_name = sys.argv[4]
		runner = sys.argv[5]
		OP_NAME = sys.argv[6]
		OP_STATUS = sys.argv[7]

		#declaring the initial operation starttime
		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[5], OP_NAME = sys.argv[6], OP_STATUS = sys.argv[7], OP_STARTTIME=OP_STARTTIME)

		#calling the AWS create-group function
		OP_STATUS = sm.add_user_to_group(service = sys.argv[2], user_name = sys.argv[3], group_name = sys.argv[4])

		#checking the condition of the return value from create_aws_user function to determine OP_STATUS and OPENDTIME for DB update
		if OP_STATUS == "COMPLETED":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "COMPLETED" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[5], OP_NAME = sys.argv[6], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)

		elif OP_STATUS == "ERROR":
			timestring3 = datetime.datetime.now()
			ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
			OP_ENDTIME = ENDTIME3.upper()
			print("End Time: {}".format(OP_ENDTIME))

			#calling the db_connection function to update the database with "ERROR" OP_STATUS and OP_ENDTIME
			sm.db_connection(runner = sys.argv[5], OP_NAME = sys.argv[6], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	elif sys.argv[1] == "add_user_to_group" and count_args != 7:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *operation* *service* *user_name* *group name* *runner* *OP_NAME* *OP_STATUS*")

			
	elif sys.argv[1] == "aws_migrate_users" and count_args == 6:
		service = sys.argv[2]
		group_name = sys.argv[3]
		runner = sys.argv[4]
		OP_NAME = sys.argv[5]
		OP_STATUS = sys.argv[6]

		#declaring the initial operation starttime
		timestring = datetime.datetime.now()
		STARTTIME = timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = STARTTIME.upper()
		print("Start Time: {}".format(OP_STARTTIME))

		#calling the db_connection function to input start-time, runner, op_name and status into database
		sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = sys.argv[6], OP_STARTTIME=OP_STARTTIME)

		#calling the AWS create-group function and adding Admin policy
		sm.aws_create_group(service = sys.argv[2], group_name = sys.argv[3])

		#calling the db_connection function to input start-time, runner, op_name and status into database
		connection = cx_Oracle.connect(user=c.apexdbdb_user, password=c.apexdbdb_password, dsn=c.db_name)
		print(connection.version)

		#establishing connection to the database to pull database users, to be used to create users in AWS
		cursor = connection.cursor()
		cursor.execute("""select username from all_users where username like '%SEP23'""")
		db_usernames = cursor.fetchall()

		#closing database connection(s)
		connection.commit()
		cursor.close()
		connection.close()

		#looping through the list of users pulled from database to create each AWS user and add AWS user to AWS group
		try:
			for each_username in db_usernames:
				db_user = each_username[0]
				print(db_user)

				#calling the AWS create-user function in the loop for each database user
				sm.aws_create_user(service = sys.argv[2], aws_user = db_user)

				#calling the AWS create-group function
				sm.add_user_to_group(service = sys.argv[2], group_name = sys.argv[3], user_name = db_user)


			#logging endtime of operation into the database
			OP_STATUS = "COMPLETED"
			if OP_STATUS == "COMPLETED":
				timestring3 = datetime.datetime.now()
				ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
				OP_ENDTIME = ENDTIME3.upper()
				print("End Time: {}".format(OP_ENDTIME))

				#calling the db_connection function to update the database with "COMPLETED" OP_STATUS and OP_ENDTIME
				sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "COMPLETED", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


		#checking for errors and logging endtime of operation into database when an error occurs as well
		except Exception as e:
			print("ERROR! {}".format(e))
			OP_STATUS = "ERROR"
			if OP_STATUS == "ERROR":
				timestring3 = datetime.datetime.now()
				ENDTIME3 = timestring3.strftime("%d-%b-%y %I.%M.%S.%f %p")
				OP_ENDTIME = ENDTIME3.upper()
				print("End Time: {}".format(OP_ENDTIME))

				#calling the db_connection function to update the database with "ERROR" OP_STATUS and OP_ENDTIME
				sm.db_connection(runner = sys.argv[4], OP_NAME = sys.argv[5], OP_STATUS = "ERROR", OP_STARTTIME=OP_STARTTIME, OP_ENDTIME=OP_ENDTIME)


	#rainy day scenario for when operation is correct - "aws_migrate_users", but the # of command line arguments is outside of required - 6
	elif sys.argv[1] == "aws_migrate_users" and count_args != 6:
		print("You have provided the wrong number of command line arguments.")
		print("Please run this script in the format below:")
		print("python *scriptname* *operation* *service* *group name* *runner* *OP_NAME* *OP_STATUS*")

	#rainy day scenario for when operation is wrongly selected. Please select right operation and provide correct command line arguments
	else:
		print("Please select operation to perform: 'backup', 'database_backup', 'disk_utilization', 'database_import', 'database_migration', 'create_aws_user', 'create_aws_group' or 'add_user_to_group'")



