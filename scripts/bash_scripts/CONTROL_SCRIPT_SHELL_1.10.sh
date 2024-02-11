#!/bin/bash


#function for backup
backup_f_d()
{
	echo "copying ${source} to ${destination}"	
	mkdir -p  ${destination}
	cp -r ${source} ${destination}
	echo "${source} has been copied to ${destination}"
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
      echo "Please address this issue."
   else
      echo "The disk utilization is within the ${threshold}% threshold."
      echo "No action needed."
   fi
}

#main body



# checking for the number of command line arguments
if [[ $# == 0 ]]
then
	#checking whether to run backup or disk utilization
	echo "You have entered $# command line argument(s)."
	read -p "Please select 'backup' or 'disk_utility_check': " ENTERED1
	
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
	else
		echo "please choose 'backup' or 'disk_utility_check' only"
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
else
	#checking for errors in both functions and providing usage
	echo "ERROR! You have entered $# command line arguments."
	echo "USAGE: For a backup, please run script with 4 command line arguments as below: "
	echo "./scriptname source_path destination_path runner."
	echo "USAGE: For disk utilization check, please run script with 3 command line arguments as below: "
	echo "./scriptname disk_name threshold."
fi
























