#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start the live music system
module='Roland Corp. EDIROL SD-90'
data='/mnt/flash/music/soundlib'

#Check sound module
if [ $(lsusb | grep -c "$module") -eq 0 ]
then
	echo "$module not found"
	exit 1
fi

#Mount the usb flash stick containg audio files
sudo mkdir -m777 -p /mnt/flash
sudo mount /dev/sda1 /mnt/flash
if  [ ! -d "$data" ]
then
	echo "$data not found"
	exit 1
fi

# Create a symlink in /tmp with the usb soundlib 
ln -sf /mnt/flash/music/soundlib /tmp/soundlib

# OK
cd $DIR
/bin/bash $DIR/menu.sh
