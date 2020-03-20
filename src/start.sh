#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Vars
flash="/mnt/flash"
audio="$flash/music/soundlib"

#Mount usb flash
sudo mkdir -m777 -p $flash
count=$(df | grep -c sda1)
if [ $count -eq 0 ]
then
	sudo mount /dev/sda1 $flash
fi

ln -sf $audio /tmp/soundlib

/bin/bash $DIR/menu.sh
