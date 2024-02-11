#!/usr/bin/python

import os

"""
#taking input
user_entry = int(input("Please enter first name: "))
print("User entered: {}".format(user_entry))
print(type(user_entry))
"""


#for loops in ranges

#for x in range(2,10):
#	print(x)

#for x in range(2,10,2):
#	print(x)

"""
#creating/writing into a file
fo = open("test_isaac.par","w+")
#print("The name of the file is {}".format(fo.name))
#print("Is {} closed? {}".format(fo.name, fo.closed))
fo.write("userid='/ as sysdba'\nschemas=stack_temp\ndumpfile=stacktemp_dump_isaac.dmp\nlogfile=stacktemp_dump_isaac.log\ndirectory=DATA_PUMP_DIR")
fo.close()
#print("Is {} closed? {}".format(fo.name,fo.closed))

#opening and reading from a file
file_view = open("/home/oracle/scripts/practicedir_isa_sep23/test_isaac.par", "r+")
file_content = file_view.read()
print(file_content)
file_view.close()
"""

"""
#creating a new file to write into it
new_file = open("/home/oracle/scripts/practicedir_isa_sep23/writefile.txt", "w")
new_file.write("Hello World,\nI am learning how to read and write to files.")
#print(new_file)
new_file.close()

#opening the file that was last created to be read
new_file2 = open("/home/oracle/scripts/practicedir_isa_sep23/writefile.txt", "r")
file_content = new_file2.read()
print(file_content)
new_file2.close()
"""


dir_content = os.listdir('.')
print(dir_content)



