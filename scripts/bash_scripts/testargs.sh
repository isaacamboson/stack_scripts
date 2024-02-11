#!/bin/bash

#variable declaration
source=$1
dest=$2
TS=$(date '+%m%d%y')
destination=${dest}/${TS}
#echo "This script has $# command line arguments"


if [[ $# -eq 0 ]]
then
	echo "No command line arguments were provided."
	read -p "Enter source path: " ENTERED1
	read -p "Enter destination path: " ENTERED2
	echo "You have entered ${ENTERED1} as the source path, and"
	echo "${ENTERED2} as destination path."
elif [[ $# -eq 2 ]]
then
	echo "The scripts has $# command line arguments."
	echo "The correct command line arguments were provided."
	echo "source_path = ${source}"
	echo "dest_path = ${dest}"
else
	echo "USAGE: This requires two command line arguments."
	echo "The two command line arguments should begin with a SOURCE"
	echo "and a DESTINATION."
	echo "an example of such will be:"
	echo "./name_of_script source_file destination_file"
	exit
fi

echo "I am continuing."


<<comment
#main body
#creating backup location 
mkdir -p ${destination}

#copying file or directory from source to destination
echo "copying file ${source} to ${destination}"
cp -r ${source} ${destination}
echo "file $source has been successfully copied to $destination"
comment


