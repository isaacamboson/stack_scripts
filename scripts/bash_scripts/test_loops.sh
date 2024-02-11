#!/bin/bash



schemas="stack_temp stack_mike stack_wilson"



#for loop using list
for name in $schemas
do
	
	TS=$(date '+%m%d%y%H%M%S')
	. /home/oracle/scripts/oracle_env_APEXDB.sh
	echo "userid='/ as sysdba'" > export_${name}.par
	echo "schemas=${name}" >> export_${name}.par
	echo "dumpfile=${name}_${TS}.dmp" >> export_${name}.par
	echo "logfile=${name}_${TS}.log" >> export_${name}.par
	echo "directory=DATA_PUMP_DIR" >> export_${name}.par

	expdp parfile=export_$name.par

	sleep 30
done

<<comment
#for loop using range
for value in {1..5}
do

	echo "The value is: $value"

done
comment


