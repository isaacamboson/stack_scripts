#!/usr/bin/python

#Module declaration
import sys
import stack_modules as sm

#variables
hostname="MKIT-DEV-OEM"

if __name__ == "__main__":

	dict_output=sm.get_server_dictionary()
	#print(dict_output)
	
"""
# checking for the hard-coded hostnames if they are cloud or on-prem servers
	if (dict_output["hosts"][0]["MKIT-DEV-OEM"]) == "ON_PREM":
		print("This is an on-prem server")
	elif (dict_output["hosts"][1]["STACKCLOUD"]) == "CLOUD":
		print("This is a cloud server")
"""

# method 3:
hostname = "MKIT-DEV-OEM"
dict_hosts = dict_output["Hosts"]
for each_host in dict_hosts:
    if each_host == hostname:
        print("{} is an {} server.".format(each_host, dict_hosts[each_host]))


