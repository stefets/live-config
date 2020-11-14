#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Vars
flash="/mnt/flash"
audio="$flash/music/soundlib"
app="$DIR/execute.sh"

ln -sf $audio /tmp/soundlib

chmod +x $app
$app keyboard.py
