#!/usr/bin/python

#imported modules
import sys

"""
def myfirstfunction(a,b,c):
	print("My name is {}, {}, {}".format(a,b,c))

x,y,z="isaac","Brittany","Abigail"

myfirstfunction(x,y,z)
"""

"""
#def check_function():
"""


#taking command line arguments


def myfirstfunction(a,b,c):
	print("The values entered into the module are {} {} {}".format(a,b,c))
	if int(a)>6:
		print("{} is greater than 6".format(a))

# anything below can only run when this script is being run itself
# if this module is being called by another script, everything below does not run
if __name__=="__main__":
	x,y,z=sys.argv[1],sys.argv[2],sys.argv[3]
	count_args=len(sys.argv) - 1
	print("The number of command line arguments is {}".format(count_args))

	myfirstfunction(x,y,z)



