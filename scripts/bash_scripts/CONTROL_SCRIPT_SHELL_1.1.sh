#!/bin/bash

#create static file copy with timestamp 1.1

#variable declaration
source=/home/oracle/scripts/practicedir_isa_sep23/CONTROL_SCRIPT_1.0.sh
dest=/home/oracle/scripts/practicedir_isa_sep23/backup/CONTROL_SCRIPT_1.0
TS=$(date '+%m%d%y%H%M%S')
destination=${dest}_${TS}.sh

ls -ltr /home/oracle/scripts/practicedir_isa_sep23/backup/
echo "copying file from ${source} to ${destination}"
cp ${source} ${destination}

# listing the content of the backup directory:
ls -ltr /home/oracle/scripts/practicedir_isa_sep23/backup/

