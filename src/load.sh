#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

app="$DIR/build_script.sh"
chmod +x $app

scene=$1
if [ -z "$scene" ]; then
    scene="default"
fi

echo "Loading context $scene"
$app $scene.py
