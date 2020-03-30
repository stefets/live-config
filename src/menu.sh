#!/bin/bash
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function process()
{ 
    OUT="$(mktemp)"
	case $1 in
		0 )
            $DIR/keyboard.sh
			break
			;;
		1 )	
            echo "_ctrl=fcb1010" > $OUT
            items=(palindrome push)
            while true
            do
                choice=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 20 20 10 0 ${items[0]} 1 ${items[1]})
                $DIR/execute.sh ${items[$choice]}.py $OUT
            done
			break
			;;
        * )
            break
            ;;
	esac
}

# ------------------
controllers=(keyboard fcb1010)
while true
do
	process $(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Controller" 10 15 2 0 ${controllers[0]} 1 ${controllers[1]})
done
