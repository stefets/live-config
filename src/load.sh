#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Environment
source $DIR/../.venv/bin/activate

#Vars
audio="/media/soundlib"
app="$DIR/build.sh"

rm -f /tmp/soundlib
ln -sf $audio /tmp/soundlib

chmod +x $app
$app $1.py
