#!/bin/bash 

sudo mkdir -m777 -p /mnt/flash
sudo mount -o uid=1000,gid=1000 /dev/sda1 /mnt/flash 2>/dev/null
