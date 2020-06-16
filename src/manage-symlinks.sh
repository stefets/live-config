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
for file in $(find $origin -type f ! -iname theme.mp3 -iname "*.mp3" | sort)
do
    filename="${file##*/}"
	ln -fs $file $filename
done

# Create theme symlink for note zero
theme=$(find /mnt/flash/music/soundlib -type f -iname main-theme.mp3)
if [ ! -z $theme ] 
then
    ln -fs $theme 0.mp3
fi

ls *.mp3 > playlist
