# This is my personal and complete MIDIDINGS configuration
* I use it live and to practice guitar and bass with a FCB1010, Roland PK5A, Alesis Q49, Boss GT10 and POD HD500
* The WIP branch contains the latest updates (semi-stable)
# I use script to dynamically load a list of scenes from DIALOG or the CLI
* HW : Raspberry PI (Ubuntu Mate 16.04) and the munster Edirol SD-90 by Roland Corp. as my BRAIN extension, my MIDI gears of course, a router, a cell phone with Juice SSH)
* SW : MIDIDINGS 2015+rbbec99a, using Python 2.7.12, bash (Optionals : mpg123, aplaymidi, your logic, etc...)
# Call stack
* You can call start.sh, menu.sh or execute.sh as an entry point
* start.sh: it check for flash usb, sound module, etc... If all is correct it call menu.sh 
* menu.sh : use dialog as UI; It's a mini menu (bash script) made for my Juice SSH Android App when I play live. That's it, I use my phone as a terminal.
	* ![UI](https://github.com/stefets/live-config/blob/wip/_ui.jpg "Screen Capture")
	* The menu choice call execute.sh with the filename as parameter (without the .py extension), the filename is a list of scenes.
* execute.sh: Replace two tokens in main.py: __PATCHES__ and __SCENES__ and create complete python script to a file in /tmp/ and run it.
* main.py contain config, classes, methods, pre, post, control, patch to external command and two tokens that I replace with the execute.sh.
# Hint
* Replace patches.py by your own list of patches
# Help
* http://www.nortonmusic.com/midi_cc.html
* http://dsacre.github.io/mididings/doc/
# MIDI HARDWARE USED TO BETTER UNDERSTAND MY PATCHES
* Alesis Q49 configured on midi channel 1
* Roland PK5 configured on midi channel 2
* Line6 POD HD500 configured on midi channel 9
* Behringer FCB1010 with UnO 1.04 configured on MIDI channel 9
	* It control scene navigation and my Pod HD500 directly or through mididings
* WIP
	* BOSS GT-10B to insert
# MY CURRENT MIDI CONNECTION CHAIN
* Q49.out -> in.FCB1010.out -> in.PK5.out -> in1.SD-90.out1 -> in.HD500.out -> in.GT-10B.out -> free
*                                 PK5.thru (free)
*
* Known bugs : The PODHD500 is unable to merge if placed immediatly after the PK5
