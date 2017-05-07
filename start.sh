#!/bin/bash

# Start the live music system

module='Roland Corp. EDIROL SD-90'
data='/mnt/flash/live'

#Check & Unmount & ReMount flash
sh ./unmount.sh &> /dev/null
sh ./mount.sh > /dev/null
if ! [ -d "$data" ]
then
	echo "$data not found"
	exit 1
fi

#Check module
if [ $(lsusb | grep -c "$module") -eq 0 ]
then
	echo "$module not found"
	exit 1
fi

# OK
python ./live.py
