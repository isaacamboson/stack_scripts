#!/bin/bash


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

#variable declaration
disk=$1
threshold=$2

#checking for number of command line arguments
if [[ $# -eq 2 ]]
then
	echo "You have entered $# command line arguments."
	echo "This is the required number of command line arguments."
	
	#calling the disk util function for each disk
	disk_util_check

else
	echo "You have entered $# command line argument(s)."
	echo "ERROR! This script requires two command line arguments."
	echo "And please run script in the following format: ./scriptname disk_name threshold_value."
	
fi


