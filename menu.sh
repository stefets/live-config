 #!/bin/bash

#
# Main menu, depend on start.sh
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# GENERAL PARAMETERS
soundlib=/tmp/soundlib	# symlink set in start.sh

# CONTROLLERS
# Keyboard to control mpg123 in remote mode from a single mididings scene in mp3_piano_player.py
# FCB1010 to control mididings normally
controllers=(KeyboardMPG123 FCB1010)

# MENU
# options must match name.py if controller is fcb1010 or folder name if controller is keyboard
#items=($(find -L /tmp/soundlib ! -path /tmp/soundlib -type d -printf '%f\n'))
items=(palindrome bass_cover midi push styx system tabarnac timeline demon rush_cover)

function process()
{ 
	ctrl=$1
	choice=$2

	case $ctrl in
		0 )

			#target="${items[$choice]}"
			target="$soundlib/${items[$choice]}"
			if [ ! -d $target ]; then
				clear
				read -n 1 -s -r -p "$target does not exists - press any key to create and continue"
                mkdir -p $target
			fi
			/bin/bash $DIR/mklink.sh $target
			/bin/bash $DIR/execute.sh mp3_piano_player.py
			break
			;;
		1 )	
			/bin/bash $DIR/execute.sh ${items[$choice]}.py
			break
			;;
        * )
            break
            ;;
	esac
}

function main()
{

	ctrl=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Controller" 10 15 2 0 ${controllers[0]} 1 ${controllers[1]})
	if [ -z "${ctrl}" ]; then
		break
	fi
		
	while true
	do
	
		choice=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 20 20 10 0 ${items[0]} 1 ${items[1]} 2 ${items[2]} 3 ${items[3]} 4 ${items[4]} 5 ${items[5]} 6 ${items[6]} 7 ${items[7]} 8 ${items[8]} 9 ${items[9]})

		if [ -z "${choice}" ]; then
 			break
		fi

		# Call mididings here
		process $ctrl $choice

	done

}

# Let's start here 
while true
do
	main
done
