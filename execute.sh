#!/bin/bash

# Create the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main="main.py"
target=$(mktemp)
scenes=$1

# Replace __TOKEN__ in main.py
sed -e "/__PATCHES__/r patches.py" -e "/__PATCHES__/d" \
    -e "/__SCENES__/r $scenes" -e "/__SCENES__/d" \
	$main > $target

clear
# Start the mididings script
python $target
#rm $target
