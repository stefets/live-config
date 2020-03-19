#!/bin/bash
#
# Create/overwrite a symlink in $target directory for each mp3 file found by find in the $origin directory
#

origin=$1
target=$2

# Optional album theme reserved at note 12
theme=$origin/theme.mp3
ln -fs $theme $target/12.mp3

# Note number from the keyboard, adjustable offset
note_number=13

for file in $(find $origin -name "*.mp3" -type f | sort)
do
	ln -fs $file $target/$note_number.mp3
	let note_number++
done
