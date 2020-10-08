#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Vars
flash="/mnt/flash"
audio="$flash/music/soundlib"
menu="$DIR/menu.sh"

#Mount usb flash
#sudo mkdir -m777 -p $flash
#count=$(df | grep -c sda1)
#if [ $count -eq 0 ]
#then
#	sudo mount /dev/sdb1 $flash
#fi

ln -sf $audio /tmp/soundlib

chmod 755 $menu
$menu
