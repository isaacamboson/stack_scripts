#!/usr/bin/python

def get_server_dictionary():
	servers={
    "hosts":[{"MKIT-DEV-OEM":"ON_PREM"},{"STACKCLOUD":"CLOUD"}],
    "disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
    "transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }

	return servers

"""
def add(a,b):
	z=a+b
	return z

def sub(a,b):
	z=a-b
	return z
	
def mul(a,b):
	z=a*b
	return z
"""


#Main body
if __name__ == "__main__":
	"""	
	add(a,b)
	sub(a,b)
	mul(a,b)
	"""

	get_server_dictionary()


