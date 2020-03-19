#!/bin/bash

# Create the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

template="main.py"
target="render.py"
sceneFileName="./scenes/$1"
ctrl="$2"

# Replace __TOKEN__ in template file
sed \
    -e "/__FUNCTIONS__/r functions.py" \
    -e "/__FILTERS__/r filters.py" \
    -e "/__CONTROL__/r control.py" \
    -e "/__SD90__/r ./hardware/sd90.py" \
	-e "/__HD500__/r ./hardware/hd500.py" \
	-e "/__GT10B__/r ./hardware/gt10b.py" \
	-e "/__PATCHES__/r patches.py" \
    -e "/__SCENES__/r $sceneFileName" \
    -e "/__CONTROLLER__/r $ctrl" \
	-e "/__FUNCTIONS__/d" \
	-e "/__FILTERS__/d" \
	-e "/__CONTROL__/d" \
	-e "/__SD90__/d" \
	-e "/__HD500__/d" \
	-e "/__GT10B__/d" \
	-e "/__PATCHES__/d" \
	-e "/__SCENES__/d" \
	-e "/__CONTROLLER__/d" \
	$template > $target

# Start the mididings script
python $target
