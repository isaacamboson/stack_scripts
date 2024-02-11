#!/bin/bash

#Accept Command Line Arguments - CONTROL_SCRIPT_1.4

#variable declaration
source=$1
dest=$2
runner=$3
TS=$(date '+%m%d%y%H%M%S')
destination=${dest}/${runner}/${TS}

mkdir -p ${destination}

ls -ltr ${destination}

#copying file from source to destination
echo "copying file ${source} to ${destination}"
cp -r ${source} ${destination}
echo "file ${source} has been successfully copied to ${destination}"

ls -ltr ${destination}




































