#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start the live music system
module='Roland Corp. EDIROL SD-90'

failed=0

#Check MIDI sound module
if [ $(lsusb | grep -c "$module") -eq 0 ]
then
	echo "$module not found"
	failed=1
fi

#Mount the usb flash stick containg audio files
data='/mnt/flash/music/soundlib'
sudo mkdir -m777 -p /mnt/flash
sudo mount /dev/sda1 /mnt/flash
if  [ ! -d "$data" ]
then
	echo "$data not found, force create"
	mkdir -p $data
	failed=1
fi

if  [ $failed -eq 1 ]
then
	read -n 1 -s -r -p "WARNING - press any key to continue or ctrl-c to abort"
fi

# Create a symlink in /tmp with the usb soundlib 
ln -sf /mnt/flash/music/soundlib /tmp/soundlib

/bin/bash $DIR/menu.sh
