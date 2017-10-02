#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


#{}{}{}
function run()
{ 
	sed "s/__SCENES__/$(cat $1.py)/" main.py > live.py
    python live.py
}

while true
do

	echo "MIDIDINGS MENU ($LOGNAME),"
	echo ""
	echo "1) Push"
	echo "2) Rush cover"
	echo "3) Basse cover"
	echo "4) Originales"
    echo "-----------------"
	echo "q) BASH"
	echo ""

	read -rs -n1 -ep  "> " value
	if [ -z $value ]; then continue; fi

	case $value in
		1 )
			run push
            continue
            ;;
		2 )
			run rush_cover
            continue
            ;;
		3 )
			run bass
            continue
            ;;
		4 )
			run originales
            continue
            ;;
		[qQ] )
            break
            ;;
        * )
            continue
            ;;
	esac
done
