#!/bin/bash

echo "Hi, I am happy to be in class today."

read -p "Please enter function: " INPUT

case $INPUT in

	ADD)
		echo "calling addition function"
	;;

	SUB)
		echo "calling the subtraction function"
	;;

	MUL)
		echo "calling the multiplication function"
	;;
	
	*)
		echo "You entered an invalid function"
	;;

esac

