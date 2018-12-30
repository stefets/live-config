#!/bin/bash

# Create the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main="main.py"
target=$(mktemp)
scenes=$1
controller=$2

# Replace __TOKEN__ in main.py
sed \
    -e "/__FUNCTIONS__/r functions.py" \
    -e "/__FILTERS__/r filters.py" \
    -e "/__CONTROL__/r control.py" \
    -e "/__SOUNDMODULE__/r soundmodule.py" \
	-e "/__HD500__/r hd500.py" \
	-e "/__PATCHES__/r patches.py" \
    -e "/__SCENES__/r $scenes" \
	-e "/__FUNCTIONS__/d" \
	-e "/__FILTERS__/d" \
	-e "/__CONTROL__/d" \
	-e "/__SOUNDMODULE__/d" \
	-e "/__HD500__/d" \
	-e "/__PATCHES__/d" \
	-e "/__SCENES__/d" \
	$main > $target

clear
# Start the mididings script
python $target
#rm $target
