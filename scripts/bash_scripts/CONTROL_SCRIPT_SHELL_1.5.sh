#!/bin/bash

#create backup_f_d function CONTROL_SCRIPT_1.5

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
	echo "checking disk utilization"
	df -h
}


#main body
function=$1

if [[ $function == "backup" ]]
then
	#variable declaration
	source=$2
	TS=$(date +'%m%d%y%H%S')
	dest=$3
	runner=$4
	destination=${dest}/${runner}/${TS}
	
	#calling the backup function
	echo "backing up ${source} to ${destination}"
	backup_f_d ${source} ${destination} ${runner}

elif [[ ${function} == "disk_util_check" ]]
then
	#calling the disk utilization function
	threshold=$2
	disk_util_check ${threshold}
else
	echo "please choose backup or disk_util_check"
fi
























