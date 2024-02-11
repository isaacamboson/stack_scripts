#!/bin/bash


DB=$1

#running oracle database environment variable script
. /home/oracle/scripts/oracle_env_APEXDB.sh

#write if statement to see if this is true
if [[ ps -ef | grep pmon | grep APEXDB ]]
then
	echo "APEXDB database is running. But this does not mean it is OPEN."

	sqlplus stack_temp/stackinc@APEXDB<<EOF
	set echo on feedback on
	spool /home/oracle/scripts/practicedir_isa_sep23/db_status.log
	show user
	select * from global_name;
	select status from v\$instance;
	spool off
EOF

else
	echo "APEXDB database is not running."
	exit
fi

