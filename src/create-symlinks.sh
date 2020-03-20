#!/bin/bash
#
# Create/overwrite a symlink in $target directory for each mp3 file found by find in the $origin directory
#
origin=$1
target=$2
rm $target/*.mp3

# Application theme reserved at note 12
theme="$target/soundlib/theme.mp3"
if [ -e $theme ]
then
    ln -fs $theme $target/12.mp3
fi

# Note number from the keyboard, adjustable offset
note_number=13

for file in $(find $origin -name "*.mp3" -type f | sort)
do
	ln -fs $file $target/$note_number.mp3
	let note_number++
done
