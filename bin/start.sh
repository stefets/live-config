#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#TODO Array of module
modules='Roland Corp. EDIROL SD-90'
flash="/mnt/flash"
audio="$flash/music/soundlib"
failed=0

#Check modules
if [ $(lsusb | grep -c "$modules") -eq 0 ]
then
	echo "$modules not found"
	failed=1
fi

#Mount usb flash
sudo mkdir -m777 -p $flash
# Check if / is mount in sda*
count=$(df / | grep -c sda1)
if [ $count -eq 0 ]
then
	sudo mount /dev/sda1 $flash
else
	sudo mount /dev/sdb1 $flash
fi

# Audio directory
mkdir -p $audio
if  [ ! -d "$audio" ]
then
	echo "$audio directory not found"
	failed=1
else
	# symlink 
	ln -sf $audio /tmp/soundlib
fi

if  [ $failed -eq 1 ]
then
	read -n 1 -s -r -p "*** WARNING *** - press any key to continue or ctrl-c to abort"
fi

/bin/bash $DIR/menu.sh
