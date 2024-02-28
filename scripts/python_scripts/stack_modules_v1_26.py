#!/usr/bin/python

import os 
import sys
import time
import psutil
import shutil
import subprocess
import gzip
import tarfile
import smtplib
import cx_Oracle
import datetime
import boto3, botocore
from botocore.exceptions import ClientError
import creds as c


timestring = time.localtime()
TS = time.strftime("%d%m%Y%H%M%S", timestring)

#creating a database connection function
def db_connection(**db_conn):

	try:

		if db_conn["OP_STATUS"] == "BEGIN":

			OP_STATUS = "RUNNING"
			
			connection = cx_Oracle.connect(user=c.apexdbdb_user, password=c.apexdbdb_password, dsn=c.db_name)
			print(connection.version)

			cursor = connection.cursor()
			cursor.execute("""insert into prod_activities (OP_STARTTIME, RUNNER, STATUS) values (:OP_STARTTIME_INS, :RUNNER_INS, :STATUS_INS)""", 
					OP_STARTTIME_INS = db_conn["OP_STARTTIME"],
					RUNNER_INS = db_conn["runner"], 
					STATUS_INS = OP_STATUS
					)
			
			cursor.execute("""update prod_activities set OP_ID = (select OP_ID from prod_operations where op_name = :OP_NAME_INS) where OP_STARTTIME = :OP_STARTTIME_INS""", OP_NAME_INS = db_conn["OP_NAME"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])
			cursor.execute("""update prod_activities set MON_EMAIL = (select MONITORING_EMAIL from prod_operations where op_name = :OP_NAME_INS) where OP_STARTTIME = :OP_STARTTIME_INS""", OP_NAME_INS = db_conn["OP_NAME"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])

			connection.commit()
			cursor.close()
			connection.close()

		elif db_conn["OP_STATUS"] == "COMPLETED":

			connection = cx_Oracle.connect(user=c.apexdbdb_user, password=c.apexdbdb_password, dsn=c.db_name)
			print(connection.version)

			cursor = connection.cursor()
			cursor.execute("""update prod_activities set OP_ENDTIME = :OP_ENDTIME_INS where OP_STARTTIME = :OP_STARTTIME_INS""", OP_ENDTIME_INS = db_conn["OP_ENDTIME"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])
			cursor.execute("""update prod_activities set STATUS = :STATUS_INS where OP_STARTTIME = :OP_STARTTIME_INS""", STATUS_INS = db_conn["OP_STATUS"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])
			cursor.execute("""select po.op_id, po.op_name, po.op_type, pa.op_starttime, pa.op_endtime, pa.mon_email
							from prod_operations po
							left join prod_activities pa
							on po.op_id = pa.op_id
							where OP_STARTTIME = :OP_STARTTIME_INS""",
							OP_STARTTIME_INS = db_conn["OP_STARTTIME"]
							)
			
			select_result = cursor.fetchall()
			for each in select_result:
				OP_ID = each[0]
				OP_NAME = each[1]
				OP_TYPE = each[2]
				OP_STARTTIME = each[3]
				OP_ENDTIME = each[4]
				MON_EMAIL = each[5]
				print("OP_ID: {}\nOP_NAME: {}\nOP_TYPE: {}\nOP_STARTTIME: {}\nOP_ENDTIME: {}\nMON_EMAIL: {}".format(OP_ID, OP_NAME, OP_TYPE, OP_STARTTIME, OP_ENDTIME, MON_EMAIL))

			connection.commit()
			cursor.close()
			connection.close()

		elif db_conn["OP_STATUS"] == "ERROR":

			connection = cx_Oracle.connect(user=c.apexdbdb_user, password=c.apexdbdb_password, dsn=c.db_name)
			print(connection.version)

			cursor = connection.cursor()
			cursor.execute("""update prod_activities set OP_ENDTIME = :OP_ENDTIME_INS where OP_STARTTIME = :OP_STARTTIME_INS""", OP_ENDTIME_INS = db_conn["OP_ENDTIME"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])
			cursor.execute("""update prod_activities set STATUS = :STATUS_INS where OP_STARTTIME = :OP_STARTTIME_INS""", STATUS_INS = db_conn["OP_STATUS"], OP_STARTTIME_INS = db_conn["OP_STARTTIME"])
			cursor.execute("""select po.op_id, po.op_name, po.op_type, pa.op_starttime, pa.op_endtime, pa.mon_email
							from prod_operations po
							left join prod_activities pa
							on po.op_id = pa.op_id
							where OP_STARTTIME = :OP_STARTTIME_INS""",
							OP_STARTTIME_INS = db_conn["OP_STARTTIME"]
							)
			
			select_result = cursor.fetchall()
			for each in select_result:
				OP_ID = each[0]
				OP_NAME = each[1]
				OP_TYPE = each[2]
				OP_STARTTIME = each[3]
				OP_ENDTIME = each[4]
				MON_EMAIL = each[5]
				print("OP_ID: {}\nOP_NAME: {}\nOP_TYPE: {}\nOP_STARTTIME: {}\nOP_ENDTIME: {}\nMON_EMAIL: {}".format(OP_ID, OP_NAME, OP_TYPE, OP_STARTTIME, OP_ENDTIME, MON_EMAIL))

			connection.commit()
			cursor.close()
			connection.close()

	except Exception as e:
		print("Database connection function failed to connect! {}".format(e))

		TO_EMAIL = "stackcloud11@mkitconsulting.net"
		SUBJECT = "Database connection ERROR - ISAAC"
		BODY = "Database connection ERROR. Please investigate!"
		stack_email2(TO_EMAIL, SUBJECT, BODY)


#creating a dictionary function for servers
def get_server_dictionary():

	servers={
    "Hosts":{"MKIT-DEV-OEM":"ON-PREM","STACKCLOUD":"CLOUD"},
    "Disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
    "Transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }

	return servers


#creating the function that copies file or directory from source to destination
def copy_fd(src, dest):
	if os.path.isfile(src):
		shutil.copy(src, dest)
	elif os.path.isdir(src):
		source_base = os.path.basename(src)
		dest_d = os.path.join(dest, source_base)
		shutil.copytree(src, dest_d)


#creating a tar function
def tar_func(tar_path, tar_file):
	file_tar = tarfile.open(tar_path, "w")
	file_tar.add(tar_file)
	file_tar.close()


#creating a GZIP function
def g_zipp(a_path):
	with open(a_path, "rb") as file_in:
		new_path = a_path + ".gz"
		with gzip.open(new_path, "wb") as file_out:
			shutil.copyfileobj(file_in, file_out)


#creating the unzip / untar function
#tarz_file - absolute path of file to be untarred and unzipped
#untar_path - dest path for the untarred and unzipped file(s)
def unzip_untar(tarz_file, untar_path):	
	tarz_open = tarfile.open(tarz_file)
	tarz_open.extractall(untar_path)
	tarz_open.close()


#creating the email function
def stack_email2(TO_EMAIL, SUBJECT, BODY):
	FROM = "oracle@MKIT-DEV-OEM.localadmin"
	MSG="\n".join(("From: {}".format(FROM), "To: {}".format(TO_EMAIL), "Subject: {}:\n".format(SUBJECT), "{}".format(BODY)))
	try:
		with smtplib.SMTP('localhost') as my_server:
			my_server.sendmail(FROM, TO_EMAIL, MSG)
			print("Email sent successfully to {}".format(TO_EMAIL))
	except:
		print("Email failed to be sent.")


#creating the email function that uniquely works with DB export and receives CMD line arguments
def stack_email(**email_args):
	FROM = "oracle@MKIT-DEV-OEM.localadmin"
	TO_EMAIL = email_args["p1"]
	if status == "COMPLETED":
		SUBJECT = "{} successfully {} - {}".format(email_args["p3"], email_args["p2"], email_args["p4"])
		BODY = "{} ran by {} was succesfully {}.".format(email_args["p3"], email_args["p4"], email_args["p2"])
		MSG="\n".join(("From: {}".format(FROM), "To: {}".format(TO_EMAIL), "Subject: {}:\n".format(SUBJECT), "{}".format(BODY)))
		try:
			with smtplib.SMTP('localhost') as my_server:
				my_server.sendmail(FROM, TO_EMAIL, MSG)
				print("success email sent to {}".format(TO_EMAIL))
		except:
			print("Email failed to be sent.")
	else:
		SUBJECT = "{} {} - {}".format(function, status, runner)
		BODY = "{} ran by {} was {}. Thus FAILED!".format(function, runner, status)
		MSG="\n".join(("From: {}".format(FROM), "To: {}".format(TO_EMAIL), "Subject: {}:\n".format(SUBJECT), "{}".format(BODY)))
		try:
			with smtplib.SMTP('localhost') as my_server:
				my_server.sendmail(FROM, TO_EMAIL, MSG)
				print("Failure email sent to {}".format(TO_EMAIL))
		except:
			print("Email failed to be sent.")


#creating a database backup function
def database_backup(**bk_args):

	pd_dir = "/home/oracle/scripts/practicedir_isa_sep23"

	#creating a subfolder named with runner in /backup/AWSSEP23/APEXDB/ for future backups
	backup_dir = os.path.join(bk_args["backup_base"], bk_args["runner"]) 

	try:
		#creating the .par file for the database export/backup
		file_add = open("{}/expdp_{}_{}_{}.par".format(pd_dir, bk_args["schema"], bk_args["runner"], TS), "w")
		file_add.write("userid='/ as sysdba'\n")
		file_add.write("schemas={}\n".format(bk_args["schema"]))
		file_add.write("dumpfile={}_{}_{}.dmp\n".format(bk_args["schema"], bk_args["runner"], TS))
		file_add.write("logfile={}_{}_{}.log\n".format(bk_args["schema"], bk_args["runner"], TS))
		file_add.write("directory={}".format(bk_args["directory1"]))
		file_add.close()

		#printing the content of the .par to the STDOUT for verification of database export config details
		file_view = open("{}/expdp_{}_{}_{}.par".format(pd_dir, bk_args["schema"], bk_args["runner"], TS), "r")
		file_content = file_view.read()
		print(file_content)
		file_view.close()

		#checking to see if par file was successfully created and printing the absolute path to STDOUT
		file_name = "expdp_{}_{}_{}.par".format(bk_args["schema"], bk_args["runner"], TS)
		file_path = os.path.join(os.getcwd(), file_name)
		print(file_name)
		print(file_path)

		#creating the .sh file the runs the expdp command for the database export
		export = open("{}/export.sh".format(pd_dir), "w+")
		export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile={}/expdp_{}_{}_{}.par".format(pd_dir, bk_args["schema"], bk_args["runner"], TS))
		export_content = "{}/export.sh".format(pd_dir)
		export.close()

		if os.path.isfile(file_path):
			print(".par file exists.")
		backup_path = os.path.join(backup_dir, TS)
		print(backup_path)

		#creating the back directory for future .dmp files 
		os.makedirs(backup_path)

		#making the .sh file executable and running it to run the database backup
		os.popen("chmod 700 {}".format(export_content))
		subprocess.run(["/bin/bash", export_content])

		#assigning the variables for the tar function
		tar_path = "{}/{}_{}_{}.tar".format(bk_args["backup_base"], bk_args["schema"], bk_args["runner"], TS)
		os.chdir("{}".format(bk_args["backup_base"]))
		tar_file = "{}_{}_{}.dmp".format(bk_args["schema"], bk_args["runner"], TS)

		#calling the tar function
		tar_func(tar_path, tar_file)

		#assigning the variables for the g_zipp function
		a_path = "{}/{}_{}_{}.tar".format(bk_args["backup_base"], bk_args["schema"], bk_args["runner"], TS)

		#calling the g_zipp function
		g_zipp(a_path)

		#assigning the created log file and dumpfiles to variables
		dmp_export = "{}_{}_{}.dmp".format(bk_args["schema"], bk_args["runner"], TS)
		log_export = "{}_{}_{}.log".format(bk_args["schema"], bk_args["runner"], TS)

		fullpath_dmp = os.path.join(bk_args["backup_base"], dmp_export)
		fullpath_log = os.path.join(bk_args["backup_base"], log_export)

		with open(fullpath_log, "r") as r:
			log_check = r.read()
			
			if "successfully completed" in log_check:
				print("Database backup was completed successfully.")

				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database backup has been completed - ISAAC"
				BODY = "The Database backup process has successfully been completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "COMPLETED"
				return status1
			
			else:
				print("Database import was NOT completed.")
		
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database Import FAILED - ISAAC"
				BODY = "The Database Import process was NOT successfully completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "ERROR"
				return status1

	except Exception as e:
		print("Export failed! {}".format(e))

		TO_EMAIL = "stackcloud11@mkitconsulting.net"
		SUBJECT = "Database backup ERROR - ISAAC"
		BODY = "The Database backup ERROR. Please investigate!"
		stack_email2(TO_EMAIL, SUBJECT, BODY)

		status1 = "ERROR"
		return status1


#creating a database import function
def database_import(**imp_args):

	try:
		#exp_log_dir = "/backup/AWSSEP23/APEXDB"
		import_log_dir = "/backup/AWSSEP23/SAMD"
		pd_dir = "/home/oracle/scripts/practicedir_isa_sep23"
		
		#copying the .tar.gz from the DB export output location to the import location for the SAMD DB
		src = "{}/stack_temp_ISAAC_05022024025337.tar.gz".format(imp_args["backup_base"])
		dest = "{}".format(import_log_dir)

		#calling the copy function
		copy_fd(src, dest)	

		#untar and unzipping the .tar.gz file to obtain to the .dmp file for the import
		tarz_file = "{}/stack_temp_ISAAC_05022024025337.tar.gz".format(import_log_dir)
		untar_path = "{}".format(import_log_dir)

		#calling the unzip / untar function
		unzip_untar(tarz_file, untar_path)
	
		#creating the .par file for the import
		file_impar = open("{}/impdp_{}_stack_{}_{}.par".format(pd_dir, imp_args["schema"], imp_args["runner"], TS), "w")
		file_impar.write("userid='/ as sysdba'\n")
		file_impar.write("schemas={}\n".format(imp_args["schema"]))
		file_impar.write("remap_schema={}:{}_{}_migrated\n".format(imp_args["schema"], imp_args["schema"], imp_args["runner"]))
		file_impar.write("dumpfile=stack_temp_ISAAC_05022024025337.dmp\n")
		file_impar.write("logfile=impdp_{}_{}_{}.log\n".format(imp_args["schema"], imp_args["runner"], TS))
		file_impar.write("directory={}\n".format(imp_args["directory1"]))
		file_impar.write("table_exists_action=replace")
		file_impar.close()

		file_rd = open("{}/impdp_{}_stack_{}_{}.par".format(pd_dir, imp_args["schema"], imp_args["runner"], TS), "r")
		file_content = file_rd.read()
		print(file_content)
		file_rd.close()

		#creating the .sh file that runs the impdp command with .par file for DB import
		import_sh = open("{}/import_par.sh".format(pd_dir), "w+")
		import_sh.write(". /home/oracle/scripts/oracle_env_SAMD.sh\nimpdp parfile={}/impdp_{}_stack_{}_{}.par".format(pd_dir, imp_args["schema"], imp_args["runner"], TS))
		import_content = "{}/import_par.sh".format(pd_dir)
		import_sh.close()

		import_rd = open("{}/import_par.sh".format(pd_dir), "r")
		file_conts = import_rd.read()
		print(file_conts)
		import_rd.close()	

		#making the .sh file executable and running it to run the DB import
		os.popen("chmod 777 {}".format(import_content))
		subprocess.run(["/bin/bash", import_content])

		#assigning the created logfile to variable
		import_logfile = "impdp_{}_{}_{}.log".format(imp_args["schema"], imp_args["runner"], TS)
		full_importlog = os.path.join(import_log_dir, import_logfile)

		with open(full_importlog, "r") as r:
			log_check = r.read()
			if "completed" in log_check:
				print("Database import was completed.")

				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database Import has been completed - ISAAC"
				BODY = "The Database Import process has successfully been completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "COMPLETED"
				return status1

			else:
				print("Database import was NOT completed.")
		
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database Import FAILED - ISAAC"
				BODY = "The Database Import process was NOT successfully completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "ERROR"
				return status1

	except Exception as e:
		print("Import failed! {}".format(e))

		TO_EMAIL = "stackcloud11@mkitconsulting.net"
		SUBJECT = "Database Import ERROR - ISAAC"
		BODY = "The Database Import ERROR. Please investigate!"
		stack_email2(TO_EMAIL, SUBJECT, BODY)

		status1 = "ERROR"
		return status1
	

#creating the database migration function
def database_migration(**mg_args):
	
	try:
		#calling the database export function
		database_backup(**mg_args)

		exp_log_dir = "/backup/AWSSEP23/APEXDB"
		import_log_dir = "/backup/AWSSEP23/SAMD"
		pd_dir = "/home/oracle/scripts/practicedir_isa_sep23"
	
		#copying the .tar.gz from the DB export output location to the import location for the SAMD DB
		src = "{}/{}_{}_{}.tar.gz".format(exp_log_dir, mg_args["schema"], mg_args["runner"], TS)
		dest = "{}".format(import_log_dir)

		#calling the copy function
		copy_fd(src, dest)	

		#untar and unzipping the .tar.gz file to obtain to the .dmp file for the import
		tarz_file = "{}/{}_{}_{}.tar.gz".format(import_log_dir, mg_args["schema"], mg_args["runner"], TS)
		untar_path = "{}".format(import_log_dir)

		#calling the unzip / untar function
		unzip_untar(tarz_file, untar_path)
	
		#creating the .par file for the import
		file_impar = open("{}/impdp_{}_stack_{}_{}.par".format(pd_dir, mg_args["schema"], mg_args["runner"], TS), "w")
		file_impar.write("userid='/ as sysdba'\n")
		file_impar.write("schemas={}\n".format(mg_args["schema"]))
		file_impar.write("remap_schema={}:{}_{}_migrated\n".format(mg_args["schema"], mg_args["schema"], mg_args["runner"]))
		file_impar.write("dumpfile={}_{}_{}.dmp\n".format(mg_args["schema"], mg_args["runner"], TS))
		file_impar.write("logfile=impdp_{}_{}_{}.log\n".format(mg_args["schema"], mg_args["runner"], TS))
		file_impar.write("directory={}\n".format(mg_args["directory1"]))
		file_impar.write("table_exists_action=replace")
		file_impar.close()

		file_rd = open("{}/impdp_{}_stack_{}_{}.par".format(pd_dir, mg_args["schema"], mg_args["runner"], TS), "r")
		file_content = file_rd.read()
		print(file_content)
		file_rd.close()

		#creating the .sh file that runs the impdp command with .par file for DB import
		import_sh = open("{}/import_par.sh".format(pd_dir), "w+")
		import_sh.write(". /home/oracle/scripts/oracle_env_SAMD.sh\nimpdp parfile={}/impdp_{}_stack_{}_{}.par".format(pd_dir, mg_args["schema"], mg_args["runner"], TS))
		import_content = "{}/import_par.sh".format(pd_dir)
		import_sh.close()

		import_rd = open("{}/import_par.sh".format(pd_dir), "r")
		file_conts = import_rd.read()
		print(file_conts)
		import_rd.close()	

		#making the .sh file executable and running it to run the DB import
		os.popen("chmod 777 {}".format(import_content))
		subprocess.run(["/bin/bash", import_content])

		#assigning the created logfile to variable
		import_logfile = "impdp_{}_{}_{}.log".format(mg_args["schema"], mg_args["runner"], TS)
		full_importlog = os.path.join(import_log_dir, import_logfile)

		#reading the import log to see if operation was completed successfully or not
		with open(full_importlog, "r") as r:
			log_check = r.read()
			if "completed" in log_check:
				print("Database import was completed.")

				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database Import has been completed - ISAAC"
				BODY = "The Database Import process has successfully been completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "COMPLETED"
				return status1

			else:
				print("Database import was NOT completed.")
		
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database Import FAILED - ISAAC"
				BODY = "The Database Import process was NOT successfully completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "ERROR"
				return status1

	except Exception as e:
		print("Database Migration ERROR! {}".format(e))

		TO_EMAIL = "stackcloud11@mkitconsulting.net"
		SUBJECT = "Database Migration ERROR - ISAAC"
		BODY = "The Database MIgration ERROR. Please investigate!"
		stack_email2(TO_EMAIL, SUBJECT, BODY)

		status1 = "ERROR"
		return status1


#creating a disk utilization check function
def disk_maintenance_check_on_prem(**disk_util):

	try:
		while True:
			disk_check = shutil.disk_usage(disk_util["disk"])
			percentage_used = disk_check.used / disk_check.total * 100
			l_thresh = int(disk_util["thresh_sm"])
			h_thresh = int(disk_util["thresh_bg"])

			#check condition if percentage used is less than higher threshold and higher threshold
			if percentage_used > l_thresh and percentage_used < h_thresh:
				print("WARNING ALERT! The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
				print("This is above the {}% warning threshold. Please look into this.".format(l_thresh))
				
				#sending email alerts
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "WARNING ALERT - {} is at {:.0f}% - ISAAC".format(disk_util["disk"], percentage_used)
				BODY = "Please triage {} as disk is above the {}% threshold.".format(disk_util["disk"], l_thresh)
				stack_email2(TO_EMAIL, SUBJECT, BODY)			
				time.sleep(10)

			#checking condition if percentage used is greater than higher threshold
			elif percentage_used > h_thresh:
				print("CRITICAL ALERT! The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
				print("This is above the {}% CRITICAL threshold. Please address immediately.".format(h_thresh))

				#sending email alerts
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "CRITICAL ALERT - {} is at {:.0f}% - ISAAC".format(disk_util["disk"], percentage_used)
				BODY = "Please triage {} IMMEDIATELY as disk is above the {}% threshold.".format(disk_util["disk"], h_thresh)
				stack_email2(TO_EMAIL, SUBJECT, BODY)
				time.sleep(60 * 1)

			#checking condition if percentage used is under all thresholds
			elif percentage_used < l_thresh:
				print("The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
				print("This is below the {}% threshold.".format(l_thresh))

				#sending email alerts
				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "{} is below the {}% threshold - ISAAC".format(disk_util["disk"], l_thresh)
				BODY = "No action needed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

				status1 = "COMPLETED"
				return status1

				break
			
	except Exception as e:
		print("Disk Monitoring ERROR! {}".format(e))

		TO_EMAIL = "stackcloud11@mkitconsulting.net"
		SUBJECT = "Database Monitoring ERROR - ISAAC"
		BODY = "The Database Monitoring ERROR. Please investigate!"
		stack_email2(TO_EMAIL, SUBJECT, BODY)

		status1 = "ERROR"
		return status1
	

def aws_create_user(**args):
	try:
		iam_client = boto3.client(args["service"],
							aws_access_key_id=c.aws_access_key_id, 
							aws_secret_access_key=c.aws_secret_access_key
							)
		# iam = boto3.client("iam")
		response = iam_client.create_user(UserName = args["aws_user"])
		print(response)
		status1 = "COMPLETED"
		return status1

	except ClientError as error:
		print(error.response)
		if error.response["Error"]["Code"] == "EntityAlreadyExists":
			print("User already exists... Use the same user?")
			val = input("Enter (y or n): ")
			if val == "y":
				print("You want to use the same user")
				pass
				status1 = "ERROR"
				return status1
			else:
				print("You want to create a new user")
				new_user = input("Enter User Name: ")
				response = iam_client.create_user(UserName = new_user)
				print(response)
				status1 = "ERROR"
				return status1
		else:
			print("Unexpected error occured while creating user... exiting from here", error)
			#return "User could not be created", error
			status1 = "ERROR"
			return status1
		

def aws_create_group(**args):
	try:
		iam_client = boto3.client(args["service"],
							aws_access_key_id=c.aws_access_key_id, 
							aws_secret_access_key=c.aws_secret_access_key
							)
		response = iam_client.create_group(GroupName=args["group_name"])
		print(response)

		response1 = iam_client.attach_group_policy(
			GroupName = args["group_name"],
			PolicyArn = "arn:aws:iam::aws:policy/AdministratorAccess"
		)
		print(response1)

		status1 = "COMPLETED"
		return status1

	except ClientError as error:
		print(error.response)
		if error.response["Error"]["Code"] == "EntityAlreadyExists":
			print("Group already exists... Use the same group name?")
			value1 = input("Enter (y or n): ")
			if value1 == "y":
				print("You want to use the same group name")
				pass

			else:
				print("You want to create a new group")
				new_group = input("Enter Group Name: ")
				response = iam_client.create_group(GroupName = new_group)
				print(response)

				response1 = iam_client.attach_group_policy(
				GroupName = new_group,
				PolicyArn = "arn:aws:iam::aws:policy/AdministratorAccess"
				)
				print(response1)

				status1 = "COMPLETED"
				return status1
		else:
			print("Unexpected error occured while creating group... exiting from here", error)
			#return "Group could not be created", error

			status1 = "ERROR"
			return status1
				

def add_user_to_group(**args):
	try:
		iam_client = boto3.client(args["service"],
							aws_access_key_id=c.aws_access_key_id, 
							aws_secret_access_key=c.aws_secret_access_key
							)
		response = iam_client.add_user_to_group(
			GroupName = args["group_name"],
			UserName = args["user_name"]
		)
		print(response)

		try:
			response1 = iam_client.create_login_profile(
				UserName = args["user_name"],
				Password = "Stackinc987",
				PasswordResetRequired=False
			)
			print(response1)

		except ClientError as error:
			print(error.response)

			if error.response["Error"]["Code"] == "EntityAlreadyExists":
				status1 = "COMPLETED"
				return status1

		status1 = "COMPLETED"
		return status1

	except ClientError as error:
		print(error.response)

		#checking if user does not exist
		if error.response["Error"]["Message"] == "The user with name {} cannot be found.".format(args["user_name"]):
			print("User does not exists... Would you like to create user?")
			value1 = input("Enter (y or n): ")
			if value1 == "y":
				print("You want to create a new user")
				new_user = input("Enter User Name: ")
				response = iam_client.create_user(UserName = new_user)
				print(response)

				#creating login profile for newly created user
				response1 = iam_client.create_login_profile(
					UserName = new_user,
					Password = "Stackinc987",
					PasswordResetRequired=False
				)
				print(response1)

				try:
					#group exists but user does not exist and was newly created. Adding user to group
					iam_client = boto3.client(args["service"])
					response = iam_client.add_user_to_group(
						GroupName = args["group_name"],
						UserName = new_user
					)
					print(response)

					status1 = "COMPLETED"
					return status1

				except ClientError as error:
					print(error.response)

					#group and user do not exist. they were both newly created.
					if error.response["Error"]["Message"] == "The group with name {} cannot be found.".format(args["group_name"]):
						print("Group name does not exist... Would you like to create a new group?")
						value2 = input("Enter (y or n): ")
						if value2 == "y":
							print("You want to create a new group")
							new_group = input("Enter Group Name: ")
							response1 = iam_client.create_group(GroupName = new_group)
							print(response1)

							#adding newly created user to newly created group
							iam_client = boto3.client(args["service"],
								 aws_access_key_id=c.aws_access_key_id,
								 aws_secret_access_key=c.aws_secret_access_key
								 )
							response = iam_client.add_user_to_group(
								GroupName = new_group,
								UserName = new_user
								)
							print(response)

							#attaching admin policy to newly created group
							response1 = iam_client.attach_group_policy(
								GroupName = new_group,
								PolicyArn = "arn:aws:iam::aws:policy/AdministratorAccess"
							)
							print(response1)

							status1 = "COMPLETED"
							return status1
						else:
							print("Group does not exist and you chose not to create a new group.")

			else:
				print("You choose not to create a new user and user provided does not exist.")

		#case 2: user exists but group does not exist
		elif error.response["Error"]["Message"] == "The group with name {} cannot be found.".format(args["group_name"]):
			print("Group name does not exist... Would you like to create a new group?")
			value2 = input("Enter (y or n): ")
			if value2 == "y":
				print("You want to create a new group")
				new_group = input("Enter Group Name: ")
				response1 = iam_client.create_group(GroupName = new_group)
				print(response1)

				iam_client = boto3.client(args["service"],
							  aws_access_key_id=c.aws_access_key_id,
							  aws_secret_access_key=c.aws_secret_access_key
							  )
				response = iam_client.add_user_to_group(
					GroupName = new_group,
					UserName = args["user_name"]
				)
				print(response)

				response1 = iam_client.attach_group_policy(
					GroupName = args["group_name"],
					PolicyArn = "arn:aws:iam::aws:policy/AdministratorAccess"
				)
				print(response1)

				status1 = "COMPLETED"
				return status1

		else:
			print("Unexpected error... exiting from here", error)
			#return "User or Group could not be created", error
		
			status1 = "ERROR"
			return status1
		

#this function checks if an AWS user belongs to any AWS group(s), and returns the group(s) in a list
def aws_list_groups_for_user(**args):
	client = boto3.client(args["service"],
						aws_access_key_id=c.aws_access_key_id,
						aws_secret_access_key=c.aws_secret_access_key
						)
	response = client.list_groups_for_user(
		UserName = args["aws_user"]
	)
	
	list_group = []
	for each in response["Groups"]:
		list_group.append(each["GroupName"])
	print("User '{}' belongs in these groups -".format(args["aws_user"]), list_group)
	return list_group
	

def aws_remove_user_from_group(**args):
	client = boto3.client(args["service"],
						aws_access_key_id=c.aws_access_key_id,
						aws_secret_access_key=c.aws_secret_access_key
						)
	response = client.remove_user_from_group(
		GroupName = args["group_name"],
		UserName = args["aws_user"]
	)
	print("User {} has been removed from group - {}.".format(args["aws_user"], args["group_name"]))


def aws_delete_user(**args):

	try:
		#calling the aws service and loging in to aws profile using access and secret keys
		client = boto3.client(args["service"],
						aws_access_key_id=c.aws_access_key_id,
						aws_secret_access_key=c.aws_secret_access_key
						)		
		
		#deleting login user login profile for user
		response = client.delete_login_profile(
			UserName = args["aws_user"]
			)
		
		#deleting user
		response = client.delete_user(
			UserName = args["aws_user"]
		)
		print(response)
		
	except ClientError as error:
		
		if error.response["Error"]["Message"] == "Cannot delete entity, must remove users from group first.":
			print("ERROR!", error.response["Error"]["Message"])
			
			#listing the group(s) that a user belongs to
			groups_for_user = aws_list_groups_for_user(**args)

			#looping through the group(s) user belongs to, to remove user from each group
			for group in groups_for_user:
				aws_remove_user_from_group(service = args["service"], aws_user = args["aws_user"], group_name = group)
		
			#deleting user 
			response = client.delete_user(
				UserName = args["aws_user"]
				)

			if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
				print("User '{}' has been deleted.".format(args["aws_user"]))
									
			else:
				print("User '{}' was NOT removed from these groups. Hence, user NOT deleted.".format(args["aws_user"]))


#creating aws s3 function that creates bucket(s)
def aws_s3_create_bucket(**args):

    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        create_bucket_response = s3_client.create_bucket(Bucket = args["bucket_name"])
            
        if create_bucket_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("New S3 bucket created -", create_bucket_response["ResponseMetadata"]["HTTPHeaders"]["location"])

    except ClientError as error:
        print(error.response)


#creating aws s3 function that deletes s3 buckets
def aws_s3_delete_bucket(**args):

    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        delete_bucket_response = s3_client.delete_bucket(Bucket = args["bucket_name"])
                    
        if delete_bucket_response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            print("S3 bucket '{}' has been deleted".format(args["bucket_name"]))

    except ClientError as error:
        print(error.response)


#creating an AWS function that uploads files to an S3 bucket
def aws_s3_upload_content(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
        
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        upload_response = s3_client.upload_file(args["upload_file"], args["bucket_name"], args["key"])
        print("'{}' has been uploaded to the s3 bucket - '{}'".format(args["upload_file"], args["bucket_name"]))

    except ClientError as error:
        print(error.response)


#creating the empty s3 bucket function
def aws_s3_empty_bucket(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #using the list_objects_v2 function in boto3 to lists the objects (up to 1,000) in the bucket
        response = s3_client.list_objects_v2(Bucket = args["bucket_name"])
        
        #iterating through the response to pull the objects' 'Keys' in the bucket
        for content in response["Contents"]:
            delete_reponse = s3_client.delete_object(Bucket = args["bucket_name"], Key = content["Key"])
            if delete_reponse["ResponseMetadata"]["HTTPStatusCode"] == 204:
                print("'{}' has been deleted from the bucket - '{}'.".format(content["Key"], args["bucket_name"]))
               
    except ClientError as error:
        print(error.response)


#creating the list_content s3 function
def aws_s3_list_content(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #using the list_objects_v2 function in boto3 to lists the objects (up to 1,000) in the bucket
        response = s3_client.list_objects_v2(Bucket = args["bucket_name"])

        #iterating through the response to pull the objects' 'Keys' in the bucket
        for content in response["Contents"]:
            print(content["Key"])

    except ClientError as error:
        print(error.response)



#Main body
if __name__ == "__main__":
	get_server_dictionary()




