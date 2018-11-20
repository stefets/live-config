#!/bin/bash

#
# Create/overwrite a symlink in /tmp for each mp3 file found by find
#
counter=0
for file in $(find $PWD -name "*.mp3" -type f)
do
	ln -fs $file /tmp/$counter.mp3
	let counter++
done
