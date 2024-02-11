#!/bin/bash



backup_f_d()
{
	echo "copying file $source to $dest"

}

aws()
{
	echo "which AWS function do you want to perform?"
	read -p "For IAM enter 1: " ENTERED #whatever the user enters gets stored in the ENTERED variable	
	if  (( $ENTERED == 1 ))
	then
		echo "You have chosen the IAM service"
	fi
}



#main body

function=$1

if [[ $function == "backup" ]]
then
	source=$2
	dest=$3
	#calling backup function

	backup_f_d $source $dest
elif [[ $function == "aws" ]]
then
	#calling the aws function
	aws
else
	echo "your function is not defined"
fi


