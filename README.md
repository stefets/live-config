# Script to dynamically load a list of scenes from DIALOG or the CLI
* The WIP branch contains the latest updates (semi-stable)
* Minimal hardware : A computer and a midi device.
* My hardware : Raspberry PI (Ubuntu Mate 16.04) and the munster Edirol SD-90 by Roland Corp. as my BRAIN extension, my MIDI gears of course, a router, a cell phone with Juice SSH)
* Software : MIDIDINGS or nothing, bash (Optionals : mpg123, aplaymidi, your logic, etc...)
# Call stack
* You can call start.sh, menu.sh or execute.sh as an entry point
* start.sh: it check for flash usb, sound module, etc... If all is correct it call menu.sh 
* menu.sh : use dialog as UI; It's a mini menu (bash script) made for my Juice SSH Android App when I play live. That's it, I use my phone as a terminal.
	* The menu choice call execute.sh with the filename as parameter (without the .py extension), the filename is a list of scenes.
* execute.sh: Replace two tokens in main.py: __PATCHES__ and __SCENES__ and create complete python script to a file in /tmp/ and run it.
* main.py contain config, classes, methods, pre, post, control, patch to external command and two tokens that I replace with the execute.sh.
# Hint
* Replace patches.py by your own list of patches
# Help
* http://www.nortonmusic.com/midi_cc.html
* http://dsacre.github.io/mididings/doc/

