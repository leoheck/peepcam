#!/bin/bash

# Action script for motion project
# Leandro Heck

logfile="/var/log/peepcam/motion-action.log"

logfile_path=$(dirname "${logfile}")
mkdir -p "${logfile_path}"
chmod 777 "${logfile_path}"

datetime=$(date +"%Y.%m.%d %Hh%M'%S")

echo "${datetime} - ${0} ${@}" >> ${logfile}
chmod 777 "${logfile}"

python "/home/lheck/peepcam/bin/send-to-telegram.py" "${@}" | tea -a ${logfile}
