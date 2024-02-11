#!/bin/bash


if ( ls -ltr /home/oracle/scripts/practicedir_isa_sep23/test10.txt )
then
	echo "File exists"
else
	echo "File does not exist."
fi

if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/expdp_stack_temp_isaac.log )
then 
	echo "backup completed successfully."
else
	echo "backup failed"
fi

