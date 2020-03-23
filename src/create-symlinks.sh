#!/bin/bash
#
# Create a symlink in $target directory for each mp3 file found by find in the $origin directory
#

# Params
origin=$1
target=$2

cd $target

# Build symlinks in $target
rm *.mp3
for file in $(find $origin -name "*.mp3" -type f | sort)
do
    filename="${file##*/}"
	ln -fs $file $filename
done
ls *.mp3 > playlist
