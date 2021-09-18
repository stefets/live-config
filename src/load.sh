#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Environment
source ~/.venv/mididings/bin/activate

app="$DIR/build.sh"
chmod +x $app

scene=$1
if [ -z "$scene" ]; then
    scene="default"
fi

echo "Loading scene $scene"
$app $scene.py
