#!/usr/bin/python


#imported modules
import os
import shutil
import sys
import time
import subprocess
import tarfile
import gzip
import smtplib

#variable declaration
timestring=time.localtime()
TS=time.strftime("%d%m%Y%H%M%S",timestring)


#function declaration
def STACK_EMAIL(a,b,c,d):
		try:
			FROM='oracle@MKIT-DEV-OEM.localdomain'
         #variables
			TO_EMAIL=a
			SUBJECT="%s %s: %s"%(c,TS,b)
			
			if b == "success":
				BODY="%s for %s was a %s!"%(c,d,b) 
			else:
				BODY="%s for %s was a %s!"%(c,d,b)


			MSG=("\n".join(("From: %s" %FROM, "To: %s" %TO_EMAIL, "Subject: %s:\n" %SUBJECT,"%s" %BODY)))

			with smtplib.SMTP('localhost') as my_server:
				my_server.sendmail(FROM,TO_EMAIL,MSG)
			print("Email sent successfully to %s" %TO_EMAIL)
		except Exception as d:
			print("Email was not sent. Error: %s" %str(b))

def database_backup(a,b,c,d,e):
	backup_base=e
	runner=b
	
	#absolute path .dblogin.sh
	dbstatus_path="%sdblogin.sh"%(d)
		
	#process commands and variables
	ps_command="ps -ef | grep pmon | grep APEXDB"
	output=subprocess.getoutput(ps_command)
	
	#schema export variables
	export_dmp="%s_%s_%s.dmp"%(a,b,TS)
	export_log="%s_%s_%s.log"%(a,b,TS)
	exportdmp_path=os.path.join(backup_base,export_dmp)
	exportlog_path=os.path.join(backup_base,export_log)

	#path to db_status.log file	
	file_path="%sdb_status.log"%(d)

	#checking is the database process is running and started up
	if output:
		print("Database is running!")	
		os.popen(dbstatus_path)
		
		#opening db_status.log file in read mode
		with open(file_path,'r') as dblog:
			file_contents=dblog.read()
			
		#checking if "OPEN" string is present in the file contents
		if "OPEN" in file_contents:
			print("Database is Open!")
		else:
			print("Database is not Open!")
		try:
			#creating .par file 
			par=open("%sexport_%s_%s_%s.par"%(d,a,b,TS), "w+")
			par.write("userid='/ as sysdba'\n")
			par.write("schemas=%s\n"%(a))
			par.write("dumpfile=%s_%s_%s.dmp\n"%(a,b,TS))
			par.write("logfile=%s_%s_%s.log\n"%(a,b,TS))
			par.write("directory=%s"%(c))
			par.close()
			par_read=open("%sexport_%s_%s_%s.par"%(d,a,b,TS),"r+")
			par_content=par_read.read()
			print(par_content)
			par_read.close()
			par_name="export_%s_%s_%s.par"%(a,b,TS)
			print(par_name)
		except:
			print("par file creation unscuccessful")

		try:
			#getting absolute path ofr .par file
			par_path=os.path.join(os.getcwd(),"%s"%(par_name))			
	
			#creating .sh file to set environment variables and start db schema backup
			export=open("%sexport_%s.sh"%(d,TS),"w+")
			export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=%sexport_%s_%s_%s.par"%(d,a,b,TS))
			
			export.close()
			export_content="%sexport_%s.sh"%(d,TS)	
			os.popen("chmod 700 %s"%(export_content))
		except:
			print("%s file creation failed"%(export_content))

		try:
			#start DB schema backup using expdp command
			print("Starting Schema export for %s"%(a))
			subprocess.call(['sh',"%s"%(export_content)])		
		except:
				print("expdp backup failed")

		#opening log file in read mode
		with open(exportlog_path,'r') as exportlog:
			exportlog_contents=exportlog.read()
		
		#checking for "successfully completed" string in export_log
		if "successfully completed" in  exportlog_contents:
			print("expdp backup successful")
			status="success"
		else:
			print("expdp backup failed")	
			status="failure"
	
		try:	
			G_zipp(exportdmp_path)
		
		except:
			print("Zipping of %s was unsuccessful!"%(export_dmp)) 	
		return status	
	else:
		print("Database is not running")

def backup_f_d(a,b,c):
	dest_dir="%s/%s/%s/"%(b,c,TS)
	dest_path=os.path.join(os.getcwd(),dest_dir)
	#creating directory path if it doesnt exist yet
	
	os.makedirs(dest_path, exist_ok=True)	
	if os.path.isdir(a):
		try:
			#priting to  stdout
			print("Copying source directory %s to %s"%(a,dest_path))
      	#using shutil copytree to copy a directory and its contents to destination dir
			shutil.copytree(a,dest_path)
			status="success"
		except:
			print("Copying of source directory %s to %s failed"%(a,dest_path))
			status="failure"
	elif os.path.isfile(a):
		try:
    		#printing to stdout
			print("Copying source file %s to %s"%(a,dest_path))

      	#using shutil copy function to copy src to dst
			shutil.copy(a,dest_path)

      	#printing to stdout
			print("Copy complete!")
			status="success"
		except:
			print("Copying of source file %s to %s has failed")
			status="failure"
	return status

def disk_utilization_check(a,b):
   #output of subprocess.getoutput is stored in disk_util variable and type casted to an Integer
	disk_util=int(subprocess.getoutput(("df -h|grep '%s'|awk '{print $4}'|sed 's/%%//g'"%(a))))
	try:
		if disk_util > b:
			print("disk utilization for %s is above %s!"%(a,b))
		else:
			print("disk utilization for %s is below %s!"%(a,b))
			status="success"
	except:
		print("Disk utililization check failed")
		status="failure"
	return status

def G_zipp(a):
	file_name=os.path.basename(a)
	
	#checking if the source is a file 
	if os.path.isfile(a):
		try:
			#constructing output file name
			tar_file="%s_%s.tgz"%(a,TS)
			#opening tar archive in write mode with gzip conmpression
			with tarfile.open(tar_file,'w:gz') as tar:
				#adding the source file to tar archive with the same base name
				tar.add(a,arcname=os.path.basename(a))
				
				print("%s has been succcessfully Gzipped!"%(file_name))
				status="success"
		except:
			print("%s has failed to zip"%(file_name))
			status="failure"
	elif os.path.isdir(a):
		try:
			#constructing output file name
			tar_dir="%s_%s.tgz"%(a,TS)
			# opens a tar archive with gzip compression in write mode
			with tarfile.open(tar_dir, "w:gz") as tar:
				#adding source file to tar archive under source file name
				tar.add(a,arcname=os.path.basename(a))

				print("%s has been successfully Gzipped!"%(file_name))						
				status="success"
		except:
			print("%s has failed to zip"%(file_name))
			status="failure"
	#returning status to caller
	return status

def unzipp(a,b):
	try:
		#opens specified tar archive
		file=tarfile.open(a)
		print(file.getnames())
		
		#extracts the content of the tar archive to the destination path
		file.extractall(b)
		
		#close tar archive
		file.close()	
		print("%a has successfully been unzipped!"%(a))
	except:
		print("%s has failed to unzip!"%(a))
	
def database_import(a,b,c,d,e,f,g,h):
	dblog_path="%sdb_status.log"%(d)
	import_log="%s_%s_%s.log"%(a,g,TS)
	importlog_path=os.path.join(e,import_log)
	dmpfile_path=os.path.splitext(h)[0]	
	dmp_file=os.path.basename(dmpfile_path)
	
	#removes time stamp from .dmp file
	index_dmp=dmp_file.find('.dmp')
	dumpfile=dmp_file[:index_dmp + 4] if index_dmp != -1 else dmp_file	
	
	unzipp(h,e)
	
	try:
		#creating .par file for import
		par=open("impdp_%s_%s_%s.par"%(a,g,TS),'w+')				
		par.write("userid='/ as sysdba'\n")
		par.write("schemas=%s\n"%(a))
		par.write("remap_schema=%s:%s_%s_imported\n"%(a,a,g))
		par.write("dumpfile=%s\n"%(dumpfile))
		par.write("logfile=%s_%s_%s.log\n"%(a,g,TS))
		par.write("directory=%s\n"%(c))
		par.write("table_exists_action=replace")
		par.close()
	
		par_read=open("%simpdp_%s_%s_%s.par"%(d,a,g,TS),'r+')
		par_content=par_read.read()
		print(par_content)
	
		par_name="impdp_%s_%s_%s.par"%(a,g,TS)
		print(par_name)
	except:
		print("Par file creation unscuccessful")
	
	try:
		#creating.sh file for import
		import_exec=open("%simport_exec.sh"%(d), "w+")
		import_exec.write(". /home/oracle/scripts/oracle_env_%s.sh\nimpdp parfile=impdp_%s_%s_%s.par"%(f,a,g,TS))
		import_exec.close()
		import_content=("%simport_exec.sh"%(d))
		os.popen("chmod 700 %s"%(import_content))
	except:
		print(".sh file creation failed")
	
		#Checking DB status
		subprocess.call(['sh', '%sdblogin.sh'%(d)])
		#opening db_status.log file in read mode
		with open(file_path,'r') as dblog:
			file_contents=dblog.read()

		#checking if "OPEN" string is present in the file contents
		if "OPEN" in file_contents:
			print("Database is Open!")
		else:
			print("Database is not Open!")
		
	#Starting import
	subprocess.call(['sh', '%simport_exec.sh'%(d)])

		#opening log file in read mode
	with open(importlog_path,'r') as importlog:
		importlog_contents=importlog.read()

	#checking for "successfully completed" string in export_log
	if "completed" in  importlog_contents:
		print("impdp import successful")
		status="success"
	else:
		print("import failed")
		status="failure"
	return status

#main body
if __name__=="__main__":
	
	if function == "database_backup":
		schema=sys.argv[2]
		runner=sys.argv[3]
		directory=sys.argv[4]
		par_dir=sys.argv[5]
		sourcedb_physical=sys.argv[6]

		#calling function with required arguements
		database_backup(schema,runner,directory,par_dir,sourcedb_physical)
	elif function == "file_directory_cp":
		src=sys.argv[2]
		dst=sys.argv[3]
	
		file_directory_cp(src,dst)















