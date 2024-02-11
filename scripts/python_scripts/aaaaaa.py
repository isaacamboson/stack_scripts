#!/usr/bin/python

import os
import cx_Oracle


connection = cx_Oracle.connect(user="STACK_ISA_SEP23", password="stackinc", dsn="MKIT-DEV-OEM/APEXDB")
print(connection.version)

cursor = connection.cursor()
var1 = cursor.execute("""select * from prod_operations""")
print(var1)

connection.commit()
cursor.close()
connection.close()



