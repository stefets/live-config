#!/bin/bash

#
# Main menu
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function run()
{ 
	filename=$1
	/bin/bash $DIR/execute.sh $filename
}

while true
do
	
	value=$(dialog --begin 0 0 --no-shadow --stdout --menu "Configuration" 15 20 7 1 push 2 rush_cover 3 bass_cover 4 originales 5 timeline 6 duo 7 shutdown)
	case $value in
		1 )
			run push.py
            continue
            ;;
		2 )
			run rush_cover.py
            continue
            ;;
		3 )
			run bass_cover.py
            continue
            ;;
		4 )
			run originales.py
            continue
            ;;
		5 )
			run timeline.py
            continue
            ;;
		6 )
			run duo.py
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
