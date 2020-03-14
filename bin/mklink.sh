#!/bin/bash

#
# Create/overwrite a symlink in /tmp for each mp3 file found by find in the $target directory
#

# Clear existing symlink
rm -f /tmp/*.mp3

target=$1
root=$2

# Keyboard theme reserved at note 12
theme=$root/system/theme.mp3
ln -fs $theme /tmp/12.mp3

# Note number from the keyboard, adjustable offset
note_number=13

# Scenes
for file in $(find $target -name "*.mp3" -type f | sort)
do
	ln -fs $file /tmp/$note_number.mp3
	let note_number++
done

