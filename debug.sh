#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main="main.py"
target=$(mktemp)

sed -e "/__SCENES__/r $1.py" -e "/__SCENES__/d" $main > $target
clear
python $target
