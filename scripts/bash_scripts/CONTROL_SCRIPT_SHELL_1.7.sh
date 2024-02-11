#!/bin/bash


#disk utilization check function

$disk='/u01'
$threshold='60'

disk_util_check()
{
	echo "checking disk utilization..."

	current_use=$(df -h | grep ${disk} | awk '{print $4}' | sed 's/%//g')
	if [[ ${current_use} -ge ${threshold} ]]
	then
		echo "The disk utilization is above the ${threshold}% threshold!"
		echo "Please address this issue."
	else
		echo "The disk utilization is within the ${threshold}% threshold."
		echo "No action needed."
	fi
}


