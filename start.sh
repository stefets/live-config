#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start the live music system
module='Roland Corp. EDIROL SD-90'
data='/mnt/flash/live'

#Mount flash 
sh $DIR/unmount.sh
sh $DIR/mount.sh > /dev/null
if ! [ -d "$data" ]
then
	echo "$data not found"
	exit 1
fi

#Check sound module
if [ $(lsusb | grep -c "$module") -eq 0 ]
then
	echo "$module not found"
	exit 1
fi

# OK
cd $DIR
python $DIR/live.py
