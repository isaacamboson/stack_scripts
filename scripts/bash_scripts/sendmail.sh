#!/bin/bash


 read -p "Do you want to send an email?" INPUT
  6 if [[ ${INPUT} == "yes" ]]
  7 then
  8    echo "You chose to send an email" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
  9 else
 10    echo "You chose not to send an email."
 11 fi
 12
 13 # you can use this will sending emails if your exit status fails

