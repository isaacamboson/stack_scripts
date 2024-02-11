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

#def copy_fd(**locations):
#	if os.path.isfile()

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


#def stack_email(TO_EMAIL, SUBJECT, BODY):
#def stack_email(rcp_email, status, function, runner):
def stack_email(**email_args):
	FROM = "oracle@MKIT-DEV-OEM.localadmin"
	TO_EMAIL = email_args["p1"]
	if email_args["p2"] == "COMPLETED":
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
		SUBJECT = "{} {} - {}".format(email_args["p3"], email_args["p2"], email_args["p4"])
		BODY = "{} ran by {} was {}. Thus FAILED!".format(email_args["p3"], email_args["p4"], email_args["p2"])
		MSG="\n".join(("From: {}".format(FROM), "To: {}".format(TO_EMAIL), "Subject: {}:\n".format(SUBJECT), "{}".format(BODY)))
		try:
			with smtplib.SMTP('localhost') as my_server:
				my_server.sendmail(FROM, TO_EMAIL, MSG)
				print("Failure email sent to {}".format(TO_EMAIL))
		except:
			print("Email failed to be sent.")

#creating a database backup function
#def database_backup(runner, schema, backup_base):
def database_backup(**bk_args):
	backup_dir = os.path.join(bk_args["p3"], bk_args["p1"]) #creating a subfolder named with runner in /backup/AWSSEP23/APEXDB/ for future backups

	try:
		#creating the .par file for the database export/backup
		file_add = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(bk_args["p2"], bk_args["p1"], TS), "w")
		file_add.write("userid='/ as sysdba'\n")
		file_add.write("schemas={}\n".format(bk_args["p2"]))
		file_add.write("dumpfile={}_{}_{}.dmp\n".format(bk_args["p2"], bk_args["p1"], TS))
		file_add.write("logfile={}_{}_{}.log\n".format(bk_args["p2"], bk_args["p1"], TS))
		file_add.write("directory=DATA_PUMP_DIR")

		file_add.close()

		#printing the content of the .par to the STDOUT for verification of database export config details
		file_view = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(bk_args["p2"], bk_args["p1"], TS), "r")
		file_content = file_view.read()
		print(file_content)
		file_view.close()

		#checking to see if par file was successfully created and printing the absolute path to STDOUT
		file_name = "expdp_{}_{}_{}.par".format(bk_args["p2"], bk_args["p1"], TS)
		file_path = os.path.join(os.getcwd(), file_name)
		print(file_name)
		print(file_path)

		#creating the .sh file the runs the expdp command for the database export
		export = open("/home/oracle/scripts/practicedir_isa_sep23/export.sh", "w+")
		export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=expdp_{}_{}_{}.par".format(bk_args["p2"], bk_args["p1"], TS))
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
		subprocess.run(["/bin/bash", export_content], check=True)

		#assigning the variables for the tar function
		tar_path = "/backup/AWSSEP23/APEXDB/{}_{}_{}.tar".format(bk_args["p2"], bk_args["p1"], TS)
		os.chdir("/backup/AWSSEP23/APEXDB/")
		tar_file = "{}_{}_{}.dmp".format(bk_args["p2"], bk_args["p1"], TS)

		#calling the tar function
		tar_func(tar_path, tar_file)

		#assigning the variables for the g_zipp function
		a_path = "/backup/AWSSEP23/APEXDB/{}_{}_{}.tar".format(bk_args["p2"], bk_args["p1"], TS)
		
		#calling the g_zipp function
		g_zipp(a_path)


		#assigning the created log file and dumpfiles to variables
		dmp_export = "{}_{}_{}.dmp".format(bk_args["p2"], bk_args["p1"], TS)
		log_export = "{}_{}_{}.log".format(bk_args["p2"], bk_args["p1"], TS)

		fullpath_dmp = os.path.join(bk_args["p3"], dmp_export)
		fullpath_log = os.path.join(bk_args["p3"], log_export)

		with open(fullpath_log, "r") as r:
			log_check = r.read()
			
			if "successfully completed" in log_check:
				print("Database backup was completed successfully.")
				status = "COMPLETED"	
				return status
			else:
				print("Database backup FAILED!")
				status = "NOT COMPLETED"
				return status				

	except Exception as e:
		print("Export failed! {}".format(e))


#creating a database import function
def database_import(**imp_args):

	import_log_dir = "/backup/AWSSEP23/SAMD"

	#creating the .par file for the import
	file_impar = open("/home/oracle/scripts/practicedir_isa_sep23/impdp_{}_stack_{}_{}.par".format(imp_args["p2"], imp_args["p1"], TS), "w")
	file_impar.write("userid='/ as sysdba'\n")
	file_impar.write("schemas={}\n".format(imp_args["p2"]))
	file_impar.write("remap_schema={}:{}_{}_migrated\n".format(imp_args["p2"], imp_args["p2"], imp_args["p1"]))
	file_impar.write("dumpfile={}\n".format(imp_args["p3"]))
	file_impar.write("logfile=impdp_{}_{}_{}.log\n".format(imp_args["p2"], imp_args["p1"], TS))
	file_impar.write("directory={}\n".format(imp_args["p4"]))
	file_impar.write("table_exists_action=replace")
	file_impar.close()

	file_rd = open("/home/oracle/scripts/practicedir_isa_sep23/impdp_{}_stack_{}_{}.par".format(imp_args["p2"], imp_args["p1"], TS), "r")
	file_content = file_rd.read()
	print(file_content)
	file_rd.close()

	#creating the .sh file that runs the impdp command with .par file for DB import
	import_sh = open("/home/oracle/scripts/practicedir_isa_sep23/import_par.sh", "w+")
	import_sh.write(". /home/oracle/scripts/oracle_env_SAMD.sh\nimpdp parfile=impdp_{}_stack_{}_{}.par".format(imp_args["p2"], imp_args["p1"], TS))
	import_content = "/home/oracle/scripts/practicedir_isa_sep23/import_par.sh"
	import_sh.close()

	import_rd = open("/home/oracle/scripts/practicedir_isa_sep23/import_par.sh", "r")
	file_conts = import_rd.read()
	print(file_conts)
	import_rd.close()	

	#making the .sh file executable and running it to run the DB import
	os.popen("chmod 700 {}".format(import_content))
	os.popen("{}".format(import_content))

	#assigning the created logfile to variable
	import_logfile = "impdp_{}_{}_{}.log".format(imp_args["p2"], imp_args["p1"], TS)
	full_importlog = os.path.join(import_log_dir, import_logfile)

	with open(full_importlog, "r") as r:
		log_check = r.read()
		if "completed" in log_check:
			print("Database import was completed.")
			status = "COMPLETED"
			return status

		else:
			print("Database import was NOT completed.")
			status = "NOT COMPLETED"
			return status

#creating a disk utilization check function
def disk_maintenance_check_on_prem(disk, threshold):
	disk_util = shutil.disk_usage(disk)
	percentage_used = disk_util.used / disk_util.total * 100
	thresh = int(threshold)

	if  percentage_used > thresh:
		print("The disk utilization is at {:.0f}%.".format(percentage_used))
		print("This is above the {:.0f}% threshold.".format(thresh))
	else:
		print("The disk utilization is within the threshold limits.")


#Main body
if __name__ == "__main__":
	get_server_dictionary()


