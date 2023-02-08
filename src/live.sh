#!/bin/bash

# Setup a configuration file for MIDIDINGS and exec_mididings it, that's it.

function configure() {

    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    template="template.py"
    script="script.py"
    
    configure_scene $1
    configure_script
    configure_alsa
    configure_mpg123
}

function configure_scene() {
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

function configure_script() {

    # Merge patches
    patches=$(mktemp)
    cat $DIR/patches/*.py > $patches

    # Merge modules
    modules=$(mktemp)
    cat $DIR/modules/*.py > $modules

    # Replace __TOKEN__ from various files through $template file to $script
    sed \
        -e "/__MODULES_/r $modules" -e "/__PATCHES__/r $patches" -e "/__SCENES__/r $scenes" \
        -e "/__MODULES_/d" -e "/__PATCHES__/d" -e "/__SCENES__/d" \
        $template > $script

    # Replace __TOKEN__ for the input/output ports with alsalist
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
        $script
}

function configure_alsa() {
    # Patch asoundrc.conf, via tmp and copy result to  ~/.asoundrc
    conf=$(mktemp)
    cp $DIR/asoundrc.conf $conf
    cards=$(arecord -l |egrep "carte|card" | awk '{print $2 $3}')
    sed -i \
        -e "s/__SD90__/$(echo  "$cards" | grep SD90  | cut -d: -f1)/" \
        -e "s/__GT10B__/$(echo "$cards" | grep GT10B | cut -d: -f1)/" \
        -e "s/__U192k__/$(echo "$cards" | grep U192k | cut -d: -f1)/" \
        $conf

    cp $conf ~/.asoundrc
}

function configure_mpg123() {
    # Don't know what process bust my link but enough is enough
    sudo ln -sf /usr/local/lib/libmpg123.so.0 /lib/aarch64-linux-gnu/libmpg123.so.0
    sudo ln -sf /usr/local/lib/libout123.so.0 /lib/aarch64-linux-gnu/libout123.so.0
    sudo ln -sf /usr/local/lib/libsyn123.so.0 /lib/aarch64-linux-gnu/libsyn123.so.0
}

function exec_mididings() {
    mididings -f $script
}

function main() {
    configure $1
    exec_mididings
}

main $1
