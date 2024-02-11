#!/bin/bash


#create unique backup directories - CONTROL_SCRIPT_1.3

#variable declaration
source_file=/home/oracle/scripts/practicedir_isa_sep23/isaac_file.txt
TS=$(date +'%m%d%y%H%S')
runner=isaac
destination=/home/oracle/scripts/practicedir_isa_sep23/backup/${runner}/${TS}

#creating the runner and timestamped directory
mkdir -p ${destination}

#listing the empty, newly created runner and timestamped directory
ls -ltr ${destination}

#copying from the source to the runner and timestamped directory
cp ${source_file} ${destination} 

#listing the content of the backup/runnner/timestamped directory
ls -ltr ${destination}


