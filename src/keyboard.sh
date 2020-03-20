#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT="$(mktemp)"

# Hack
echo "_ctrl=keyboard" > $OUT

$DIR/execute.sh keyboard.py $OUT

exit 0
