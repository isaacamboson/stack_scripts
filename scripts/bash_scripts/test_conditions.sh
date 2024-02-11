#!/bin/bash



x=$1
y=$2

<<comment
if (( x!=5 ))
then 
	echo "x is not equal to 5"
else
	echo "x is equal to 5"
fi
comment


if (( $x == 5 ))
then
	echo "x is equal to 5"
elif (( $x == 6 ))
then 
	echo "x is equal to 6"
elif (( $x == 7 ))
then
	echo "x is equal to 7"
elif (( $x == 8 ))
then 
	echo "x is equal to 8"
elif (( $x == 9 ))
then 
	echo "x is equal to 9"
else
	echo "x fails all the conditions."
fi

if [[ $y == "YINKA" ]]
then
	echo "$y is STUDENT"
elif [[ $y == "WILSON" ]]

then
	echo "$y is a STUDENT"
elif [[ $y == "LEKE" ]]
then
	echo "$y is a STUDENT"
elif [[ $y == "NICK" ]]
then
	echo "$y is a STUDENT"
else 
	echo "y is not STUDENT"
fi





#check exit status
cp /home/oracle/scripts/practicedir_isa_sep23/rubbish.txt /home/oracle/scripts/practicedir_isa_sep23/backup/

if (( $? != 0 ))
then 
	echo "copy command failed."
fi




