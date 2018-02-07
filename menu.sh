#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main="main.py"
target=$(mktemp)

function run()
{ 
	/bin/bash $DIR/execute.sh $1
}

while true
do
	
	value=$(dialog --begin 0 0 --no-shadow --stdout --menu "Configuration" 15 20 7 1 push 2 rush_cover 3 bass_cover 4 originales 5 timeline 6 duo 7 shutdown)
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
			run timeline
            continue
            ;;
		6 )
			run duo
            continue
            ;;
		7 )
		    sudo shutdown -h now &
			break
			;;
        * )
            break
            ;;
	esac
done
