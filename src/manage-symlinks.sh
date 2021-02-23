#!/bin/bash
#
# Create a symlink in $target directory for each mp3 file found by find in the $origin directory
#

# Params
origin=$1
target=$2

cd $target

# Build symlinks in $target
rm -f *.mp3 # Wipe out current mp3 symlinks
for file in $(find -L $origin -type f -iname "*.mp3" | sort)
do
    filename="${file##*/}"
	ln -fs $file $filename
done

ls *.mp3 > playlist
