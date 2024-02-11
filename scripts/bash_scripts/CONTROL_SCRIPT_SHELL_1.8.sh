#!/bin/bash


#disk utilization check function

disk_util_check()
{
	echo "checking disk utilization..."

	# checking the disk utilization	
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


#main body

disk=$1
threshold=$2

if [[ ${disk} == "/u01" ]]
	then
		disk_util_check ${disk}
elif [[ ${disk} == "/u02" ]]
	then
		disk_util_check ${disk}
elif [[ ${disk} == "/u03" ]]
	then
		disk_util_check ${disk}
elif [[ ${disk} == "/u04" ]]
	then
		disk_util_check ${disk}
elif [[ ${disk} == "backup" ]]
	then
		disk_util_check ${disk} ${threshold}
else
	echo "Please enter a valid disk value."
fi


