#!/usr/bin/python

import cx_Oracle


#def credit_check(ssn):
	
#	connection = cx_Oracle.connect(user="STACK_ISA_SEP23", password="stackinc", dsn="MKIT-DEV-OEM/APEXDB")
#	print(connection.version)
#	cursor = connection.cursor()

#	cursor.execute("""select * from credit_check""")
#	select_result = cursor.fetchall()
#	for each in select_result:
#		ssn_db = each[0]
#		c_score_db = each[1]
#		if ssn == ssn_db:
#			print(c_score_db)
#			if c_score_db >= 720:
#				print("Approved")
#			else:
#				print("Not Approved")
#	
#	connection.commit()
#	cursor.close()
#	connection.close()
#


def credit_ck(ssn):
	connection = cx_Oracle.connect(user="STACK_ISA_SEP23", password="stackinc", dsn="MKIT-DEV-OEM/APEXDB")
#	print(connection.version)
	cursor = connection.cursor()

	cursor.execute("""select credit_score from credit_check where SSN = :INP_SSN""", INP_SSN = ssn)
	select_result = cursor.fetchall()
	for each in select_result:
		crd_sc = each[0]

		print("Credit Score:", crd_sc)
		if crd_sc >= 720:
			print("Approved. Credit Score is 720 or above.")
			print("----------------------------------------")
		else:
			print("Not Approved. Credit Score is below 720.")
			print("----------------------------------------")

	connection.commit()
	cursor.close()
	connection.close()
	




