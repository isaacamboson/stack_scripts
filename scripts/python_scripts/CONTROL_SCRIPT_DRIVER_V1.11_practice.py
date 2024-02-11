#!/usr/bin/python



#imported modules
import sys
import stack_modules_v11 as k



#variable declaration

comlin_args=len(sys.argv) -1

#main body

#condition for if no command line arguments are entered at run time
if comlin_args == 0:
	print()
	function=input("what task are you trying to do? database_backup, backup_f_d, disk_utilization_check, G_zipp, unzipp, or database_import?: ")	
	if function == "database_backup":
	 
		#prompting user for required arguments to call database backup function
		schema=input("Enter Schemas: ")
		runner=input("Enter Runner: ")
		directory=input("Enter Directory: ")
		par_dir=input("Enter path for .par file creation: ")
		sourcedb_physical=input("Enter source DB physical path: ")
		
		email_send=input("would you like to send an email upon completion? Yes or No: ")
		if email_send == "Yes":
			email_add=input("enter email: ")
		
			#calling database backup fucntion with required arguments
			status=k.database_backup(schema,runner,directory,par_dir,sourcedb_physical)
			
			#calling STACK EMAIL function with required arguments
			k.STACK_EMAIL(email_add,status,function,runner)
		elif email_send == "No":
			k.database_backup(schema,runner,directory,par_dir,sourcedb_physical)
		else:
			print("Incorrect Option Entered!")
			print("Please Enter Yes or No!")	
	elif function == "backup_f_d":
		#prompting user for required arguments to call backup_f_d function
		src=input("Enter source path: ")
		dst=input("Enter destination path: ")
		runner=input("Enter runner: ")
	
		#prompting user for email to be sent	
		email_send=input("would you like to send an email upon completion? Yes or No: ")
		if email_send == "Yes":
			email_add=input("enter email: ")
	
			#calling file directory copy function with required arguments
			status=k.backup_f_d(src,dst,runner)	
			k.STACK_EMAIL(email_add,status,function,runner)
		elif email_send == "No":
			k.backup_f_d(src,dst,runner)
		else:
			print("Incorrect Option Entered!")
			print("Please Enter Yes or No!")

	elif function == "disk_utilization_check":
		disk=input("Enter disk: ")
		threshold=int(input("Enter Threshold: "))
		
		email_send=input("would you like to send an email upon completion? Yes or No: ")
		if email_send == "Yes":
			email_add=input("enter email: ")
			runner=input("Enter runner: ")
			
			#assigning disk util check function call the status variable
			status=k.disk_utilization_check(disk,threshold)
			k.STACK_EMAIL(email_add,status,function,runner)
		
		elif email_send == "No":
			k.disk_utilization_check(disk,threshold)
		else:
			print("Incorrect Option Entered!")
			print("Please Enter Yes or No!")	

	elif function == "G_zipp":
		file_dir=input("Enter absolute path of file or directory that you would like to G_zipp: ")
		
		email_send=input("would you like to send an email upon completion? Yes or No: ")
		if email_send == "Yes":
			email_add=input("enter email: ")
			runner=input("Enter runner: ")
				
			#calling G_zipp function with required arguments
			status=k.G_zipp(file_dir)
			
			k.STACK_EMAIL(email_add,status,function,runner)
		elif email_send == "No":
			k.G_zipp(file_dir)
		else:
			print("Incorrect Option Entered!")
			print("Please Enter Yes or No!")
	elif function == "unzipp":
		file_dir=input("Enter absolute path of file or directory that you would like to unzipp: ")
		destination=input("Enter Destination path: ")	
		#calling unzipp function with required arguments
		k.unzipp(file_dir,destination)
	
	elif function == "database_import":
		#prompting for variable required for a database import
		schema=input("Enter Schemas: ")
		runner=input("Enter Runner: ")
		directory=input("Enter Directory: ")
		par_dir=input("Enter path for .par file creation: ")	
		sourcedb_physical=input("Enter source DB physical path: ")
		dbname=input("Enter Database name to Import Schema into: ")
		import_schema=input("Enter schema to import to Database: ")
		dmp_file=input("Enter path absolute path to Zipped dump file: ")
		
		#prompting for 
		email_send=input("would you like to send an email upon completion? Yes or No: ")
		if email_send == "Yes":
			email_add=input("enter email: ")
			
			#calling database backup import with required arguments
			status=k.database_import(schema,runner,directory,par_dir,sourcedb_physical,dbname,import_schema,dmp_file)
				
			#calling email function with required arguments
			k.STACK_EMAIL(email_add,status,function,runner)
		elif email_send == "No":
			#calling database import function with required arguments
			k.database_import(schema,runner,directory,par_dir,sourcedb_physical,dbname,import_schema,dmp_file)
		else:
			print("Incorrect Option Entered!")
			print("Please Enter Yes or No!")
	else:
		print("Function not defined")
		print()
		print("USAGE: the following is how to properly use the database_backup, and backup_f_d function!")
		print()
		print("       database_backup")
		print("       eg .modulename database_backup schema runner directory par_dir sourcedb_physical")
		print()
		print("       backup_f_d")
		print("       eg .modulename backup_f_d src dst runner")
		print()	
		print("       disk_utilization_check")
		print("       eg .modulename disk_utilization_check disk threshold")
		print()
		print("       G_zipp")
		print("       eg .modulename G_zipp file_dir")
		print()
		print("       unzipp")
		print("       eg .modulename unzipp file_dir")
		print()
		print("       database_import")
		print("       eg .modulename database_backup schema runner directory par_dir sourcedb_physical dbname import_schema dmp_file")
		

elif sys.argv[1] == "database_backup":
	if comlin_args == 6:
		schema=sys.argv[2]
		runner=sys.argv[3]
		directory=sys.argv[4]
		par_dir=sys.argv[5]
		sourcedb_physical=sys.argv[6]
		
		#calling database backup fucntion with required arguments
		k.database_backup(schema,runner,directory,par_dir,sourcedb_physical)
	elif comlin_args == 7:
		schema=sys.argv[2]
		runner=sys.argv[3]
		directory=sys.argv[4]
		par_dir=sys.argv[5]
		sourcedb_physical=sys.argv[6]
		email_add=sys.argv[7]

		#calling database backup fucntion with required arguments
		status=k.database_backup(schema,runner,directory,par_dir,sourcedb_physical)
		k.STACK_EMAIL(email_add,status,function,runner)
	
	elif comlin_args != 6 and comlin_args != 7:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the database_backup function!")
		print()
		print("       database_backup")
		print("       eg .modulename database_backup schema runner directory par_dir sourcedb_physical")	
		print()
		print("       database_backup:EMAIL")
		print("       eg .modulename database_backup schema runner directory par_dir sourcedb_physical email_add")
		print()
elif sys.argv[1] == "backup_f_d":
	if comlin_args == 4:
		src=sys.argv[2]
		dst=sys.argv[3]
		runner=sys.argv[4]				
		#calling file directory copy function with required arguments
		k.file_directory(src,dst,runner)
	elif comlin_args == 5:
		src=sys.argv[2]
		dst=sys.argv[3]
		runner=sys.argv[4]
		email_add=sys.argv[5]
		
		#calling file directory copy function with required arguments
		status=k.file_directory(src,dst,runner)
		k.STACK_EMAIL(email_add,status,function,runner)
	
	elif comlin_args != 4 and comlin_args != 5:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the backup_f_d function!")
		print()
		print("       backup_f_d")
		print("       eg .modulename backup_f_d src dst runner")	
		print()
		print("       backup_f_d:EMAIL")
		print("       eg .modulename backup_f_d src dst runner email_add")
		print()
elif sys.argv[1] == "disk_utilization_check":
	if comlin_args == 3:
		disk=sys.argv[2]
		threshold=int(sys.argv[3])
		
		#calling unzip function with required argument
		k.disk_utilization_check(disk,threshold)
	elif comlin_args == 5:
		disk=sys.argv[2]
		threshold=int(sys.argv[3])
		email_add=sys.argv[4]
		runner=sys.argv[5]

		#calling unzip function with required argument
		status=k.disk_utilization_check(disk,threshold)
		k.STACK_EMAIL(email_add,status,function,runner)

	elif comlin_args != 3 and comlin_args != 5:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the disk_utilization_check function!")
		print()
		print("       disk_utilization_check")
		print("       eg .modulename disk_utilization_check disk  threshold")
		print()
		print("       disk_utilization_check:EMAIL")
		print("       eg .modulename disk_utilization_check disk  threshold email_add runner")
		print()	
elif sys.argv[1] == "G_zipp":
	if comlin_args == 2:
		file_dir=sys.argv[2]

		#calling unzip function with required argument
		k.G_zipp(file_dir)
	elif comlin_args == 4:
		file_dir=sys.argv[2]
		email_add=sys.argv[3]
		runner=sys.argv[4]
		
		#calling unzip function with required argument
		status=k.G_zipp(file_dir)
		k.STACK_EMAIL(email_add,status,function,runner)

	elif comlin_args != 2 and comlin_args != 4:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the disk_utilization_check function!")
		print()
		print("       G_zipp")
		print("       eg .modulename G_zipp file_dir")
		print()
		print("       G_zipp:EMAIL")
		print("       eg .modulename G_zipp file_dir email_add runner")
		print()
elif sys.argv[1] == "unzipp":
	if comlin_args == 2:
		file_dir=sys.argv[2]

		#calling unzip function with required argument
		k.unzipp(file_dir)
	elif comlin_args != 2:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the disk_utilization_check function!")
		print()
		print("       unzipp")
		print("       eg .modulename unzipp file_dir")
		print()
elif sys.argv[1] == "database_import":
	if comlin_args == 7:
		schema=sys.argv[2]
		runner=sys.argv[3]
		directory=sys.argv[4]
		par_dir=sys.argv[5]
		sourcedb_physical=sys.argv[6]
		dbname=sys.argv[7]
		import_schema=sys.argv[8]
		dmp_file=sys.argv[9]
			
		#calling database import function with required argument
		k.database_import(schema,runner,directory,par_dir,sourcedb_physical,dbname,import_schema,dmp_file)
	elif comlin_args == 10:
		schema=sys.argv[2]
		runner=sys.argv[3]
		directory=sys.argv[4]
		par_dir=sys.argv[5]
		sourcedb_physical=sys.argv[6]
		dbname=sys.argv[7]
		import_schema=sys.argv[8]
		dmp_file=sys.argv[9]
		email_add=sys.argv[10]
		
		status=k.database_import(schema,runner,directory,par_dir,sourcedb_physical,dbname,import_schema,dmp_file)
		k.STACK_EMAIL(email_add,status,function,runner)

	elif comlin_args != 7 and comlin_args != 10:
		print()
		print("Incorrect arguments")
		print("USAGE: the following is how to properly use the database_import function!")
		print()
		print("       database_import")
		print("       eg .modulename database_import schema runner directory par_dir sourcedb_physical dbname import_schema dmp_file")
		print()
		print("       database_import:EMAIL")
		print("       eg .modulename database_import schema runner directory par_dir sourcedb_physical dbname import_schema dmp_file email_add")
		print()

else:
	print()
	print("Function not defined or incorrect arguments")
	print()
	print("USAGE: the following is how to properly use this module!")
	print()
	print("       database_backup")
	print("       eg .modulename database_backup schema runner directory par_dir sourcedb_physical")
	print()
	print("       backup_f_d")
	print("       eg .modulename backup_f_d src dst runner")
	print()
	print("       disk_utilization_check")
	print("       eg .modulename disk_utilization_check disk  threshold")
	print()
	print("       G_zipp")
	print("       eg .modulename G_zipp file_dir")
	print()
	print("       unzipp")
	print("       eg .modulename unzipp file_dir")
	print()
	print("       database_import")
	print("       eg .modulename database_import schema runner directory par_dir sourcedb_physical dbname import_schema dmp_file")
	print()





