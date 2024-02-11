#!/bin/bash


# function that checks for exit status
check_exit_status()
{
	if (( $? != 0 ))
	then
		echo "failed exit status run"
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
		echo "${source} FAILED to copied to ${destination}"
	fi
}


#disk utilization check function
disk_util_check()
{
	echo "checking disk utilization..."

	# checking the disk utilization
	current_use=$(df -h | grep ${disk} | awk '{print $4}' | sed 's/%//g')
	if (( $? != 0 ))
	then
		echo "variable declaration for the current disk use FAILED!"
	else
		if [[ ${current_use} -gt ${threshold} ]]
   	then
 			echo "The disk utilization is above the ${threshold}% threshold!"
      	echo "Please address this issue."
   	else
      	echo "The disk utilization is within the ${threshold}% threshold."
      	echo "No action needed.:"
   	fi
	fi
}


#database schema backup function
database_backup()
{
	#running the oracle database env variable script
	. /home/oracle/scripts/oracle_env_APEXDB.sh
	
	#checking if APEXDB is running. Does not check if it is OPEN
	ps -ef | grep pmon | grep APEXDB

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
			echo "expdp command FAILED to run!"
		fi		
   else
      echo "Database is NOT open."
      exit
   fi
}


#main body

# checking for the number of command line arguments
if [[ $# == 0 ]]
then
	#checking whether to run backup or disk utilization
	echo "You have entered $# command line argument(s)."
	read -p "Please select 'backup' or 'disk_utility_check' or 'database_backup': " ENTERED1
	
	#prompting for arguments for backup 
	if [[ ${ENTERED1} == "backup" ]]
	then
		read -p "please enter source path: " source
		read -p "please enter destination path: " dest 
		read -p "please enter a runner: " runner
		TS=$(date +'%m%d%y')
		destination=${dest}/${runner}_${TS}
	
		#calling backup function
		backup_f_d ${source} ${destination} ${runner}
		
	#prompting for disk utilization arguments
	elif [[ ${ENTERED1} == "disk_utility_check" ]]
	then
		echo "performing disk utilization check."
		read -p "please enter disk name ('/u01', '/u02', '/u03' or 'backup'): " disk
		read -p "please enter threshold value: " threshold
	
		# calling the disk utilization function
		disk_util_check ${disk} ${threshold}
		
	#prompting for database schema backup arguments
	elif [[ ${ENTERED1} == "database_backup" ]]
	then
		TS=$(date +'%m%d%y%H%M%S')
		read -p "please provide userid: " user
		read -p "please provide schema: " schema1
		read -p "please provide a runner: " runner_db
		read -p "please provide directory: " directory1
	
		#touch /home/oracle/scripts/practicedir_isa_sep23/${schema1}_${runner_db}_${TS}.par
		expdp_file=/home/oracle/scripts/practicedir_isa_sep23/${schema1}_${runner_db}_${TS}.par		
	
		echo "userid='/ as ${user}'" > ${expdp_file}
		echo "schemas=${schema1}" >> ${expdp_file}
		echo "dumpfile=${schema1}_${runner_db}_${TS}.dmp" >> ${expdp_file}
		echo "logfile=${schema1}_${runner_db}_${TS}.log" >> ${expdp_file}
		echo "directory=${directory1}" >> ${expdp_file}

		#calling database function
		database_backup
		
		#checking if the DB schema backup was successful
      if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${schema1}_${runner_db}_${TS}.log )
		then
			echo "Database Schema backup completed successfully."
         #printing the results of the destination
         ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}
      else
         echo "Database Schema backup FAILED!"
         exit
      fi
	else
		echo "please choose 'backup' or 'disk_utility_check' or 'database_backup' only"
	fi


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

#checking for condtions for disk utilization functions with command line arguments passed
elif [[ $# == 3 ]] && [[ $1 == "disk_util_check" ]]
then
	echo "You have entered $# command line arguments."
	#calling the disk utilization function
	disk=$2
	threshold=$3	
	disk_util_check ${disk} ${threshold}

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
	
	#checking if the DB schema backup was successful
	if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${schema1}_${runner_db}_${TS}.log )
	then
		echo "Database Schema backup completed successfully."
		#printing the results of the destination
		ls -ltr /backup/AWSSEP23/APEXDB | grep ${runner_db}
	else
		echo "Database Schema backup FAILED!"
		exit
	fi
else
	#checking for errors in both functions and providing usage
	echo "ERROR! You have entered $# command line arguments."
	echo "USAGE: For a backup, please run script with 4 command line arguments as below: "
	echo "./scriptname source_path destination_path runner."
	echo "USAGE: For disk utilization check, please run script with 3 command line arguments as below: "
	echo "./scriptname disk_name threshold."
	echo "USAGE: For database schema backup, please enter 'database_backup' only."
	echo "Or enter 'database_backup, followed by 5 command line arguments in the following order: '"
	echo "/scriptname database_backup userid schema runner directory"
fi



