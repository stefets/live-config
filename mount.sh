#!/bin/bash 

sudo mkdir -m777 -p /mnt/flash
sudo umount /mnt/flash
sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/flash
find /mnt/flash
