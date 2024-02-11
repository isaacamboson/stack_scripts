#!/usr/bin/python

import os

if os.popen("if (grep \"successfully completed\" /backup/AWSSEP23/APEXDB/stack_temp_UCHE_15012024160226.log)") == True:
	print("Correctttttt!")

