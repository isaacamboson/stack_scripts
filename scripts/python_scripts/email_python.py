#!/usr/bin/python

import smtplib

#variables
TO_EMAIL = "stackcloud11@mkitconsulting.net"
SUBJECT = "Test Email Isaac"
BODY = "This is a test email."
FROM = "oracle@MKIT-DEV-OEM.localdomain"

#MSG=("\n".join(("From: {}".format(FROM), "To: {}".format(TO_EMAIL), "Subject: {}:\n".format(SUBJECT), "{}".format(BODY)))

MSG = ("\n".join(("From: %s" %FROM, "To: %s" %TO_EMAIL, "Subject: %s:\n" %SUBJECT, "%s" %BODY)))

with smtplib.SMTP('localhost') as my_server:
	my_server.sendmail(FROM, TO_EMAIL, MSG)
	print("Email sent successfully to {}".format(TO_EMAIL))




