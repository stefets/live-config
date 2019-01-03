#!/bin/bash

#
# Main menu
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
menus=(bass_cover midi rush styx system tabarnac timeline demon rush_cover)

function process()
{ 
	ctrl=$1
	choice=$2

	case $ctrl in
		0 )

			target="$soundlib/${menus[$choice]}"
			if [ ! -d $target ]; then
				clear
				read -n 1 -s -r -p "$target does not exists - press any key to continue"
			else
				/bin/bash $DIR/mklink.sh $target
				/bin/bash $DIR/execute.sh mp3_piano_player.py
			fi
			break
			;;
		1 )	
			/bin/bash $DIR/execute.sh ${menus[$choice]}.py
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
	
		choice=$(dialog --begin 0 0 --no-shadow --output-fd 1 --menu "Configuration" 20 20 9 0 ${menus[0]} 1 ${menus[1]} 2 ${menus[2]} 3 ${menus[3]} 4 ${menus[4]} 5 ${menus[5]} 6 ${menus[6]} 7 ${menus[7]} 8 ${menus[8]})

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
