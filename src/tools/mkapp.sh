#!/bin/bash

# Creates a mididings script from a skeleton
# Input and output ports are tokenized with sed

# Validate script name
filename="$1"
if [[ -z "$filename" || "$filename" = "skeleton" ]]; then
    echo "usage : ./mkapp.sh SCRIPTNAME"
    exit 1
fi

source="skeleton.py"
target="$filename.py"

cp $source $target

ports=$(alsalist)
sed -i \
    -e "s/__SD-90 Part A__/$(echo "$ports"  | grep 'SD-90 Part A'  | awk '{print $1}')/" \
    -e "s/__SD-90 Part B__/$(echo "$ports"  | grep 'SD-90 Part B'  | awk '{print $1}')/" \
    -e "s/__SD-90 MIDI 1__/$(echo "$ports"  | grep 'SD-90 MIDI 1'  | awk '{print $1}')/" \
    -e "s/__SD-90 MIDI 2__/$(echo "$ports"  | grep 'SD-90 MIDI 2'  | awk '{print $1}')/" \
    -e "s/__GT-10B MIDI 1__/$(echo "$ports" | grep 'GT-10B MIDI 1' | awk '{print $1}')/" \
    -e "s/__Q49 MIDI 1__/$(echo "$ports"    | grep 'Q49 MIDI 1'    | awk '{print $1}')/" \
    -e "s/__MPK249 Port A__/$(echo "$ports" | grep 'MPK249 Port A' | awk '{print $1}')/" \
    -e "s/__MPK249 Port B__/$(echo "$ports" | grep 'MPK249 Port B' | awk '{print $1}')/" \
    -e "s/__MPK249 MIDI__/$(echo "$ports" | grep 'MPK249 MIDI' | awk '{print $1}')/" \
    -e "s/__MPK249 Remote__/$(echo "$ports" | grep 'MPK249 Remote' | awk '{print $1}')/" \
    -e "s/__MIDI Mix MIDI 1__/$(echo "$ports" | grep 'MIDI Mix MIDI 1' | awk '{print $1}')/" \
    -e "s/__UMC204HD 192k MIDI 1__/$(echo "$ports" | grep 'UMC204HD 192k MIDI 1' | awk '{print $1}')/" \
    $target