#!/usr/bin/python

import tarfile

file_name = "/home/oracle/scripts/practicedir_isa_sep23/stack_mike_isaac_011224023743_1.dmp.tar"
file_tar = tarfile.open(file_name, "w")

file_tar.add("stack_mike_isaac_011224023743_1.dmp")

file_tar.close()


