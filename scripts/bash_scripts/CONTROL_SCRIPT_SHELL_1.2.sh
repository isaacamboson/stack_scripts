#!/bin/bash

#create backup directories with timestamp - CONTROL_SCRIPT_1.2

#variable declaration
source=/home/oracle/scripts/practicedir_isa_sep23/testdir
dest=/home/oracle/scripts/practicedir_isa_sep23/backup
TS=$(date '+%m%d%y%H%M%S')

#destination=${dest}/$(basename "$source")_${TS}
destination=${dest}/testdir_${TS}

ls -ltr /home/oracle/scripts/practicedir_isa_sep23/backup/
echo "copying file from ${source} to ${destination}"
cp -r ${source} ${destination}

#listing the content of the backup directory:
ls -ltr /home/oracle/scripts/practicedir_isa_sep23/backup/


