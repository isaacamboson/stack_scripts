#!/usr/bin/python


"""
servers={"Hostname":"MKIT-DEV-OEM"}
print(servers["Hosts"])
"""
# ex. 1:
# servers={
#     "hosts":[{"MKIT-DEV-OEM":"ON_PREM"},{"STACKCLOUD":"CLOUD"}],
#     "disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
#     "transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
#     }

# # working with the "hosts" dictionary
# print(servers["hosts"])                         #prints - {'MKIT-DEV-OEM': 'ON_PREM'}, {'STACKCLOUD': 'CLOUD'}]
# print(servers["hosts"][0])                      #prints - {'MKIT-DEV-OEM': 'ON_PREM'}
# print(servers["hosts"][0]["MKIT-DEV-OEM"])      #prints - ON_PREM

# # working with the "disks" dictionary
# print(servers["disks"])                         #prints - ['/u01', '/u02', '/u03', '/u04', '/u05', '/backup']
# print(servers["disks"][0])                      #prints - /u01
# print(servers["disks"][5])                      #prints - /backup

# # testing a conditional statement with lists
# names = ["Mike", "Rasheed", "Nick"]
# if "Mike" in names:
#     print("Mike is in this list.")              #prints - Mike is in this list.


#ex. 2:
servers={
    "hosts":[{"MKIT-DEV-OEM":"ON_PREM"},{"STACKCLOUD":"CLOUD"}],
    "disks":["/u01","/u02","/u03","/u04","/u05",{"disk_type":"NFS"}],
    "transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }

#how to print the value for "disk_type"
print(servers)                                     #prints - the entire "servers" dictionary
print(servers["disks"])                            #prints - ['/u01', '/u02', '/u03', '/u04', '/u05', {'disk_type': 'NFS'}]
print(servers["disks"][5])                         #prints - {'disk_type': 'NFS'}
print(servers["disks"][5]["disk_type"])            #prints - NFS



"""
servers={
    "Hosts":{"MKIT-DEV-OEM":"ON-PREM","STACKCLOUD":"CLOUD"},
    "Disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
    "Transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }
"""
