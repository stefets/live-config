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
	
	value=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 15 20 8 1 push 2 rush_cover 3 bass_cover 4 originales 5 timeline 6 solo 7 styx 8 shutdown)
	#value=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 15 20 8 push - rush_cover - solo - styx -)
    #run $value.py
    #continue
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
			run solo.py
            continue
            ;;
		7 )
			run styx.py
            continue
            ;;
		8 )
		    sudo poweroff &
			break
			;;
        * )
            break
            ;;
	esac
done
