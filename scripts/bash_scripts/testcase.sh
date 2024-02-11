#!/bin/bash

#disk utilization function
disk_util()
{
	echo "This is the disk Utilization function"
}

#database backup function
db_backup()
{
	echo "This is the database backup function"
}

#file and directory backup function
file_dir_backup()
{
	echo "This is the file and directory function"
}

#AWS function
AWS_backup()
{
	echo ""This is the AWS function
}

#prompting user for function type
read -p "Hello, what function would you like to call? " input

case $input in
	
	disk_utilization)
		disk_util
	;;
	
	database_backup)
		db_backup
	;;

	file_directory_backup)
		file_dir_backup
	;;

	AWS)
		AWS_backup
	;;

	*)
		echo "You entered an invalid function."
	;;

esac

