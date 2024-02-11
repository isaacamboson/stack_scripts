#!/usr/bin/python

import credit_check as cc




if __name__ == "__main__":

	ssn = input("Please provide you Social Security Number: ")
	val = cc.credit_check(ssn)
	print(val)
	if val >= 720:
		print("Approved.")
	else:
		print("Not Approved.")



