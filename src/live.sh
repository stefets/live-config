#!/bin/bash

# Setup a configuration file for MIDIDINGS and run it, that's it.

function setup() {
    setup_base
    setup_scene $1
    setup_script
}

function setup_base() {
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    # Template
    template="template.py"

    # Modules
    control="mod_control.py"
    logic="mod_logic.py"
    filters="mod_filters.py"
    patches="mod_patches.py"

    # Target script
    script="script.py"
}

function setup_scene() {
    # Scene from param or default
    scene=$1
    if [ -z "$scene" ]; then
        scene="default"
    fi

    scenes="./scenes/$scene.py"
    if [ ! -f "$scenes" ]; then
        echo -e "Scene $scene not found\nAvailable scenes"
        find ./scenes -type f
        exit 1
    fi
}

function setup_script() {

    # Create a devices file
    patches=$(mktemp)
    cat $DIR/patches/*.py > $patches

    modules=$(mktemp)
    cat $DIR/modules/*.py > $modules

    # Replace __TOKEN__ from various files through $template file to $script
    sed \
        -e "/__MODULES_/r $modules" -e "/__PATCHES__/r $patches" -e "/__SCENES__/r $scenes" \
        -e "/__MODULES_/d" -e "/__PATCHES__/d" -e "/__SCENES__/d" \
        $template > $script

    # Replace __TOKEN__ for the input/output ports with alsalist
    # https://github.com/danieloneill/alsalist
    ports=$(alsalist)
    sed -i \
        -e "s/__SD-90 Part A__/$(echo "$ports"  | grep 'SD-90 Part A'  | awk '{print $1}')/" \
        -e "s/__SD-90 Part B__/$(echo "$ports"  | grep 'SD-90 Part B'  | awk '{print $1}')/" \
        -e "s/__SD-90 MIDI 1__/$(echo "$ports"  | grep 'SD-90 MIDI 1'  | awk '{print $1}')/" \
        -e "s/__SD-90 MIDI 2__/$(echo "$ports"  | grep 'SD-90 MIDI 2'  | awk '{print $1}')/" \
        -e "s/__UM-2 MIDI 1__/$(echo "$ports"   | grep 'UM-2 MIDI 1'   | awk '{print $1}')/" \
        -e "s/__UM-2 MIDI 2__/$(echo "$ports"   | grep 'UM-2 MIDI 2'   | awk '{print $1}')/" \
        -e "s/__GT-10B MIDI 1__/$(echo "$ports" | grep 'GT-10B MIDI 1' | awk '{print $1}')/" \
        -e "s/__Q49 MIDI 1__/$(echo "$ports"    | grep 'Q49 MIDI 1'    | awk '{print $1}')/" \
        -e "s/__MPK249 MIDI 1__/$(echo "$ports" | grep 'MPK249 MIDI 1' | awk '{print $1}')/" \
        -e "s/__MPK249 MIDI 2__/$(echo "$ports" | grep 'MPK249 MIDI 2' | awk '{print $1}')/" \
        -e "s/__MPK249 MIDI 3__/$(echo "$ports" | grep 'MPK249 MIDI 3' | awk '{print $1}')/" \
        -e "s/__MPK249 MIDI 4__/$(echo "$ports" | grep 'MPK249 MIDI 4' | awk '{print $1}')/" \
        -e "s/__MIDI Mix MIDI 1__/$(echo "$ports" | grep 'MIDI Mix MIDI 1' | awk '{print $1}')/" \
        -e "s/__UMC204HD 192k MIDI 1__/$(echo "$ports" | grep 'UMC204HD 192k MIDI 1' | awk '{print $1}')/" \
        $script
}

function run() {
    mididings -f $script
}

# ----
# Main
setup $1
run

