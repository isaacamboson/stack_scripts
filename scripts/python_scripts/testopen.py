#!/usr/bin/python

import os
import time

timestring = time.localtime()
TS = time.strftime("%d%m%Y%H%M%S", timestring)
print(TS)
backup_base = "/backup/AWSSEP23/APEXDB"
runner = "ISAAC"
backup_dir = os.path.join(backup_base, runner)


try:
	file_add = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_stacktemp_isaac_{}.par".format(TS), "w")
	file_add.write("userid='/ as sysdba'\nschemas=stack_temp\ndumpfile=stack_temp_dump_isaac_{}.dmp\nlogfile=stacktemp_dump_isaac_{}.log\ndirectory=DATA_PUMP_DIR".format(TS,TS))
	file_add.close()

	file_view = open("/home/oracle/scripts/practicedir_isa_sep23/expdp_stacktemp_isaac_{}.par".format(TS), "r")
	file_content = file_view.read()

	print(file_content)
	file_view.close()

	file_name = "expdp_stacktemp_isaac_{}.par".format(TS)
#	file_dir = os.path.cwd()
	file_path = os.path.join(os.getcwd(), file_name)
	print(file_name)
	print(file_path)

	export = open("/home/oracle/scripts/practicedir_isa_sep23/export.sh", "w+")
	export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=expdp_stacktemp_isaac_{}.par".format(TS))	
	export_content = "/home/oracle/scripts/practicedir_isa_sep23/export.sh"
	export.close()
	
	if os.path.isfile(file_path):
		print(".par file exists.")		
	backup_path = os.path.join(backup_dir, TS)
	print(backup_path)

	os.makedirs(backup_path)
#	OR
#	os.popen("mkdir -p {}".format(backup_path))
	os.popen("chmod 700 {}".format(export_content))
	os.popen("{}".format(export_content))

	if os.path.isdir(backup_path):
		print("Timestamped backup path exists.")

except:
	print("Export failed!")


