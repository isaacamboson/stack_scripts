#!/usr/bin/python

import credit_check as cc
import json 



if __name__ == "__main__":

	"""
	ssn = input("Please provide you Social Security Number: ")
	val = cc.credit_check(ssn)
	print(val)
	if val >= 720:
		print("Approved.")
	else:
		print("Not Approved.")

	"""

	#opening .json file
	new_file = open("/home/oracle/scripts/practicedir_isa_sep23/customer.json")

	#returning .json file as a dictionary
	records = json.load(new_file)

	for each in records["customer"]:
		a_ssn = (each["SSN"])
		print("Social Security #:", a_ssn)

		#calling the credit check function to check each credit score tied to each SSN from the database
		cc.credit_ck(a_ssn)

	new_file.close()





