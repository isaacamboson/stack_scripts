#!/usr/bin/python

import json

#opening .json file
new_file = open("/home/oracle/scripts/practicedir_isa_sep23/customer.json")

#returning .json file as a dictionary
records = json.load(new_file)

for each in records["customer"]:
	print(each["SSN"])
		



new_file.close()

