#!/bin/bash

# Build the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

template="main.py"
output="render.py"
sceneFileName="./scenes/$1"
if [ ! -f "$sceneFileName" ]; then
   echo "Scene $1 invalide"
   find ./scenes -type f
   exit 1
fi

# Merge devices
devices=$(mktemp)
cat $DIR/devices/*.py > $devices

# Replace __TOKEN__ in template file
sed \
    -e "/__FUNCTIONS__/r functions.py" \
    -e "/__FILTERS__/r filters.py" \
    -e "/__CONTROL__/r control.py" \
	-e "/__PATCHES__/r patches.py" \
    -e "/__DEVICES__/r $devices" \
    -e "/__SCENES__/r $sceneFileName" \
	-e "/__FUNCTIONS__/d" \
	-e "/__FILTERS__/d" \
	-e "/__CONTROL__/d" \
	-e "/__DEVICES__/d" \
	-e "/__PATCHES__/d" \
	-e "/__SCENES__/d" \
	$template > $output

# Start the mididings script
mididings -f $output
