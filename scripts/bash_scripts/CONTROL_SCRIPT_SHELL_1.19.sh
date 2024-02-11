#!/bin/bash


#creating a secure copy function (server to server)
secure_copy_sts()
{
	#on on-prem: pushing to the cloud server
	if ( grep "${dest_server}" /home/oracle/scripts/practicedir_isa_sep23/cloud_servers.txt )
	then
		scp -r -i ${private_key} ${src_path} ${user_acnt}@${dest_server}:${dest_path}  
		if (( $? != 0 ))
		then 
			echo "SCP failed!"
		else
			echo "SCP Successful!"
		fi	

	#on cloud server: pushing to on-prem
	elif ( grep "${dest_server}" /home/oracle/scripts/practicedir_isa_sep23/on_prem_servers.txt )
	then
		scp -r ${src_path} ${user_acnt}@${dest_server}:${dest_path}
		if (( $? != 0 ))
		then
			echo "SCP failed!"
		else
			echo "SCP Successful."
		fi
	else
		echo "Wrong options selected"
	fi
}


# function that checks for exit status
check_exit_status()
{
	if (( $? != 0 ))
	then
		# "action" variable is a unique variable used to uniquely call an exit status function
		echo "${action} - failed exit status run"
		echo "${action} - failed exit status run" | mailx -s "EXIT STATUS FAILED!" stackcloud11@mkitconsulting.net
   else
      echo "${action} - passed exit status run."
   fi
}


#function for backup
backup_f_d()
{
	echo "copying ${source} to ${destination}"	
	mkdir -p  ${destination}
	cp -r ${source} ${destination}
	if (( $? != 0 ))
	then
		echo "${source} failed to copy to ${destination}" | mailx -s "Copy FAILED!" stackcloud11@mkitconsulting.net 
	else
		echo "The copy was successful."
	fi
}


#disk utilization check function
disk_util_check()
{
	echo "checking disk utilization..."

	# checking the disk utilization
	current_use=$(df -h | grep ${disk} | awk '{print $4}' | sed 's/%//g')
   if [[ ${current_use} -gt ${threshold} ]]
	then
		echo "The disk utilization is above the ${threshold}% threshold!"
 		echo "The disk utilization is above the ${threshold}% threshold!" | mailx -s "Disk Utilization Above Threshold." stackcloud11@mkitconsulting.net
   else
		echo "The disk utilization is within the ${threshold}% threshold."
     	echo "The disk utilization is within the ${threshold}% threshold." | mailx -s "Disk Utilization Within Threshold." stackcloud11@mkitconsulting.net
   fi
}

#database schema backup function
database_backup()
{
	#running the oracle database env variable script
	. /home/oracle/scripts/oracle_env_APEXDB.sh
	
	#checking if APEXDB is running. Does not check if it is OPEN
	if  ( ps -ef | grep pmon | grep APEXDB )
	then
		
   	#creating logfile containing schema log in details
   	sqlplus stack_temp/stackinc@APEXDB<<EOF
   	set echo on feedback on
   	spool /home/oracle/scripts/practicedir_isa_sep23/db_status.log
   	show user
   	select * from global_name;
   	select status from v\$instance;
   	spool off
EOF
	
		#checking if the APEXBD is OPEN from the logfile
		if ( grep "OPEN" /home/oracle/scripts/practicedir_isa_sep23/db_status.log )
   	then
			echo "Database is OPEN."

			#creating a loop for looping through schema lists
			schemas="${schema1}"
			for l_schema in ${schemas}
			do
					
				#assigning the .par config file to a variable
				expdp_file=/home/oracle/scripts/practicedir_isa_sep23/${l_schema}_${runner_db}_${TS}.par
	
				#creating and assigning config details to the .par config file
				echo "userid='/ as ${user}'" > ${expdp_file}
				echo "schemas=${l_schema}" >> ${expdp_file}
				echo "dumpfile=${l_schema}_${runner_db}_${TS}.dmp" >> ${expdp_file}
				echo "logfile=${l_schema}_${runner_db}_${TS}.log" >> ${expdp_file}
				echo "directory=${directory1}" >> ${expdp_file}				

	      	#running DB schema backup
   	   	expdp parfile=${expdp_file}
				if (( $? != 0 ))
				then 
					echo "expdp command failed to run."
					echo "expdp command failed to run." | mailx -s "Database Backup FAILED!" stackcloud11@mkitconsulting.net	
				else
					echo "The expdp command ran successfully"
					echo "expdp command ran successfully." | mailx -s "Database Backup successful!" stackcloud11@mkitconsulting.net
				fi	

				#checking if the DB schema was successfully backed up
				if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${l_schema}_${runner_db}_${TS}.log )
				then
					echo "Your database backup completed successfully." | mailx -s "Back Successful" stackcloud11@mkitconsulting.net
					#printing the results of the destination
					ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}
				else
					echo "Your database backup FAILED!" | mailx -s "Backup FAILED!" stackcloud11@mkitconsulting.net
				fi			
				
				#creating a zip file containing all the backed up schema files associated with your runner
				cd /backup/AWSSEP23/APEXDB/
				tar -cvf ${l_schema}_${runner_db}_${TS}.tar *${l_schema}_${runner_db}_${TS}* --remove-files
				if (( $? != 0 ))
				then
					echo "The schema backup files were not zipped."
				else
					echo "The schema backup files were zipped successfully."
				fi

				ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}

				#creating a backup retention policy of two days
				find /backup/AWSSEP23/APEXDB -name "*${runner_db}*" -mtime +2 -exec rm -rf {} \;		
				if (( $? == 0 ))
				then
					echo "The backup retention policy for files created by ${runner_db}, older than two days has been applied."
				else
					echo "The backup retention policy for files created by ${runner_db}, older than two days was not applied."
				fi
	
				ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}

				sleep 5
			done

	   else
   	  	echo "Database instance is NOT OPEN."
			exit
	   fi
	else
		echo "Database is NOT running."
		exit
	fi		
}


database_import()
{
	schemas="${schema1}"
	for l_schema in ${schemas}
	do

		#assigning the .par config file to a variable
		impdp_file=/home/oracle/scripts/practicedir_isa_sep23/impdp_${l_schema}_stack_${runner_db}_${TS}.par

		#creating and assigning config details to the .par config file
		echo "userid='/ as ${user}'" > ${impdp_file}
		echo "schemas=${l_schema}" >> ${impdp_file}
		echo "remap_schema=${l_schema}:${l_schema}_${runner_db}_migrated" >> ${impdp_file}
		echo "dumpfile=${l_schema}_${runner_db}_${TS}.dmp" >> ${impdp_file}
		echo "logfile=impdp_${l_schema}_${runner_db}_${TS}.log" >> ${impdp_file}
		echo "directory=${directory1}" >> ${impdp_file}
		echo "table_exists_action=replace" >> ${impdp_file}

		import_sh=/home/oracle/scripts/practicedir_isa_sep23/import_${l_schema}.sh

		#creating the executable file that runs the impdp file
		echo "export ORACLE_HOME=\"/u01/app/oracle/product/12.1.0/db_1\"" > ${import_sh}
		echo "export ORACLE_SID=HERC" >> ${import_sh}
		echo "/u01/app/oracle/product/12.1.0/db_1/bin/impdp parfile=/home/oracle/scripts/practicedir_isa_sep23/impdp_${l_schema}_stack_${runner_db}_${TS}.par" >> ${import_sh}

		#making the executable file have permissions to run
		chmod 744 ${import_sh}

		#creating the new variable for the secure copy function
		src_path=/backup/AWSSEP23/APEXDB/${l_schema}_${runner_db}_${TS}.tar
		dest_path=/backup/datapump

		#calling the secure copy function for the .tar file
		secure_copy_sts

		#remotely extracting the .dmp and log file from the zipped file on the cloud server
		ssh -i /home/oracle/scripts/practicedir_isa_sep23/MyEC2KeyPair.pem ${user_acnt}@${dest_server} "cd /backup/datapump && tar -xvf /backup/datapump/${l_schema}_${runner_db}_${TS}.tar"

		#assigning new source and dest paths for the .par config file
		src_path=${impdp_file}
		dest_path=/home/oracle/scripts/practicedir_isa_sep23

		#calling the secure copy function for the .par file
		secure_copy_sts

		#assigning new source and dest paths for the .sh file that runs the impdp command
		src_path=${import_sh}
		dest_path=/home/oracle/scripts/practicedir_isa_sep23

		#calling the secure copy function for the .sh config file
		secure_copy_sts

		#remotely running the .sh file containing the impdp commmand, from the on-prem server
		ssh -i /home/oracle/scripts/practicedir_isa_sep23/MyEC2KeyPair.pem ${user_acnt}@${dest_server} "/home/oracle/scripts/practicedir_isa_sep23/import_${l_schema}.sh"

		#removing the files specific to a schema after database import for the schema is complete

		ssh -i /home/oracle/scripts/practicedir_isa_sep23/MyEC2KeyPair.pem ${user_acnt}@${dest_server} "rm -r /backup/datapump/${l_schema}_${runner_db}_${TS}.dmp"
		#checking exit status
		action="dump file removal"
		check_exit_status

		ssh -i /home/oracle/scripts/practicedir_isa_sep23/MyEC2KeyPair.pem ${user_acnt}@${dest_server} "rm -r /backup/datapump/${l_schema}_${runner_db}_${TS}.log"
		#checking exit status
		action="log file removal"
		check_exit_status

		ssh -i /home/oracle/scripts/practicedir_isa_sep23/MyEC2KeyPair.pem ${user_acnt}@${dest_server} "rm -r /backup/datapump/${l_schema}_${runner_db}_${TS}.tar"
		#checking exit status
		action="tar file removal"
		check_exit_status

	done	
}


#database migration function: this calls the database export function and database import function
database_migration()
{
   database_backup

	database_import
}


#main body
# checking for the number of command line arguments

TS=$(date +'%m%d%y%H%M%S')

if [[ $# == 0 ]]
then
	#checking whether to run backup, disk utilization check, DB backup or SCP
	echo "You have entered $# command line argument(s)."
	read -p "Please select 'backup', 'disk_util_check', 'database_migration', 'secure_copy': " ENTERED1

	#case statements for 0 command line args 	
	case ${ENTERED1} in
		#case statement for backup
		backup)
			read -p "please enter source path: " source
			read -p "please enter destination path: " dest
			read -p "please enter a runner: " runner
			TS=$(date +'%m%d%y')
			destination=${dest}/${runner}_${TS}

			#calling the backup fucntion
			backup_f_d
			;;

		#case statement for disk_util_check
		disk_util_check)
			read -p "please enter disk name ('/u01', '/u02', '/u03' or 'backup'): " disk
			read -p "please enter threshold value: " threshold

			# calling the disk utilization function
			disk_util_check ${disk} ${threshold}
			;;

		#case statement for DB schema backup
		database_backup)
			#TS=$(date +'%m%d%y%H%M%S')
			read -p "please provide userid: " user
			read -p "please provide schema name. For multiple schemas, please leave space between schemas: " schema1
			read -p "please provide a runner: " runner_db
			read -p "please provide directory: " directory1
			
			#calling database function
			database_backup
			;;

		#case statement for scp from on-prem server to cloud server and vice versa
		secure_copy)
			read -p "please provide cloud server private key: " private_key
			read -p "please provide the user on the server: " user_acnt
			read -p "please provide source path (file or directory included) : " src_path
			read -p "please provide destination server: " dest_server
			read -p "please provide destination path: " dest_path

			#calling the scp function
			secure_copy_sts
			;;

		#case statement for data migration
		database_migration)
			echo "For the database migration, the database schema export will be performed first."
			echo "please provide details for the database export."
			read -p "please provide database user on the on-prem server: " user
			read -p "please provide schema name. For multiple schemas, please leave space between schemas: " schema1
			read -p "please provide a runner name: " runner_db
			read -p "please provide database directory name for database export: " directory1
			echo " "

			echo "please provide details for the secure copy: "
			read -p "please provide cloud server private key: " private_key
			read -p "please provide the user on the cloud server: " user_acnt
			read -p "please provide destination cloud server: " dest_server
			read -p "please provide destination path for .dmp file: " dest_path_dmp

			#calling the data migration function
			database_migration
			;;

		*)
			echo "please choose 'backup', 'disk_utility_check', 'database_backup', 'database_migration', or 'secure_copy'. "
			;;				

	esac				
	

#checking for conditions for backup functions with command line arguments passed
elif [[ $# == 4 ]] && [[ $1 == "backup" ]]
then
	echo "You have entered $# command line arguments."
	#variable declaration
	source=$2
	TS=$(date +'%m%d%y%')
	dest=$3
	runner=$4
	destination=${dest}/${runner}_${TS}
	
	#calling the backup function
	echo "backing up ${source} to ${destination}"
	backup_f_d ${source} ${destination} ${runner}

#checking for errors in both functions and providing usage
elif [[ $# != 4 ]] && [[ $1 == "backup" ]]
then
	echo "ERROR!"
	echo "USAGE: For a backup, please run script with 4 command line arguments as below: "
	echo "./scriptname source_path destination_path runner."

#checking for conditions for disk utilization functions with command line arguments passed
elif [[ $# == 3 ]] && [[ $1 == "disk_util_check" ]]
then
	echo "You have entered $# command line arguments."
	#calling the disk utilization function
	disk=$2
	threshold=$3	
	disk_util_check ${disk} ${threshold}

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $# != 3 ]] && [[ $1 == "disk_util_check" ]]
then
	echo "ERROR!"
	echo "USAGE: For disk utilization check, please run script with 3 command line arguments as below: "
	echo "./scriptname disk_name threshold."

#checking for conditions for DB schema backup with command line args
elif [[ $1 == "database_backup" ]] && [[ $# == 5 ]]
then
	#declaring variables for use in the .par config file
	#TS=$(date +'%m%d%y%H%M%S')
	user=$2
	schema1=$3
	runner_db=$4
	directory1=$5

	#calling DB schema backup function & exit status
	database_backup

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $1 == "database_backup" ]] && [[ $# != 5 ]]
then
	echo "USAGE: enter 'database_backup', followed by 5 command line arguments in the following order: "
	echo "/scriptname database_backup userid schema runner directory"

#checking for conditions for SCP from server to server, with command line args passed
elif [[ $1 == "secure_copy" ]] && [[ $# == 6 ]]
then
	private_key=$2
	user_acnt=$3
	src_path=$4
	dest_server=$5
	dest_path=$6

	#calling the SCP function
	secure_copy_sts

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $1 == "secure_copy" ]] && [[ $# != 6 ]]
then
	echo "ERROR!"
	echo "USAGE: enter 'secure_copy' followed by 5 command line arguments in following order: "
	echo "./scriptname secure_copy primary_key user absolute_source_path destination_server absolute_destination_path."

#checking for the conditions for the database_migration
elif [[ $1 == "database_migration" ]] && [[ $# == 9 ]]
then
	user=$2
	schema1=$3
	runner_db=$4
	directory1=$5
	private_key=$6
	user_acnt=$7
	dest_server=$8
	dest_path=$9
	
	#calling the database migration function
	database_migration

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $1 == "database_migration" ]] && [[ $# != 9 ]]
then
	echo "ERROR!"
	echo "USAGE: enter 'data_migration' followed by 8 command line arguments in following order: "
	echo "./scriptname data_migration dba_user(e.g. sysdba) schema(s) runner directory(e.g DATA_PUMP_DIR) primary_key cloud_user(e.g. oracle) dest_server(e.g **amazonaws) dest_path_dmp(e.g. destination for dmp file on cloud server)."

else
	echo "please choose 'backup', 'disk_utility_check', 'database_backup', 'database_migration', or 'secure_copy' only. "
	exit
fi




