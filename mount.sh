#!/bin/bash 

sudo mkdir -m777 -p /mnt/flash
sudo umount /mnt/flash
sudo mount /dev/sda1 /mnt/flash
find /mnt/flash
