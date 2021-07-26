#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Environment
source ~/.venv/mididings/bin/activate

app="$DIR/build.sh"
chmod +x $app

scene=$1

echo "Loading scene $scene"
$app $scene.py
