#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT="$(mktemp)"

# Hack
echo "_ctrl=fcb1010" > $OUT

$DIR/execute.sh $1 $OUT

exit 0
