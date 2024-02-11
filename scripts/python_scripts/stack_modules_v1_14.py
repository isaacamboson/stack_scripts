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


timestring = time.localtime()
TS = time.strftime("%d%m%Y%H%M%S", timestring)


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


#creating the email function
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

	backup_dir = os.path.join(bk_args["backup_base"], bk_args["runner"]) #creating a subfolder named with runner in /backup/AWSSEP23/APEXDB/ for future backups

	try:
		#creating the .par file for the database export/backup
		file_add = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(bk_args["schema"], bk_args["runner"], TS), "w")
		file_add.write("userid='/ as sysdba'\n")
		file_add.write("schemas={}\n".format(bk_args["schema"]))
		file_add.write("dumpfile={}_{}_{}.dmp\n".format(bk_args["schema"], bk_args["runner"], TS))
		file_add.write("logfile={}_{}_{}.log\n".format(bk_args["schema"], bk_args["runner"], TS))
		file_add.write("directory={}".format(bk_args["directory1"]))
		file_add.close()

		#printing the content of the .par to the STDOUT for verification of database export config details
		file_view = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(bk_args["schema"], bk_args["runner"], TS), "r")
		file_content = file_view.read()
		print(file_content)
		file_view.close()

		#checking to see if par file was successfully created and printing the absolute path to STDOUT
		file_name = "expdp_{}_{}_{}.par".format(bk_args["schema"], bk_args["runner"], TS)
		file_path = os.path.join(os.getcwd(), file_name)
		print(file_name)
		print(file_path)

		#creating the .sh file the runs the expdp command for the database export
		export = open("/home/oracle/scripts/practicedir_isa_sep23/export.sh", "w+")
		export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=expdp_{}_{}_{}.par".format(bk_args["schema"], bk_args["runner"], TS))
		export_content = "/home/oracle/scripts/practicedir_isa_sep23/export.sh"
		export.close()

		if os.path.isfile(file_path):
			print(".par file exists.")
		backup_path = os.path.join(backup_dir, TS)
		print(backup_path)

		#creating the back directory for future .dmp files 
		os.makedirs(backup_path)

		#making the .sh file executable and running it to run the database backup
		os.popen("chmod 700 {}".format(export_content))
#		os.popen("{}".format(export_content))
		subprocess.run(["/bin/bash", export_content])

		#assigning the variables for the tar function
		tar_path = "/backup/AWSSEP23/APEXDB/{}_{}_{}.tar".format(bk_args["schema"], bk_args["runner"], TS)
		os.chdir("/backup/AWSSEP23/APEXDB/")
		tar_file = "{}_{}_{}.dmp".format(bk_args["schema"], bk_args["runner"], TS)

		#calling the tar function
		tar_func(tar_path, tar_file)

		#assigning the variables for the g_zipp function
		a_path = "/backup/AWSSEP23/APEXDB/{}_{}_{}.tar".format(bk_args["schema"], bk_args["runner"], TS)

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
#				status = "COMPLETED"
#				return status

				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database backup has been completed - ISAAC"
				BODY = "The Database backup process has successfully been completed."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

			else:
				print("Database backup FAILED!")
#				status = "NOT COMPLETED"
#				return status

				TO_EMAIL = "stackcloud11@mkitconsulting.net"
				SUBJECT = "Database backup FAILED - ISAAC"
				BODY = "The Database backup process was NOT completed successfully."
				stack_email2(TO_EMAIL, SUBJECT, BODY)

	except Exception as e:
		print("Export failed! {}".format(e))


#creating a database import function
def database_import(**imp_args):

	import_log_dir = "/backup/AWSSEP23/SAMD"
	
	#copying the .tar.gz from the DB export output location to the import location for the SAMD DB
	src = "/backup/AWSSEP23/APEXDB/{}_{}_{}.tar.gz".format(imp_args["schema"], imp_args["runner"], TS)
	dest = "/backup/AWSSEP23/SAMD"

	#calling the copy function
	copy_fd(src, dest)	

	#untar and unzipping the .tar.gz file to obtain to the .dmp file for the import
	tarz_file = "/backup/AWSSEP23/SAMD/{}_{}_{}.tar.gz".format(imp_args["schema"], imp_args["runner"], TS)
	untar_path = "/backup/AWSSEP23/SAMD"

	#calling the unzip / untar function
	unzip_untar(tarz_file, untar_path)
	
	#creating the .par file for the import
	file_impar = open("/home/oracle/scripts/practicedir_isa_sep23/impdp_{}_stack_{}_{}.par".format(imp_args["schema"], imp_args["runner"], TS), "w")
	file_impar.write("userid='/ as sysdba'\n")
	file_impar.write("schemas={}\n".format(imp_args["schema"]))
	file_impar.write("remap_schema={}:{}_{}_migrated\n".format(imp_args["schema"], imp_args["schema"], imp_args["runner"]))
	file_impar.write("dumpfile={}_{}_{}.dmp\n".format(imp_args["schema"], imp_args["runner"], TS))
	file_impar.write("logfile=impdp_{}_{}_{}.log\n".format(imp_args["schema"], imp_args["runner"], TS))
	file_impar.write("directory={}\n".format(imp_args["directory1"]))
	file_impar.write("table_exists_action=replace")
	file_impar.close()

	file_rd = open("/home/oracle/scripts/practicedir_isa_sep23/impdp_{}_stack_{}_{}.par".format(imp_args["schema"], imp_args["runner"], TS), "r")
	file_content = file_rd.read()
	print(file_content)
	file_rd.close()

	#creating the .sh file that runs the impdp command with .par file for DB import
	import_sh = open("/home/oracle/scripts/practicedir_isa_sep23/import_par.sh", "w+")
	import_sh.write(". /home/oracle/scripts/oracle_env_SAMD.sh\nimpdp parfile=/home/oracle/scripts/practicedir_isa_sep23/impdp_{}_stack_{}_{}.par".format(imp_args["schema"], imp_args["runner"], TS))
	import_content = "/home/oracle/scripts/practicedir_isa_sep23/import_par.sh"
	import_sh.close()

	import_rd = open("/home/oracle/scripts/practicedir_isa_sep23/import_par.sh", "r")
	file_conts = import_rd.read()
	print(file_conts)
	import_rd.close()	

	#making the .sh file executable and running it to run the DB import
	os.popen("chmod 777 {}".format(import_content))
#	os.popen("{}".format(import_content))
	subprocess.run(["/bin/bash", import_content])

	#assigning the created logfile to variable
	import_logfile = "impdp_{}_{}_{}.log".format(imp_args["schema"], imp_args["runner"], TS)
	full_importlog = os.path.join(import_log_dir, import_logfile)

	with open(full_importlog, "r") as r:
		log_check = r.read()
		if "completed" in log_check:
			print("Database import was completed.")
#			status = "COMPLETED"
#			return status
			
			TO_EMAIL = "stackcloud11@mkitconsulting.net"
			SUBJECT = "Database Import has been completed - ISAAC"
			BODY = "The Database Import process has successfully been completed."
			stack_email2(TO_EMAIL, SUBJECT, BODY)
		else:
			print("Database import was NOT completed.")
#			status = "NOT COMPLETED"
#			return status
			
			TO_EMAIL = "stackcloud11@mkitconsulting.net"
			SUBJECT = "Database Import FAILED - ISAAC"
			BODY = "The Database Import process was NOT successfully completed."
			stack_email2(TO_EMAIL, SUBJECT, BODY)

#creating the database migration function
def database_migration(**mg_args):
	#calling the database export function
	database_backup(**mg_args)

	#calling the database import function
	database_import(**mg_args)


#creating a disk utilization check function
def disk_maintenance_check_on_prem(**disk_util):

	while True:
		disk_check = shutil.disk_usage(disk_util["disk"])
		percentage_used = disk_check.used / disk_check.total * 100
		l_thresh = int(disk_util["thresh_sm"])
		h_thresh = int(disk_util["thresh_bg"])
		if percentage_used > l_thresh and percentage_used < h_thresh:
			print("WARNING ALERT! The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
			print("This is above the {}% warning threshold. Please look into this.".format(l_thresh))
			
			TO_EMAIL = "stackcloud11@mkitconsulting.net"
			SUBJECT = "WARNING ALERT - {} is at {:.0f}% - ISAAC".format(disk_util["disk"], percentage_used)
			BODY = "Please triage {} as disk is above the {}% threshold.".format(disk_util["disk"], l_thresh)
			stack_email2(TO_EMAIL, SUBJECT, BODY)			
			time.sleep(5 * 60)

		elif percentage_used > h_thresh:
			print("CRITICAL ALERT! The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
			print("This is above the {}% CRITICAL threshold. Please address immediately.".format(h_thresh))

			TO_EMAIL = "stackcloud11@mkitconsulting.net"
			SUBJECT = "CRITICAL ALERT - {} is at {:.0f}% - ISAAC".format(disk_util["disk"], percentage_used)
			BODY = "Please triage {} IMMEDIATELY as disk is above the {}% threshold.".format(disk_util["disk"], h_thresh)
			stack_email2(TO_EMAIL, SUBJECT, BODY)
			time.sleep(60 * 1)

		elif percentage_used < l_thresh:
			print("The disk utilization for {} is at {:.0f}%.".format(disk_util["disk"], percentage_used))
			print("This is below the {}% threshold.".format(l_thresh))

			TO_EMAIL = "stackcloud11@mkitconsulting.net"
			SUBJECT = "{} is below the {}% threshold - ISAAC".format(disk_util["disk"], l_thresh)
			BODY = "No action needed."
			stack_email2(TO_EMAIL, SUBJECT, BODY)
			break


#Main body
if __name__ == "__main__":
	get_server_dictionary()













