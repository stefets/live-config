#!/bin/bash

# Build the final mididings configuration file and execute it.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

template="main.py"
output="live-config.py"
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

# Replace __TOKEN__ for the input and output ports - thanks to alsalist
ports=$(alsalist)
sed -i \
    -e "s/__SD-90 Part A__/$(echo "$ports" | grep 'SD-90 Part A'  | awk '{print $1}')/" \
    -e "s/__SD-90 Part B__/$(echo "$ports" | grep 'SD-90 Part B'  | awk '{print $1}')/" \
    -e "s/__SD-90 MIDI 1__/$(echo "$ports" | grep 'SD-90 MIDI 1'  | awk '{print $1}')/" \
    -e "s/__SD-90 MIDI 2__/$(echo "$ports" | grep 'SD-90 MIDI 2'  | awk '{print $1}')/" \
    -e "s/__UM-2 MIDI 1__/$(echo "$ports"  | grep 'UM-2 MIDI 1'   | awk '{print $1}')/" \
    -e "s/__UM-2 MIDI 2__/$(echo "$ports"  | grep 'UM-2 MIDI 2'   | awk '{print $1}')/" \
    -e "s/__GT-10B MIDI 1__/$(echo "$ports"| grep 'GT-10B MIDI 1' | awk '{print $1}')/" \
    -e "s/__Q49 MIDI 1__/$(echo "$ports"   | grep 'Q49 MIDI 1'    | awk '{print $1}')/" \
    -e "s/__CME M-KEY MIDI 1__/$(echo "$ports" | grep 'CME M-KEY MIDI 1' | awk '{print $1}')/" \
    -e "s/__MPK249 MIDI 1__/$(echo "$ports" | grep 'MPK249 MIDI 1' | awk '{print $1}')/" \
    -e "s/__MPK249 MIDI 2__/$(echo "$ports" | grep 'MPK249 MIDI 2' | awk '{print $1}')/" \
    -e "s/__MPK249 MIDI 3__/$(echo "$ports" | grep 'MPK249 MIDI 3' | awk '{print $1}')/" \
    -e "s/__MPK249 MIDI 4__/$(echo "$ports" | grep 'MPK249 MIDI 4' | awk '{print $1}')/" \
    $output

# Start the mididings script
mididings -f $output
