#!/bin/bash

# Create the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Hack for the ../run symlink
cd $DIR

main="main.py"
target=$DIR/static.py
scenes=$1
ctrl="$2"

# Replace __TOKEN__ in main.py
sed \
    -e "/__FUNCTIONS__/r functions.py" \
    -e "/__FILTERS__/r filters.py" \
    -e "/__CONTROL__/r control.py" \
    -e "/__SOUNDMODULE__/r soundmodule.py" \
	-e "/__HD500__/r hd500.py" \
	-e "/__GT10B__/r gt10b.py" \
	-e "/__PATCHES__/r patches.py" \
    -e "/__SCENES__/r $scenes" \
    -e "/__CONTROLLER__/r $ctrl" \
	-e "/__FUNCTIONS__/d" \
	-e "/__FILTERS__/d" \
	-e "/__CONTROL__/d" \
	-e "/__SOUNDMODULE__/d" \
	-e "/__HD500__/d" \
	-e "/__GT10B__/d" \
	-e "/__PATCHES__/d" \
	-e "/__SCENES__/d" \
	-e "/__CONTROLLER__/d" \
	$main > $target

# tmp version for debug purpose
cp $target /tmp/output.py

# Start the mididings script
python $target
