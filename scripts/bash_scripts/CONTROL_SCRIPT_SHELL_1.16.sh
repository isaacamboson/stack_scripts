#!/bin/bash


#creating a secure copy function (server to server)
secure_copy_sts()
{
	#on on-prem: pushing to the cloud server
	if ( grep "${dest_server}" /home/oracle/scripts/practicedir_isa_sep23/cloud_servers.txt )
	then
		scp -r -i ${private_key} ${src_path} oracle@${dest_server}:${dest_path}  
		if (( $? != 0 ))
		then 
			echo "SCP failed!"
		else
			echo "SCP Successful!"
		fi	

	#on cloud server: pushing to on-prem
	elif ( grep "${dest_server}" /home/oracle/scripts/practicedir_isa_sep23/on_prem_servers.txt )
	then
		scp -r ${src_path} oracle@${dest_server}:${dest_path}
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
		echo "failed exit status run" | mailx -s "EXIT STATUS FAILED!" stackcloud11@mkitconsulting.net
   else
      echo "command was successfully run."
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
			if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${schema1}_${runner_db}_${TS}.log )
			then
				echo "Your database backup completed successfully." | mailx -s "Back Successful" stackcloud11@mkitconsulting.net
				#printing the results of the destination
				ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}
			else
				echo "Your database backup FAILED!" | mailx -s "Backup FAILED!" stackcloud11@mkitconsulting.net
			fi			

			#creating a zip file containing all the backed up schema files associated with your runner and deleting files
			tar -cvf /backup/AWSSEP23/APEXDB/${schema1}_${runner_db}_${TS}.tar /backup/AWSSEP23/APEXDB/*${runner_db}_${TS}* --remove-files
			if (( $? != 0 ))
			then
				echo "The schema backup files were not zipped."
			else
				echo "The schema backup files were zipped successfully."
			fi
			
			ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}

	   else
   	   echo "Database instance is NOT running."
			exit
	   fi
	else
		echo "Database is NOT running."
	fi		
}


#main body

# checking for the number of command line arguments
if [[ $# == 0 ]]
then
	#checking whether to run backup, disk utilization check, DB backup or SCP
	echo "You have entered $# command line argument(s)."
	read -p "Please select 'backup', 'disk_util_check', 'database_backup', or  'secure_copy' " ENTERED1

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
			TS=$(date +'%m%d%y%H%M%S')
			read -p "please provide userid: " user
			read -p "please provide schema: " schema1
			read -p "please provide a runner: " runner_db
			read -p "please provide directory: " directory1
		
			#assigning the .par config file to a variable
			expdp_file=/home/oracle/scripts/practicedir_isa_sep23/${schema1}_${runner_db}_${TS}.par

			#creating and assigning config details to the .par config file
			echo "userid='/ as ${user}'" > ${expdp_file}
			echo "schemas=${schema1}" >> ${expdp_file}	
			echo "dumpfile=${schema1}_${runner_db}_${TS}.dmp" >> ${expdp_file}
			echo "logfile=${schema1}_${runner_db}_${TS}.log" >> ${expdp_file}
			echo "directory=${directory1}" >> ${expdp_file}

			#calling database function
			database_backup
			;;
		
		#case statement for scp from on-prem server to cloud server and vice versa
		secure_copy)
			read -p "please provide cloud server private key: " private_key
			read -p "please provide source path (file or directory included) : " src_path
			read -p "please provide destination server: " dest_server
			read -p "please provide destination path: " dest_path

			#calling the scp function
			secure_copy_sts
			;;

		*)
			echo "please choose 'backup', 'disk_utility_check', 'database_backup', 'secure_copy' or 'multiple_database_backup' only."
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
	TS=$(date +'%m%d%y%H%M%S')
	userid=$2
	schema1=$3
	runner_db=$4
	directory1=$5

	#assigning the .par config file to a variable
	expdp_file=/home/oracle/scripts/practicedir_isa_sep23/expdp_${schema1}_${runner_db}_${TS}.par

	#creating and exporting config details to the .par config file
	echo "userid='/ as ${userid}'" > ${expdp_file}
	echo "schemas=${schema1}" >> ${expdp_file}
	echo "dumpfile=${schema1}_${runner_db}_${TS}.dmp" >> ${expdp_file}
	echo "logfile=${schema1}_${runner_db}_${TS}.log" >> ${expdp_file}
	echo "directory=${directory1}" >> ${expdp_file}
	
	#calling DB schema backup function & exit status
	database_backup

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $1 == "database_backup" ]] && [[ $# != 5 ]]
then
	echo "USAGE: enter 'database_backup', followed by 5 command line arguments in the following order: "
	echo "/scriptname database_backup userid schema runner directory"
	
#checking for conditions for SCP from server to server, with command line args passed
elif [[ $1 == "secure_copy" ]] && [[ $# == 5 ]]
then
	private_key=$2
	src_path=$3
	dest_server=$4
	dest_path=$5

	#calling the SCP function
	secure_copy_sts

#checking if the first command line arg is correct but the wrong number of command line args is passed
elif [[ $1 == "secure_copy" ]] && [[ $# != 5 ]]
then
	echo "ERROR!"
	echo "USAGE: enter 'secure_copy' followed by 5 command line arguments in following order: "
	echo "./scriptname secure_copy primary_key absolute_source_path destination_server absolute_destination_path."

else
	echo "please choose 'backup', 'disk_utility_check', 'database_backup', or 'secure_copy' only. "
		
fi



