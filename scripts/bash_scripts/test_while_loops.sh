#!/bin/bash

while read LINE
do	
	mkdir -p /home/oracle/scripts/practicedir_isa_sep23/backup2
	cp $LINE /home/oracle/scripts/practicedir_isa_sep23/backup2
done</home/oracle/scripts/practicedir_isa_sep23/files.txt

