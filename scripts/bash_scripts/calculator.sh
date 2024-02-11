#!/bin/bash

#addition function

add_funct()
{
	result=$( expr ${f_add} + ${s_add} )
	if (( $? == 0 ))
	then
		echo $result
		echo "Your result is $result" | mailx -s "Your function worked!" stackcloud11@mkitconsulting.net
	else
		echo "function failed to run!"
	fi
}

#subtraction_function
sub_funct()
{
	result=$( expr ${f_sub} - ${s_sub} )
	if (( $? == 0 ))
	then
		echo $result
		echo "Your result is $result" | mailx -s "Your function worked!" stackcloud11@mkitconsulting.net
	else
		echo "function failed to run!"
	fi
}

#multiplication function
mult_funct()
{
	result=$( expr ${f_mult} \* ${s_mult})
	if (( $? == 0 ))
	then
		echo $result
		echo "Your result is $result" | mailx -s "Your function worked!" stackcloud11@mkitconsulting.net
	else
		echo "function failed to run!"
	fi
}

#prompting user for the type of arithmetic operation
read -p "Hello, what operation would you like to perform? " INPUT

case $INPUT in

	ADD)
		echo "calling addition function..."
		read -p "please provide first digit: " f_add
		read -p "please provide second digit: " s_add
		
		#calling addition function
		add_funct		
		;;
 	SUB)
		echo "calling the subtraction function..."
		read -p "please provide first digit: " f_sub
		read -p "please provide second digit: " s_sub

		#calling subtraction function
		sub_funct
	 	;;
	MUL)
      echo "calling the multiplication function..."
		read -p "please provide the first digit: " f_mult
		read -p "please provide the second digit: " s_mult
	
		#calling multiplication function
		mult_funct
   	;;
   *)
 	   echo "You entered an invalid function"
   	;;
esac

