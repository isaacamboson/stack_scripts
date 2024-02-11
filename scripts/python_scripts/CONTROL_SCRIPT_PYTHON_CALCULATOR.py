#!/usr/bin/python

#Module declaration
import sys
import stack_modules as sm

#variables
hostname="MKIT-DEV-OEM"

"""
#variable declaration
print(type(sys.argv[1]))
print(type(sys.argv[2]))

x=int(sys.argv[1])
y=int(sys.argv[2])

print(type(x))
print(type(y))

#function declaration
def calc(x,y):
	g=sm.add(x,y)
	print(g)
	g=sm.sub(x,y)
	print(g)
	g=sm.mul(x,y)
	print(g)
"""


if __name__ == "__main__":
#	calc(x,y)

	dict_output=sm.get_server_dictionary()
	print(dict_output)






