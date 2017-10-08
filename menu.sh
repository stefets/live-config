#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main="main.py"
target=$(mktemp)

function run()
{ 
	sed -e "/__SCENES__/r $1.py" -e "/__SCENES__/d" $main > $target
	clear
    python $target
}


while true
do
	
	value=$(dialog --begin 0 0 --no-shadow --stdout --menu "Configuration" 15 20 5 1 push 2 rush_cover 3 bass_cover 4 originales 5 shutdown)
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
			run bass_cover
            continue
            ;;
		4 )
			run originales
            continue
            ;;
		5 )
		    sudo shutdown -h now
			break
			;;
        * )
            break
            ;;
	esac
done
