#!/usr/bin/python

import tarfile

file = tarfile.open("/home/oracle/scripts/practicedir_isa_sep23/stack_mike_isaac_011224023743_1.dmp.tar.gz")

file.extractall("/home/oracle/scripts/practicedir_isa_sep23")

file.close()
