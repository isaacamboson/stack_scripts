#!/usr/bin/python

import os 
import sys
import time
import psutil
import shutil


def get_server_dictionary():

#	servers={
#    "hosts":[{"MKIT-DEV-OEM":"ON_PREM"},{"STACKCLOUD":"CLOUD"}],
#    "disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
#    "transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
#    }

	servers={
    "Hosts":{"MKIT-DEV-OEM":"ON-PREM","STACKCLOUD":"CLOUD"},
    "Disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
    "Transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }

	return servers


#calling the function that copies file or directory from source to destination
def copy_fd(src, dest):
	if os.path.isfile(src):
		shutil.copy(src, dest)
	elif os.path.isdir(src):
		source_base = os.path.basename(src)
		dest_d = os.path.join(dest, source_base)
		shutil.copytree(src, dest_d)


def database_backup(runner, schema, backup_base):
	timestring = time.localtime()
	TS = time.strftime("%d%m%Y%H%M%S", timestring)
	print(TS)
	backup_dir = os.path.join(backup_base, runner)

	try:
		file_add = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(schema, runner.lower(), TS), "w")
		file_add.write("userid='/ as sysdba'\nschemas={}\ndumpfile={}_{}_{}.dmp\nlogfile={}_{}_{}.log\ndirectory=DATA_PUMP_DIR".format(schema, schema, runner.lower(), TS, schema, runner.lower(), TS))
		file_add.close()

		file_view = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_{}_{}_{}.par".format(schema, runner.lower(), TS), "r")
		file_content = file_view.read()

		print(file_content)
		file_view.close()

		file_name = "expdp_{}_{}_{}.par".format(schema, runner.lower(), TS)
		file_path = os.path.join(os.getcwd(), file_name)
		print(file_name)
		print(file_path)

		export = open("/home/oracle/scripts/practicedir_isa_sep23/export.sh", "w+")
		export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=expdp_{}_{}_{}.par".format(schema, runner.lower(), TS))
		export_content = "/home/oracle/scripts/practicedir_isa_sep23/export.sh"
		export.close()
	
		if os.path.isfile(file_path):
			print(".par file exists.")
		backup_path = os.path.join(backup_dir, TS)
		print(backup_path)

		os.makedirs(backup_path)
#  	OR
#  	os.popen("mkdir -p {}".format(backup_path))
		os.popen("chmod 700 {}".format(export_content))
		os.popen("{}".format(export_content))
	
		if os.path.isdir(backup_path):
			print("Timestamped backup path exists.")
	except:
		print("Export failed!")


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


