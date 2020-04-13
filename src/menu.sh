#!/bin/bash
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

controllers=(keyboard fcb1010)

function process()
{ 
    OUT="$(mktemp)"
	case $1 in
		0 )
            echo "_ctrl=keyboard" > $OUT
            $DIR/execute.sh keyboard.py $OUT
            return
			;;
		1 )	
            echo "_ctrl=fcb1010" > $OUT
            items=(palindrome push)
            while true
            do
                trap ' ' SIGINT
                choice=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 20 20 10 0 ${items[0]} 1 ${items[1]})
                if [ -z "$choice" ]; then return; fi
                trap - SIGINT
                $DIR/execute.sh ${items[$choice]}.py $OUT
                continue
            done
            return
			;;
        * )
            break
            ;;
	esac
}

# ------------------
while true
do
	process $(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Controller" 10 15 2 0 ${controllers[0]} 1 ${controllers[1]})
    continue
done
