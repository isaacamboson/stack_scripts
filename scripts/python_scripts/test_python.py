#!/bin/usr/python

import sys

"""
name = "Isaac"
print("The length of my name is {}.".format(len(name)))


b = "Isaac "
print(b.strip()) 


threshold = "65%"
s_threshold = threshold.strip("%")
new_threshold = int(s_threshold)
if new_threshold > 75:
	print("The threshold of {} is greater than 75".format(new_threshold))
else:
	print("The threshold of {} is less than 75".format(new_threshold))


threshold = "65%"
new_threshold = int(threshold.strip("%"))
if new_threshold > 75:
	print("The threshold of {} is greater than 75".format(new_threshold))
else:
	print("The threshold of {} is less than 75".format(new_threshold))


b = "Isaac"
print("My name in upper case is {}.".format(b.upper()))
print("My name in lower case is {}.".format(b.lower()))


a = "Stack"
print(a.replace("S", "C"))


threshold = "65%"
new_threshold = int(threshold.replace("%", ""))
if new_threshold > 75:
	print("The threshold of {} is greater than 75".format(new_threshold))
else:
	print("The threshold of {} is less than 75".format(new_threshold))


new_file = open("test_replace.txt", "w")
new_file.write("baseball")
new_file.close()

view_file = open("test_replace.txt", "r")
file_content = view_file.read()
print(file_content)
view_file.close()

text = "basketball"
rep_base = file_content.replace("baseball", text)

write_file = open("test_replace.txt", "w")
write_file.write(rep_base)
write_file.close()

vf = open("test_replace.txt", "r")
vf_read = vf.read()
print(vf_read)
vf.close()


fullname = "Isaac,Amboson"
tokens = fullname.split(",")
print(tokens[1])


disks = "/u01, /u02, /u03, /u04, /u05, /backup"
token = disks.split(", ")
new_token = token[5].strip("/")
if new_token == "backup":
	print("This is a backup directory")
else:
	print("This is not a backup directory")


txt = "Stack IT training students stack up a lot of bread."
if "bread" in txt:
	print("bread exists in the statement.")


txt = "Stack IT training students stack up a lot of bread."
if "Stack" in txt:
	cnt = txt.count("Stack")
	print("Stack appears {} times.".format(cnt))


txt = "Stack IT training students stack up a lot of bread."
new_text = txt.lower()
if "stack" in new_text:
	cnt = new_text.count("stack")
	print("stack appears {} times.".format(cnt))


#arbitrary arguments: one "*" means the arguments are passed as a list
def my_function(*names):
	#at run time, names is assigned a list of the arguments provided
	print("The youngest child is " + names[2])

#calling the function
my_function("John", "Jeff", "Rachel")


def add(*entries):
	print(sum(entries))

add(5,6)


def add(*entries):
	total = entries[0] + entries[1]
	print(total)

add(5,6) 


#key word arguments
def my_function(name3, name1, name2):
	print("My name is " + name1)

my_function(name1="Isaac", name3="Jose", name2="Rachel")


#arbitrary keyword arguments: at runtime the arguments become a dictionary
def my_function(**names):
	print("Isaac's lastname is " + names["lname"] + " and he is " + str(names["Age"]) + " years old.")


my_function(fname="Isaac", lname="Amboson", Age=29)



def add(**numbers):
	x = numbers["f_number"] + numbers["s_number"]
	print(x)

def sub(**numbers):
	x = numbers["f_number"] - numbers["s_number"] 
	print(x)

def mul(**numbers):
	x = numbers["f_number"] * numbers["s_number"]
	print(x)


operation = sys.argv[1]
numb1 = int(sys.argv[2])
numb2 = int(sys.argv[3])

if operation == "add":
	add(f_number=numb1, s_number=numb2)	
elif operation == "sub":
	sub(f_number=numb1, s_number=numb2)
elif operation == "mul":
	mul(f_number=numb1, s_number=numb2)
else:
	print("Please choose one operation from 'add', 'sub' or 'mul' and provide two digits.")
	print("example: python *scriptname* add 7 8")
"""


name = "isaac"
print(name.capitalize())




















