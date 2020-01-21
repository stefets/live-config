#!/bin/bash

#
# Create/overwrite a symlink in /tmp for each mp3 file found by find in the $target directory
#

# Clear existing symlink
rm -f /tmp/*.mp3

target=$1
root=$2
system=$root/system

# counter = note number from the keyboard, adjustable offset
# Starting at note #12 give me notes 0-11 free :)
counter=12

# Scenes
for file in $(find $target -name "*.mp3" -type f | sort)
do
	ln -fs $file /tmp/$counter.mp3
	let counter++
done

# System
counter=5
for file in $(find $system -name "*.mp3" -type f | sort)
do
	ln -fs $file /tmp/$counter.mp3
	let counter++
done
