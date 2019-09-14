#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------
# Many thanks to the programmer Dominic Sacre for that masterpiece
# http://das.nasophon.de/mididings/
# https://github.com/dsacre
#-----------------------------------------------------------------------------------------------------------
# My personal mididings script
# Stephane Gagnon
#-----------------------------------------------------------------------------------------------------------

import os
import glob
from subprocess import Popen, PIPE
from threading import Timer
from time import sleep
from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.osc import *

#useless for a dynamic script but usefull for a static scipt
#from mididings.extra.inotify import *

config(

	# Defaults
    #initial_scene = 1,
    #backend = 'alsa',
    #client_name = 'mididings',

    out_ports = [ 
        ('SD90_PARTA', '20:0'),				# Edirol SD-90 PART A 		(Port number 1)
        ('SD90_PARTB', '20:1'),				# Edirol SD-90 PART B 		(Port number 2)
        ('SD90_MIDI_OUT_1', '20:2',), 		# Edirol SD-90 MIDI OUT 1 	(Port number 3)
        ('SD90_MIDI_OUT_2', '20:3',), 		# Edirol SD-90 MIDI OUT 2 	(Port number 4)
		# Clones
        ('HD500', '20:2',), 				# MOVABLE
        # HD500 midi out to gt10b midi , if I output to gt10b, it goes thru pod anyway
        ('GT10B', '20:2',), 				# MOVABLE
	],			

    in_ports = [ 
        ('Q49_MIDI_IN_1', '24:0',), 	# Alesis Q49 in USB MODE
        ('SD90_MIDI_IN_1','20:2',),		# Edirol SD-90 MIDI IN 1
        ('SD90_MIDI_IN_2','20:3',) 		# Edirol SD-90 MIDI IN 2
	],

)

hook(

    #MemorizeScene('memorize-scene.txt'),

    #AutoRestart(), #AutoRestart works with mididings.extra.inotify

	#OSCInterface(port=56418, notify_ports=[56419,56420]),
	#OSCInterface(port=56418, notify_ports=56419),
	#OSCInterface(),
)

#-----------------------------------------------------------------------------------------------------------
# Functions section 
# functions.py
#--------------------------------------------------------------------
# Function and classes called by scenes
#--------------------------------------------------------------------
#
# This class control mpg123 in remote mode with a keyboard (or any other midi devices of your choice)
# It's an embedded clone of the 'keyboard song trigger' of the Quebec TV Show 'Tout le monde en parle'
#
class MPG123():

    # CTOR
    def __init__(self):


        self.mpg123 = None

        # Expose songs
        # TODO faire mieux
        songs = [ "/tmp/soundlib/system/tlmep.mp3" ]

        # Add songs after the mpg123 commands
        #for song in songs:
        #    self.commands.append('l ' + song)

    # On call...
    def __call__(self, ev):
        self.event2remote(ev)

    def event2remote(self, ev):

        if self.mpg123 == None:
            self.create()

        if ev.type == NOTEON:
            self.note2remote(ev)
        elif ev.type == CTRL:
            self.cc2remote(ev)
                
	# Start mpg123
    def create(self):
        print "Create MPG123 instance"
        # TODO TOKEN REPLACE __HW__
        self.mpg123=Popen(['mpg123', '-a', 'hw:1,0', '--quiet', '--remote'], stdin=PIPE)
        self.rcall('silence') # Shut up mpg132 :)

    # METHODS
    # Write a command to the mpg123 process
    def rcall(self, cmd):
        self.mpg123.stdin.write(cmd + '\n')

    # Note to remote command
    def note2remote(self, ev):

        if ev.data1 > 11:
            self.rcall('l /tmp/' + str(ev.data1) + '.mp3')
        # Reserved 0 to 11
        elif ev.data1 == 0:
            switch_scene(current_scene()-1)
        elif ev.data1 == 1:
            switch_subscene(current_subscene()-1)
        elif ev.data1 == 2:
            self.rcall('p')            
        elif ev.data1 == 3:
            switch_subscene(current_subscene()+1)
        elif ev.data1 == 4:
            switch_scene(current_scene()+1)
        elif ev.data1 == 11:
            Popen(['ls', '-l', '/tmp/*.mp3'])
        else:
            self.rcall('l /tmp/' + str(ev.data1) + '.mp3')
#        if ev.data1 <= len(self.commands):
#           # Reserved range
#           self.rcall(self.commands[ev.data1])
#       else:
#           # Try to load the mp3
#           self.rcall('l /tmp/' + str(ev.data1) + '.mp3')

        ev.data2 = 0

        return ev

    # CC to remote command
    def cc2remote(self, ev):
        # MIDI volume to mpg123 volume
        if ev.data1==7 and ev.data2 <= 100:
            self.rcall('v ' + str(ev.data2))
        # MIDI modulation to mpg123 pitch resolution / SUCK on the RPI - can pitch 3% before hardware limitation is reached
        #elif ev.data1==1 and ev.data2 <= 100:
        #    self.rcall('pitch ' + str(float(ev.data2)/100))

# ----------------------------------------------------------------------------------------------------
#
# This class remove duplicate midi message by taking care of an offset logic
# NOT STABLE SUSPECT OVERFLOW 
# WIP TODO
class RemoveDuplicates:
    def __init__(self, _wait=0):
        self.wait = _wait
        self.prev_ev = None
        self.prev_time = 0

    def __call__(self, ev): 
        if ev.type == NOTEOFF:
            sleep(self.wait)
            return ev
        now = engine.time()
        offset=now-self.prev_time
        if offset >= 0.035:
            #if ev.type == NOTEON:
            #    print "+ " + str(offset)
            r = ev 
        else:
            #if ev.type == NOTEON:
            #    print "- " + str(offset)
            r = None
        self.prev_ev = ev
        self.prev_time = now
        return r

#--------------------------------------------------------------------
# Generate a chord prototype test
# Better to use the mididings builtin object Hamonize
def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev
#--------------------------------------------------------------------

# WIP: Glissando
def gliss_function(note, note_max, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    note += 1
    if note < note_max:
        Timer(.01, lambda: gliss_function(note, note_max, port, chan, vel)).start()

def gliss_exec(e):
    gliss_function(120, 168, e.port, e.channel, 100)

# WIP : Arpeggiator
def arpeggiator_function(current, max,note, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    current += 1
    if current < max:
        Timer(.15, lambda: arpeggiator_function(current, max, note,  port, chan, vel)).start()

def arpeggiator_exec(e):
    arpeggiator_function(0,16, 50,  e.port, e.channel, 100)

#-------------------------------------------------------------------------------------------

# Navigate through secenes and subscenes
def NavigateToScene(ev):
    # MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    # With that function, you can wrap trough Scenes AND SubScenes
    # That function assume that the first SceneNumber is 1
	#TODO field, values = dict(scenes()).items()[0]
    if ev.ctrl == 20:
        nb_scenes = len(scenes())    
        cs=current_scene()
		# Scene backward
        if ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
		# Scene forward and wrap
        elif ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs+1)
            else:
                switch_scene(1)
		# SubScene backward
        elif ev.value == 3:
            css=current_subscene()
            if css > 1:
                switch_subscene(css-1)
		# SubScene forward and wrap
        elif ev.value == 4:
            css=current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css+1)
            else:
                switch_subscene(1)

# Stop any audio processing, managed by a simple bash script
def AllAudioOff(ev):
    return "/bin/bash ./kill.sh"

# Audio and midi players suitable for my SD-90
def play_file(filename):
    fname, fext = os.path.splitext(filename)
    path=" /tmp/soundlib/"
    if fext == ".mp3":
        command="mpg123 -q"
    elif fext == ".mid":
        command="aplaymidi -p 20:1"

    return command + path + filename

# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64)*direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value*direction)


#---------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Filters Section
# filters.py
#-----------------------------------------------------------------------------------------------------------
# ALLOWED FILTERS : Available for patches, meaning, allow only for instance
q49=ChannelFilter(1)    # Filter by hardware / channel
pk5=ChannelFilter(2)    # Filter by hardware & channel
fcb=ChannelFilter(9)
hd500=ChannelFilter(9)
gt10b=ChannelFilter(16)

# By name
ch1=ChannelFilter(1)
ch2=ChannelFilter(2)
ch3=ChannelFilter(3)
ch4=ChannelFilter(4)
ch5=ChannelFilter(5)
ch6=ChannelFilter(6)
ch7=ChannelFilter(7)
ch8=ChannelFilter(8)
ch9=ChannelFilter(9)
ch10=ChannelFilter(10)
ch11=ChannelFilter(11)
ch12=ChannelFilter(12)
ch13=ChannelFilter(13)
ch14=ChannelFilter(14)
ch15=ChannelFilter(15)
ch16=ChannelFilter(16)

noch1=~ChannelFilter(1)
noch2=~ChannelFilter(2)
noch3=~ChannelFilter(3)
noch4=~ChannelFilter(4)
noch5=~ChannelFilter(5)
noch6=~ChannelFilter(6)
noch7=~ChannelFilter(7)
noch8=~ChannelFilter(8)
noch9=~ChannelFilter(9)
noch10=~ChannelFilter(10)
noch11=~ChannelFilter(11)
noch12=~ChannelFilter(12)
noch13=~ChannelFilter(13)
noch14=~ChannelFilter(14)
noch15=~ChannelFilter(15)
noch16=~ChannelFilter(16)

# Control Filter Channel (cf)
cf=~ChannelFilter(9)


#-----------------------------------------------------------------------------------------------------------
# Control section
# control.py
#-----------------------------------------------------------------------------------------------------------
# CONTROL SECTION
#-----------------------------------------------------------------------------------------------------------
q49_channel=1
pk5_channel=2
fcb_channel=9
pod_channel=9
gt10b_channel=16


# This control have the same behavior than the NavigateToScene python function above
# EXCEPT that there is NO wrap parameter for SceneSwitch
# The NavigateToScene CAN wrap through Scenes
#_control=(ChannelFilter(9) >> Filter(CTRL) >>
#	(
#		(CtrlFilter(20) >> CtrlValueFilter(1) >> SceneSwitch(offset=-1)) //
#		(CtrlFilter(20) >> CtrlValueFilter(2) >> SceneSwitch(offset=1))  //
#		(CtrlFilter(20) >> CtrlValueFilter(3) >> SubSceneSwitch(offset=1, wrap=True))
#	))


# Reset all
reset=(
	System(AllAudioOff) // Pass() // 
	SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7') // Pass()
)


# FCB1010 UNO as controller
#fcb1010=(ChannelFilter(9) >> Filter(CTRL) >> 
#	(
#		(CtrlFilter(20) >> Process(NavigateToScene)) // 
#		(CtrlFilter(22) >> reset)
#	))

# FCB1010 UNO as controller (same as above different syntaxes)
fcb1010=(Filter(CTRL) >> CtrlSplit({
    20: Process(NavigateToScene),
    22: reset,
}))

# KEYBOARD CONTROLLER - WIP
keyboard=(Filter(NOTEON|CTRL) >> Process(MPG123()))

# PK5 as Controller - WIP
_pk5_controller = Pass()

# Shortcut (Play switch)
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)
#-----------------------------------------------------------------------------------------------------------

# TODO (*** not sure until real need ***)
# Multiple controllers , different logic for each of them WIP
#main_controller=ChannelSplit({
    #1: _keyboard_controller,
    #9: _fcb1010_controller,
    #2:_pk5_controller
#})
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Sound module configuration 
#-----------------------------------------------------------------------------------------------------------

# This is the patches specific for the sound modules configuration

#
# EDIROL SD-90
#
# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01=(Ctrl(1, 1,100,0) // Ctrl(1, 1,101,0) // Ctrl(1, 1,6,12) // Ctrl(1, 1,38,0))
PB_A02=(Ctrl(1, 2,100,0) // Ctrl(1, 2,101,0) // Ctrl(1, 2,6,12) // Ctrl(1, 2,38,0))
PB_A03=(Ctrl(1, 3,100,0) // Ctrl(1, 3,101,0) // Ctrl(1, 3,6,12) // Ctrl(1, 3,38,0))
PB_A04=(Ctrl(1, 4,100,0) // Ctrl(1, 4,101,0) // Ctrl(1, 4,6,12) // Ctrl(1, 4,38,0))
PB_A05=(Ctrl(1, 5,100,0) // Ctrl(1, 5,101,0) // Ctrl(1, 5,6,12) // Ctrl(1, 5,38,0))
PB_A06=(Ctrl(1, 6,100,0) // Ctrl(1, 6,101,0) // Ctrl(1, 6,6,12) // Ctrl(1, 6,38,0))
PB_A07=(Ctrl(1, 7,100,0) // Ctrl(1, 7,101,0) // Ctrl(1, 7,6,12) // Ctrl(1, 7,38,0))
PB_A08=(Ctrl(1, 8,100,0) // Ctrl(1, 8,101,0) // Ctrl(1, 8,6,12) // Ctrl(1, 8,38,0))
PB_A09=(Ctrl(1, 9,100,0) // Ctrl(1, 9,101,0) // Ctrl(1, 9,6,12) // Ctrl(1, 9,38,0))
PB_A10=(Ctrl(1,10,100,0) // Ctrl(1,10,101,0) // Ctrl(1,10,6,12) // Ctrl(1,10,38,0))
PB_A11=(Ctrl(1,11,100,0) // Ctrl(1,11,101,0) // Ctrl(1,11,6,12) // Ctrl(1,11,38,0))
PB_A12=(Ctrl(1,12,100,0) // Ctrl(1,12,101,0) // Ctrl(1,12,6,12) // Ctrl(1,12,38,0))
PB_A13=(Ctrl(1,13,100,0) // Ctrl(1,13,101,0) // Ctrl(1,13,6,12) // Ctrl(1,13,38,0))
PB_A14=(Ctrl(1,14,100,0) // Ctrl(1,14,101,0) // Ctrl(1,14,6,12) // Ctrl(1,14,38,0))
PB_A15=(Ctrl(1,15,100,0) // Ctrl(1,15,101,0) // Ctrl(1,15,6,12) // Ctrl(1,15,38,0))
PB_A16=(Ctrl(1,16,100,0) // Ctrl(1,16,101,0) // Ctrl(1,16,6,12) // Ctrl(1,16,38,0))
# SD-90 Part B - All Channel
PB_B01=(Ctrl(2, 1,100,0) // Ctrl(2, 1,101,0) // Ctrl(2, 1,6,12) // Ctrl(2, 1,38,0))
PB_B02=(Ctrl(2, 2,100,0) // Ctrl(2, 2,101,0) // Ctrl(2, 2,6,12) // Ctrl(2, 2,38,0))
PB_B03=(Ctrl(2, 3,100,0) // Ctrl(2, 3,101,0) // Ctrl(2, 3,6,12) // Ctrl(2, 3,38,0))
PB_B04=(Ctrl(2, 4,100,0) // Ctrl(2, 4,101,0) // Ctrl(2, 4,6,12) // Ctrl(2, 4,38,0))
PB_B05=(Ctrl(2, 5,100,0) // Ctrl(2, 5,101,0) // Ctrl(2, 5,6,12) // Ctrl(2, 5,38,0))
PB_B06=(Ctrl(2, 6,100,0) // Ctrl(2, 6,101,0) // Ctrl(2, 6,6,12) // Ctrl(2, 6,38,0))
PB_B07=(Ctrl(2, 7,100,0) // Ctrl(2, 7,101,0) // Ctrl(2, 7,6,12) // Ctrl(2, 7,38,0))
PB_B08=(Ctrl(2, 8,100,0) // Ctrl(2, 8,101,0) // Ctrl(2, 8,6,12) // Ctrl(2, 8,38,0))
PB_B09=(Ctrl(2, 9,100,0) // Ctrl(2, 9,101,0) // Ctrl(2, 9,6,12) // Ctrl(2, 9,38,0))
PB_B10=(Ctrl(2,10,100,0) // Ctrl(2,10,101,0) // Ctrl(2,10,6,12) // Ctrl(2,10,38,0))
PB_B11=(Ctrl(2,11,100,0) // Ctrl(2,11,101,0) // Ctrl(2,11,6,12) // Ctrl(2,11,38,0))
PB_B12=(Ctrl(2,12,100,0) // Ctrl(2,12,101,0) // Ctrl(2,12,6,12) // Ctrl(2,12,38,0))
PB_B13=(Ctrl(2,13,100,0) // Ctrl(2,13,101,0) // Ctrl(2,13,6,12) // Ctrl(2,13,38,0))
PB_B14=(Ctrl(2,14,100,0) // Ctrl(2,14,101,0) // Ctrl(2,14,6,12) // Ctrl(2,14,38,0))
PB_B15=(Ctrl(2,15,100,0) // Ctrl(2,15,101,0) // Ctrl(2,15,6,12) // Ctrl(2,15,38,0))
PB_B16=(Ctrl(2,16,100,0) // Ctrl(2,16,101,0) // Ctrl(2,16,6,12) // Ctrl(2,16,38,0))

InitPitchBend=(
		PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
		PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
		PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
		PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

InitSoundModule=(
	SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7') // 
	InitPitchBend)

#-----------------------------------------------------------------------------------------------------------
# HD500 configuration
# hd500.py
#-----------------------------------------------------------------------------------------------------------
#
# This is the patches specific for a certain device
#
# POD-HD-500
#

hd500_channel=9
hd500_port=3

P01A=Program(hd500_port, channel=hd500_channel, program=1)
P01B=Program(hd500_port, channel=hd500_channel, program=2)
P01C=Program(hd500_port, channel=hd500_channel, program=3)
P01D=Program(hd500_port, channel=hd500_channel, program=4)
P02A=Program(hd500_port, channel=hd500_channel, program=5)
P02B=Program(hd500_port, channel=hd500_channel, program=6)
P02C=Program(hd500_port, channel=hd500_channel, program=7)
P02D=Program(hd500_port, channel=hd500_channel, program=8)
P03A=Program(hd500_port, channel=hd500_channel, program=9)
P03B=Program(hd500_port, channel=hd500_channel, program=10)
P03C=Program(hd500_port, channel=hd500_channel, program=11)
P03D=Program(hd500_port, channel=hd500_channel, program=12)
P04A=Program(hd500_port, channel=hd500_channel, program=13)
P04B=Program(hd500_port, channel=hd500_channel, program=14)
P04C=Program(hd500_port, channel=hd500_channel, program=15)
P04D=Program(hd500_port, channel=hd500_channel, program=16)
P05A=Program(hd500_port, channel=hd500_channel, program=17)
P05B=Program(hd500_port, channel=hd500_channel, program=18)
P05C=Program(hd500_port, channel=hd500_channel, program=19)
P05D=Program(hd500_port, channel=hd500_channel, program=20)
P06A=Program(hd500_port, channel=hd500_channel, program=21)
P06B=Program(hd500_port, channel=hd500_channel, program=22)
P06C=Program(hd500_port, channel=hd500_channel, program=23)
P06D=Program(hd500_port, channel=hd500_channel, program=24)
P07A=Program(hd500_port, channel=hd500_channel, program=25)
P07B=Program(hd500_port, channel=hd500_channel, program=26)
P07C=Program(hd500_port, channel=hd500_channel, program=27)
P07D=Program(hd500_port, channel=hd500_channel, program=28)
P08A=Program(hd500_port, channel=hd500_channel, program=29)
P08B=Program(hd500_port, channel=hd500_channel, program=30)
P08C=Program(hd500_port, channel=hd500_channel, program=31)
P08D=Program(hd500_port, channel=hd500_channel, program=32)
P09A=Program(hd500_port, channel=hd500_channel, program=33)
P09B=Program(hd500_port, channel=hd500_channel, program=34)
P09C=Program(hd500_port, channel=hd500_channel, program=35)
P09D=Program(hd500_port, channel=hd500_channel, program=36)
P10A=Program(hd500_port, channel=hd500_channel, program=37)
P10B=Program(hd500_port, channel=hd500_channel, program=38)
P10C=Program(hd500_port, channel=hd500_channel, program=39)
P10D=Program(hd500_port, channel=hd500_channel, program=40)
P11A=Program(hd500_port, channel=hd500_channel, program=41)
P11B=Program(hd500_port, channel=hd500_channel, program=42)
P11C=Program(hd500_port, channel=hd500_channel, program=43)
P11D=Program(hd500_port, channel=hd500_channel, program=44)
P12A=Program(hd500_port, channel=hd500_channel, program=45)
P12B=Program(hd500_port, channel=hd500_channel, program=46)
P12C=Program(hd500_port, channel=hd500_channel, program=47)
P12D=Program(hd500_port, channel=hd500_channel, program=48)
P13A=Program(hd500_port, channel=hd500_channel, program=49)
P13B=Program(hd500_port, channel=hd500_channel, program=50)
P13C=Program(hd500_port, channel=hd500_channel, program=51)
P13D=Program(hd500_port, channel=hd500_channel, program=52)
P14A=Program(hd500_port, channel=hd500_channel, program=53)
P14B=Program(hd500_port, channel=hd500_channel, program=54)
P14C=Program(hd500_port, channel=hd500_channel, program=55)
P14D=Program(hd500_port, channel=hd500_channel, program=56)
P15A=Program(hd500_port, channel=hd500_channel, program=57)
P15B=Program(hd500_port, channel=hd500_channel, program=58)
P15C=Program(hd500_port, channel=hd500_channel, program=59)
P15D=Program(hd500_port, channel=hd500_channel, program=60)
P16A=Program(hd500_port, channel=hd500_channel, program=61)
P16B=Program(hd500_port, channel=hd500_channel, program=62)
P16C=Program(hd500_port, channel=hd500_channel, program=63)
P16D=Program(hd500_port, channel=hd500_channel, program=64)

#

#
# POD-HD-500 to control Fender Super60
#

# Depend on hd500.py
S60A=Program(hd500_port, channel=hd500_channel, program=61)
S60B=Program(hd500_port, channel=hd500_channel, program=62)
S60C=Program(hd500_port, channel=hd500_channel, program=63)
S60D=Program(hd500_port, channel=hd500_channel, program=64)

# hd500_port, Channel, CC, Value
#Footsiwtch
FS1=Ctrl(hd500_port,hd500_channel,51,64)
FS2=Ctrl(hd500_port,hd500_channel,52,64)
FS3=Ctrl(hd500_port,hd500_channel,53,64)
FS4=Ctrl(hd500_port,hd500_channel,54,64)
FS5=Ctrl(hd500_port,hd500_channel,55,64)
FS6=Ctrl(hd500_port,hd500_channel,56,64)
FS7=Ctrl(hd500_port,hd500_channel,57,64)
FS8=Ctrl(hd500_port,hd500_channel,58,64)
TOE=Ctrl(hd500_port,hd500_channel,59,64)

#Pedal - useless

#Looper


#-----------------------------------------------------------------------------------------------------------
# GT10B configuration
# gt10b.py
#-----------------------------------------------------------------------------------------------------------
#
# This is the patches specific for a certain device
#
# BOSS GT_10B
#

# CONFIG

# channel
gt10b_ch=16

# port number
gt10b_port=3

gt10b_volume=(ChannelFilter(9) >> Channel(16) >> CtrlFilter(1) >> CtrlMap(1,7) >> Port(3))

# banks
gt10b_bank_0=(Ctrl(gt10b_port,gt10b_ch, 0, 0) // Ctrl(gt10b_port,gt10b_ch,32,0))
gt10b_bank_1=(Ctrl(gt10b_port,gt10b_ch, 0, 1) // Ctrl(gt10b_port,gt10b_ch,32,0))
gt10b_bank_2=(Ctrl(gt10b_port,gt10b_ch, 0, 2) // Ctrl(gt10b_port,gt10b_ch,32,0))
gt10b_bank_3=(Ctrl(gt10b_port,gt10b_ch, 0, 3) // Ctrl(gt10b_port,gt10b_ch,32,0))

# program (same for the 4 banks)
gt10b_pgrm_1 =Program(gt10b_port, channel=gt10b_ch, program= 1)
gt10b_pgrm_2 =Program(gt10b_port, channel=gt10b_ch, program= 2)
gt10b_pgrm_3 =Program(gt10b_port, channel=gt10b_ch, program= 3)
gt10b_pgrm_4 =Program(gt10b_port, channel=gt10b_ch, program= 4)
gt10b_pgrm_5 =Program(gt10b_port, channel=gt10b_ch, program= 5)
gt10b_pgrm_6 =Program(gt10b_port, channel=gt10b_ch, program= 6)
gt10b_pgrm_7 =Program(gt10b_port, channel=gt10b_ch, program= 7)
gt10b_pgrm_8 =Program(gt10b_port, channel=gt10b_ch, program= 8)
gt10b_pgrm_9 =Program(gt10b_port, channel=gt10b_ch, program= 9)
gt10b_pgrm_10=Program(gt10b_port, channel=gt10b_ch, program=10)
gt10b_pgrm_11=Program(gt10b_port, channel=gt10b_ch, program=11)
gt10b_pgrm_12=Program(gt10b_port, channel=gt10b_ch, program=12)
gt10b_pgrm_13=Program(gt10b_port, channel=gt10b_ch, program=13)
gt10b_pgrm_14=Program(gt10b_port, channel=gt10b_ch, program=14)
gt10b_pgrm_15=Program(gt10b_port, channel=gt10b_ch, program=15)
gt10b_pgrm_16=Program(gt10b_port, channel=gt10b_ch, program=16)
gt10b_pgrm_17=Program(gt10b_port, channel=gt10b_ch, program=17)
gt10b_pgrm_18=Program(gt10b_port, channel=gt10b_ch, program=18)
gt10b_pgrm_19=Program(gt10b_port, channel=gt10b_ch, program=19)
gt10b_pgrm_20=Program(gt10b_port, channel=gt10b_ch, program=20)
gt10b_pgrm_21=Program(gt10b_port, channel=gt10b_ch, program=21)
gt10b_pgrm_22=Program(gt10b_port, channel=gt10b_ch, program=22)
gt10b_pgrm_23=Program(gt10b_port, channel=gt10b_ch, program=23)
gt10b_pgrm_24=Program(gt10b_port, channel=gt10b_ch, program=24)
gt10b_pgrm_25=Program(gt10b_port, channel=gt10b_ch, program=25)
gt10b_pgrm_26=Program(gt10b_port, channel=gt10b_ch, program=26)
gt10b_pgrm_27=Program(gt10b_port, channel=gt10b_ch, program=27)
gt10b_pgrm_28=Program(gt10b_port, channel=gt10b_ch, program=28)
gt10b_pgrm_29=Program(gt10b_port, channel=gt10b_ch, program=29)
gt10b_pgrm_30=Program(gt10b_port, channel=gt10b_ch, program=30)
gt10b_pgrm_31=Program(gt10b_port, channel=gt10b_ch, program=31)
gt10b_pgrm_32=Program(gt10b_port, channel=gt10b_ch, program=32)
gt10b_pgrm_33=Program(gt10b_port, channel=gt10b_ch, program=33)
gt10b_pgrm_34=Program(gt10b_port, channel=gt10b_ch, program=34)
gt10b_pgrm_35=Program(gt10b_port, channel=gt10b_ch, program=35)
gt10b_pgrm_36=Program(gt10b_port, channel=gt10b_ch, program=36)
gt10b_pgrm_37=Program(gt10b_port, channel=gt10b_ch, program=37)
gt10b_pgrm_38=Program(gt10b_port, channel=gt10b_ch, program=38)
gt10b_pgrm_39=Program(gt10b_port, channel=gt10b_ch, program=39)
gt10b_pgrm_40=Program(gt10b_port, channel=gt10b_ch, program=40)
gt10b_pgrm_41=Program(gt10b_port, channel=gt10b_ch, program=41)
gt10b_pgrm_42=Program(gt10b_port, channel=gt10b_ch, program=42)
gt10b_pgrm_43=Program(gt10b_port, channel=gt10b_ch, program=43)
gt10b_pgrm_44=Program(gt10b_port, channel=gt10b_ch, program=44)
gt10b_pgrm_45=Program(gt10b_port, channel=gt10b_ch, program=45)
gt10b_pgrm_46=Program(gt10b_port, channel=gt10b_ch, program=46)
gt10b_pgrm_47=Program(gt10b_port, channel=gt10b_ch, program=47)
gt10b_pgrm_48=Program(gt10b_port, channel=gt10b_ch, program=48)
gt10b_pgrm_49=Program(gt10b_port, channel=gt10b_ch, program=49)
gt10b_pgrm_50=Program(gt10b_port, channel=gt10b_ch, program=50)
gt10b_pgrm_51=Program(gt10b_port, channel=gt10b_ch, program=51)
gt10b_pgrm_52=Program(gt10b_port, channel=gt10b_ch, program=52)
gt10b_pgrm_53=Program(gt10b_port, channel=gt10b_ch, program=53)
gt10b_pgrm_54=Program(gt10b_port, channel=gt10b_ch, program=54)
gt10b_pgrm_55=Program(gt10b_port, channel=gt10b_ch, program=55)
gt10b_pgrm_56=Program(gt10b_port, channel=gt10b_ch, program=56)
gt10b_pgrm_57=Program(gt10b_port, channel=gt10b_ch, program=57)
gt10b_pgrm_58=Program(gt10b_port, channel=gt10b_ch, program=58)
gt10b_pgrm_59=Program(gt10b_port, channel=gt10b_ch, program=59)
gt10b_pgrm_60=Program(gt10b_port, channel=gt10b_ch, program=60)
gt10b_pgrm_61=Program(gt10b_port, channel=gt10b_ch, program=61)
gt10b_pgrm_62=Program(gt10b_port, channel=gt10b_ch, program=62)
gt10b_pgrm_63=Program(gt10b_port, channel=gt10b_ch, program=63)
gt10b_pgrm_64=Program(gt10b_port, channel=gt10b_ch, program=64)
gt10b_pgrm_65=Program(gt10b_port, channel=gt10b_ch, program=65)
gt10b_pgrm_66=Program(gt10b_port, channel=gt10b_ch, program=66)
gt10b_pgrm_67=Program(gt10b_port, channel=gt10b_ch, program=67)
gt10b_pgrm_68=Program(gt10b_port, channel=gt10b_ch, program=68)
gt10b_pgrm_69=Program(gt10b_port, channel=gt10b_ch, program=69)
gt10b_pgrm_70=Program(gt10b_port, channel=gt10b_ch, program=70)
gt10b_pgrm_71=Program(gt10b_port, channel=gt10b_ch, program=71)
gt10b_pgrm_72=Program(gt10b_port, channel=gt10b_ch, program=72)
gt10b_pgrm_73=Program(gt10b_port, channel=gt10b_ch, program=73)
gt10b_pgrm_74=Program(gt10b_port, channel=gt10b_ch, program=74)
gt10b_pgrm_75=Program(gt10b_port, channel=gt10b_ch, program=75)
gt10b_pgrm_76=Program(gt10b_port, channel=gt10b_ch, program=76)
gt10b_pgrm_77=Program(gt10b_port, channel=gt10b_ch, program=77)
gt10b_pgrm_78=Program(gt10b_port, channel=gt10b_ch, program=78)
gt10b_pgrm_79=Program(gt10b_port, channel=gt10b_ch, program=79)
gt10b_pgrm_80=Program(gt10b_port, channel=gt10b_ch, program=80)
gt10b_pgrm_81=Program(gt10b_port, channel=gt10b_ch, program=81)
gt10b_pgrm_82=Program(gt10b_port, channel=gt10b_ch, program=82)
gt10b_pgrm_83=Program(gt10b_port, channel=gt10b_ch, program=83)
gt10b_pgrm_84=Program(gt10b_port, channel=gt10b_ch, program=84)
gt10b_pgrm_85=Program(gt10b_port, channel=gt10b_ch, program=85)
gt10b_pgrm_86=Program(gt10b_port, channel=gt10b_ch, program=86)
gt10b_pgrm_87=Program(gt10b_port, channel=gt10b_ch, program=87)
gt10b_pgrm_88=Program(gt10b_port, channel=gt10b_ch, program=88)
gt10b_pgrm_89=Program(gt10b_port, channel=gt10b_ch, program=89)
gt10b_pgrm_90=Program(gt10b_port, channel=gt10b_ch, program=90)
gt10b_pgrm_91=Program(gt10b_port, channel=gt10b_ch, program=91)
gt10b_pgrm_92=Program(gt10b_port, channel=gt10b_ch, program=92)
gt10b_pgrm_93=Program(gt10b_port, channel=gt10b_ch, program=93)
gt10b_pgrm_94=Program(gt10b_port, channel=gt10b_ch, program=94)
gt10b_pgrm_95=Program(gt10b_port, channel=gt10b_ch, program=95)
gt10b_pgrm_96=Program(gt10b_port, channel=gt10b_ch, program=96)
gt10b_pgrm_97=Program(gt10b_port, channel=gt10b_ch, program=97)
gt10b_pgrm_98=Program(gt10b_port, channel=gt10b_ch, program=98)
gt10b_pgrm_99=Program(gt10b_port, channel=gt10b_ch, program=99)
gt10b_pgrm_100=Program(gt10b_port, channel=gt10b_ch, program=100)

# gt10b_bank 0
U01_A=(gt10b_bank_0 // gt10b_pgrm_1 )
U01_B=(gt10b_bank_0 // gt10b_pgrm_2 )
U01_C=(gt10b_bank_0 // gt10b_pgrm_3 )
U01_D=(gt10b_bank_0 // gt10b_pgrm_4 )
U02_A=(gt10b_bank_0 // gt10b_pgrm_5 )
U02_B=(gt10b_bank_0 // gt10b_pgrm_6 )
U02_C=(gt10b_bank_0 // gt10b_pgrm_7 )
U02_D=(gt10b_bank_0 // gt10b_pgrm_8 ) 
U03_A=(gt10b_bank_0 // gt10b_pgrm_9 )
U03_B=(gt10b_bank_0 // gt10b_pgrm_10)
U03_C=(gt10b_bank_0 // gt10b_pgrm_11)
U03_D=(gt10b_bank_0 // gt10b_pgrm_12)
U04_A=(gt10b_bank_0 // gt10b_pgrm_13)
U04_B=(gt10b_bank_0 // gt10b_pgrm_14)
U04_C=(gt10b_bank_0 // gt10b_pgrm_15)
U04_D=(gt10b_bank_0 // gt10b_pgrm_16)
U05_A=(gt10b_bank_0 // gt10b_pgrm_17)
U05_B=(gt10b_bank_0 // gt10b_pgrm_18)
U05_C=(gt10b_bank_0 // gt10b_pgrm_19)
U05_D=(gt10b_bank_0 // gt10b_pgrm_20)
U06_A=(gt10b_bank_0 // gt10b_pgrm_21)
U06_B=(gt10b_bank_0 // gt10b_pgrm_22)
U06_C=(gt10b_bank_0 // gt10b_pgrm_23)
U06_D=(gt10b_bank_0 // gt10b_pgrm_24)
U07_A=(gt10b_bank_0 // gt10b_pgrm_25)
U07_B=(gt10b_bank_0 // gt10b_pgrm_26)
U07_C=(gt10b_bank_0 // gt10b_pgrm_27)
U07_D=(gt10b_bank_0 // gt10b_pgrm_28)
U08_A=(gt10b_bank_0 // gt10b_pgrm_29)
U08_B=(gt10b_bank_0 // gt10b_pgrm_30)
U08_C=(gt10b_bank_0 // gt10b_pgrm_31)
U08_D=(gt10b_bank_0 // gt10b_pgrm_32)
U09_A=(gt10b_bank_0 // gt10b_pgrm_33)
U09_B=(gt10b_bank_0 // gt10b_pgrm_34)
U09_C=(gt10b_bank_0 // gt10b_pgrm_35)
U09_D=(gt10b_bank_0 // gt10b_pgrm_36)
U10_A=(gt10b_bank_0 // gt10b_pgrm_37)
U10_B=(gt10b_bank_0 // gt10b_pgrm_38)
U10_C=(gt10b_bank_0 // gt10b_pgrm_39)
U10_D=(gt10b_bank_0 // gt10b_pgrm_40)
U11_A=(gt10b_bank_0 // gt10b_pgrm_41)
U11_B=(gt10b_bank_0 // gt10b_pgrm_42)
U11_C=(gt10b_bank_0 // gt10b_pgrm_43)
U11_D=(gt10b_bank_0 // gt10b_pgrm_44)
U12_A=(gt10b_bank_0 // gt10b_pgrm_45)
U12_B=(gt10b_bank_0 // gt10b_pgrm_46)
U12_C=(gt10b_bank_0 // gt10b_pgrm_47)
U12_D=(gt10b_bank_0 // gt10b_pgrm_48)
U13_A=(gt10b_bank_0 // gt10b_pgrm_49)
U13_B=(gt10b_bank_0 // gt10b_pgrm_50)
U13_C=(gt10b_bank_0 // gt10b_pgrm_51)
U13_D=(gt10b_bank_0 // gt10b_pgrm_52)
U14_A=(gt10b_bank_0 // gt10b_pgrm_53)
U14_B=(gt10b_bank_0 // gt10b_pgrm_54)
U14_C=(gt10b_bank_0 // gt10b_pgrm_55)
U14_D=(gt10b_bank_0 // gt10b_pgrm_56)
U15_A=(gt10b_bank_0 // gt10b_pgrm_57)
U15_B=(gt10b_bank_0 // gt10b_pgrm_58)
U15_C=(gt10b_bank_0 // gt10b_pgrm_59)
U15_D=(gt10b_bank_0 // gt10b_pgrm_60)
U16_A=(gt10b_bank_0 // gt10b_pgrm_61)
U16_B=(gt10b_bank_0 // gt10b_pgrm_62)
U16_C=(gt10b_bank_0 // gt10b_pgrm_63)
U16_D=(gt10b_bank_0 // gt10b_pgrm_64)
U17_A=(gt10b_bank_0 // gt10b_pgrm_65)
U17_B=(gt10b_bank_0 // gt10b_pgrm_66)
U17_C=(gt10b_bank_0 // gt10b_pgrm_67)
U17_D=(gt10b_bank_0 // gt10b_pgrm_68)
U18_A=(gt10b_bank_0 // gt10b_pgrm_69)
U18_B=(gt10b_bank_0 // gt10b_pgrm_70)
U18_C=(gt10b_bank_0 // gt10b_pgrm_71)
U18_D=(gt10b_bank_0 // gt10b_pgrm_72)
U19_A=(gt10b_bank_0 // gt10b_pgrm_73)
U19_B=(gt10b_bank_0 // gt10b_pgrm_74)
U19_C=(gt10b_bank_0 // gt10b_pgrm_75)
U19_D=(gt10b_bank_0 // gt10b_pgrm_76)
U20_A=(gt10b_bank_0 // gt10b_pgrm_77)
U20_B=(gt10b_bank_0 // gt10b_pgrm_78)
U20_C=(gt10b_bank_0 // gt10b_pgrm_79)
U20_D=(gt10b_bank_0 // gt10b_pgrm_80)
U21_A=(gt10b_bank_0 // gt10b_pgrm_81)
U21_B=(gt10b_bank_0 // gt10b_pgrm_82)
U21_C=(gt10b_bank_0 // gt10b_pgrm_83)
U21_D=(gt10b_bank_0 // gt10b_pgrm_84)
U22_A=(gt10b_bank_0 // gt10b_pgrm_85)
U22_B=(gt10b_bank_0 // gt10b_pgrm_86)
U22_C=(gt10b_bank_0 // gt10b_pgrm_87)
U22_D=(gt10b_bank_0 // gt10b_pgrm_88)
U23_A=(gt10b_bank_0 // gt10b_pgrm_89)
U23_B=(gt10b_bank_0 // gt10b_pgrm_90)
U23_C=(gt10b_bank_0 // gt10b_pgrm_91)
U23_D=(gt10b_bank_0 // gt10b_pgrm_92)
U24_A=(gt10b_bank_0 // gt10b_pgrm_93)
U24_B=(gt10b_bank_0 // gt10b_pgrm_94)
U24_C=(gt10b_bank_0 // gt10b_pgrm_95)
U24_D=(gt10b_bank_0 // gt10b_pgrm_96)
U25_A=(gt10b_bank_0 // gt10b_pgrm_97)
U25_B=(gt10b_bank_0 // gt10b_pgrm_98)
U25_C=(gt10b_bank_0 // gt10b_pgrm_99)
U25_D=(gt10b_bank_0 // gt10b_pgrm_100)

# gt10b_bank 1
U26_A=(gt10b_bank_1 // gt10b_pgrm_1 )
U26_B=(gt10b_bank_1 // gt10b_pgrm_2 )
U26_C=(gt10b_bank_1 // gt10b_pgrm_3 )
U26_D=(gt10b_bank_1 // gt10b_pgrm_4 )
U27_A=(gt10b_bank_1 // gt10b_pgrm_5 )
U27_B=(gt10b_bank_1 // gt10b_pgrm_6 )
U27_C=(gt10b_bank_1 // gt10b_pgrm_7 )
U27_D=(gt10b_bank_1 // gt10b_pgrm_8 ) 
U28_A=(gt10b_bank_1 // gt10b_pgrm_9 )
U28_B=(gt10b_bank_1 // gt10b_pgrm_10)
U28_C=(gt10b_bank_1 // gt10b_pgrm_11)
U28_D=(gt10b_bank_1 // gt10b_pgrm_12)
U29_A=(gt10b_bank_1 // gt10b_pgrm_13)
U29_B=(gt10b_bank_1 // gt10b_pgrm_14)
U29_C=(gt10b_bank_1 // gt10b_pgrm_15)
U29_D=(gt10b_bank_1 // gt10b_pgrm_16)
U30_A=(gt10b_bank_1 // gt10b_pgrm_17)
U30_B=(gt10b_bank_1 // gt10b_pgrm_18)
U30_C=(gt10b_bank_1 // gt10b_pgrm_19)
U30_D=(gt10b_bank_1 // gt10b_pgrm_20)
U31_A=(gt10b_bank_1 // gt10b_pgrm_21)
U31_B=(gt10b_bank_1 // gt10b_pgrm_22)
U31_C=(gt10b_bank_1 // gt10b_pgrm_23)
U31_D=(gt10b_bank_1 // gt10b_pgrm_24)
U32_A=(gt10b_bank_1 // gt10b_pgrm_25)
U32_B=(gt10b_bank_1 // gt10b_pgrm_26)
U32_C=(gt10b_bank_1 // gt10b_pgrm_27)
U32_D=(gt10b_bank_1 // gt10b_pgrm_28)
U33_A=(gt10b_bank_1 // gt10b_pgrm_29)
U33_B=(gt10b_bank_1 // gt10b_pgrm_30)
U33_C=(gt10b_bank_1 // gt10b_pgrm_31)
U33_D=(gt10b_bank_1 // gt10b_pgrm_32)
U34_A=(gt10b_bank_1 // gt10b_pgrm_33)
U34_B=(gt10b_bank_1 // gt10b_pgrm_34)
U34_C=(gt10b_bank_1 // gt10b_pgrm_35)
U34_D=(gt10b_bank_1 // gt10b_pgrm_36)
U35_A=(gt10b_bank_1 // gt10b_pgrm_37)
U35_B=(gt10b_bank_1 // gt10b_pgrm_38)
U35_C=(gt10b_bank_1 // gt10b_pgrm_39)
U35_D=(gt10b_bank_1 // gt10b_pgrm_40)
U36_A=(gt10b_bank_1 // gt10b_pgrm_41)
U36_B=(gt10b_bank_1 // gt10b_pgrm_42)
U36_C=(gt10b_bank_1 // gt10b_pgrm_43)
U36_D=(gt10b_bank_1 // gt10b_pgrm_44)
U37_A=(gt10b_bank_1 // gt10b_pgrm_45)
U37_B=(gt10b_bank_1 // gt10b_pgrm_46)
U37_C=(gt10b_bank_1 // gt10b_pgrm_47)
U37_D=(gt10b_bank_1 // gt10b_pgrm_48)
U38_A=(gt10b_bank_1 // gt10b_pgrm_49)
U38_B=(gt10b_bank_1 // gt10b_pgrm_50)
U38_C=(gt10b_bank_1 // gt10b_pgrm_51)
U38_D=(gt10b_bank_1 // gt10b_pgrm_52)
U39_A=(gt10b_bank_1 // gt10b_pgrm_53)
U39_B=(gt10b_bank_1 // gt10b_pgrm_54)
U39_C=(gt10b_bank_1 // gt10b_pgrm_55)
U39_D=(gt10b_bank_1 // gt10b_pgrm_56)
U40_A=(gt10b_bank_1 // gt10b_pgrm_57)
U40_B=(gt10b_bank_1 // gt10b_pgrm_58)
U40_C=(gt10b_bank_1 // gt10b_pgrm_59)
U40_D=(gt10b_bank_1 // gt10b_pgrm_60)
U41_A=(gt10b_bank_1 // gt10b_pgrm_61)
U41_B=(gt10b_bank_1 // gt10b_pgrm_62)
U41_C=(gt10b_bank_1 // gt10b_pgrm_63)
U41_D=(gt10b_bank_1 // gt10b_pgrm_64)
U42_A=(gt10b_bank_1 // gt10b_pgrm_65)
U42_B=(gt10b_bank_1 // gt10b_pgrm_66)
U42_C=(gt10b_bank_1 // gt10b_pgrm_67)
U42_D=(gt10b_bank_1 // gt10b_pgrm_68)
U43_A=(gt10b_bank_1 // gt10b_pgrm_69)
U43_B=(gt10b_bank_1 // gt10b_pgrm_70)
U43_C=(gt10b_bank_1 // gt10b_pgrm_71)
U43_D=(gt10b_bank_1 // gt10b_pgrm_72)
U44_A=(gt10b_bank_1 // gt10b_pgrm_73)
U44_B=(gt10b_bank_1 // gt10b_pgrm_74)
U44_C=(gt10b_bank_1 // gt10b_pgrm_75)
U44_D=(gt10b_bank_1 // gt10b_pgrm_76)
U45_A=(gt10b_bank_1 // gt10b_pgrm_77)
U45_B=(gt10b_bank_1 // gt10b_pgrm_78)
U45_C=(gt10b_bank_1 // gt10b_pgrm_79)
U45_D=(gt10b_bank_1 // gt10b_pgrm_80)
U46_A=(gt10b_bank_1 // gt10b_pgrm_81)
U46_B=(gt10b_bank_1 // gt10b_pgrm_82)
U46_C=(gt10b_bank_1 // gt10b_pgrm_83)
U46_D=(gt10b_bank_1 // gt10b_pgrm_84)
U47_A=(gt10b_bank_1 // gt10b_pgrm_85)
U47_B=(gt10b_bank_1 // gt10b_pgrm_86)
U47_C=(gt10b_bank_1 // gt10b_pgrm_87)
U47_D=(gt10b_bank_1 // gt10b_pgrm_88)
U48_A=(gt10b_bank_1 // gt10b_pgrm_89)
U48_B=(gt10b_bank_1 // gt10b_pgrm_90)
U48_C=(gt10b_bank_1 // gt10b_pgrm_91)
U48_D=(gt10b_bank_1 // gt10b_pgrm_92)
U49_A=(gt10b_bank_1 // gt10b_pgrm_93)
U49_B=(gt10b_bank_1 // gt10b_pgrm_94)
U49_C=(gt10b_bank_1 // gt10b_pgrm_95)
U49_D=(gt10b_bank_1 // gt10b_pgrm_96)
U50_A=(gt10b_bank_1 // gt10b_pgrm_97)
U50_B=(gt10b_bank_1 // gt10b_pgrm_98)
U50_C=(gt10b_bank_1 // gt10b_pgrm_99)
U50_D=(gt10b_bank_1 // gt10b_pgrm_100)

# gt10b_bank 2
P01_A=(gt10b_bank_2 // gt10b_pgrm_1 )
P01_B=(gt10b_bank_2 // gt10b_pgrm_2 )
P01_C=(gt10b_bank_2 // gt10b_pgrm_3 )
P01_D=(gt10b_bank_2 // gt10b_pgrm_4 )
P02_A=(gt10b_bank_2 // gt10b_pgrm_5 )
P02_B=(gt10b_bank_2 // gt10b_pgrm_6 )
P02_C=(gt10b_bank_2 // gt10b_pgrm_7 )
P02_D=(gt10b_bank_2 // gt10b_pgrm_8 ) 
P03_A=(gt10b_bank_2 // gt10b_pgrm_9 )
P03_B=(gt10b_bank_2 // gt10b_pgrm_10)
P03_C=(gt10b_bank_2 // gt10b_pgrm_11)
P03_D=(gt10b_bank_2 // gt10b_pgrm_12)
P04_A=(gt10b_bank_2 // gt10b_pgrm_13)
P04_B=(gt10b_bank_2 // gt10b_pgrm_14)
P04_C=(gt10b_bank_2 // gt10b_pgrm_15)
P04_D=(gt10b_bank_2 // gt10b_pgrm_16)
P05_A=(gt10b_bank_2 // gt10b_pgrm_17)
P05_B=(gt10b_bank_2 // gt10b_pgrm_18)
P05_C=(gt10b_bank_2 // gt10b_pgrm_19)
P05_D=(gt10b_bank_2 // gt10b_pgrm_20)
P06_A=(gt10b_bank_2 // gt10b_pgrm_21)
P06_B=(gt10b_bank_2 // gt10b_pgrm_22)
P06_C=(gt10b_bank_2 // gt10b_pgrm_23)
P06_D=(gt10b_bank_2 // gt10b_pgrm_24)
P07_A=(gt10b_bank_2 // gt10b_pgrm_25)
P07_B=(gt10b_bank_2 // gt10b_pgrm_26)
P07_C=(gt10b_bank_2 // gt10b_pgrm_27)
P07_D=(gt10b_bank_2 // gt10b_pgrm_28)
P08_A=(gt10b_bank_2 // gt10b_pgrm_29)
P08_B=(gt10b_bank_2 // gt10b_pgrm_30)
P08_C=(gt10b_bank_2 // gt10b_pgrm_31)
P08_D=(gt10b_bank_2 // gt10b_pgrm_32)
P09_A=(gt10b_bank_2 // gt10b_pgrm_33)
P09_B=(gt10b_bank_2 // gt10b_pgrm_34)
P09_C=(gt10b_bank_2 // gt10b_pgrm_35)
P09_D=(gt10b_bank_2 // gt10b_pgrm_36)
P10_A=(gt10b_bank_2 // gt10b_pgrm_37)
P10_B=(gt10b_bank_2 // gt10b_pgrm_38)
P10_C=(gt10b_bank_2 // gt10b_pgrm_39)
P10_D=(gt10b_bank_2 // gt10b_pgrm_40)
P11_A=(gt10b_bank_2 // gt10b_pgrm_41)
P11_B=(gt10b_bank_2 // gt10b_pgrm_42)
P11_C=(gt10b_bank_2 // gt10b_pgrm_43)
P11_D=(gt10b_bank_2 // gt10b_pgrm_44)
P12_A=(gt10b_bank_2 // gt10b_pgrm_45)
P12_B=(gt10b_bank_2 // gt10b_pgrm_46)
P12_C=(gt10b_bank_2 // gt10b_pgrm_47)
P12_D=(gt10b_bank_2 // gt10b_pgrm_48)
P13_A=(gt10b_bank_2 // gt10b_pgrm_49)
P13_B=(gt10b_bank_2 // gt10b_pgrm_50)
P13_C=(gt10b_bank_2 // gt10b_pgrm_51)
P13_D=(gt10b_bank_2 // gt10b_pgrm_52)
P14_A=(gt10b_bank_2 // gt10b_pgrm_53)
P14_B=(gt10b_bank_2 // gt10b_pgrm_54)
P14_C=(gt10b_bank_2 // gt10b_pgrm_55)
P14_D=(gt10b_bank_2 // gt10b_pgrm_56)
P15_A=(gt10b_bank_2 // gt10b_pgrm_57)
P15_B=(gt10b_bank_2 // gt10b_pgrm_58)
P15_C=(gt10b_bank_2 // gt10b_pgrm_59)
P15_D=(gt10b_bank_2 // gt10b_pgrm_60)
P16_A=(gt10b_bank_2 // gt10b_pgrm_61)
P16_B=(gt10b_bank_2 // gt10b_pgrm_62)
P16_C=(gt10b_bank_2 // gt10b_pgrm_63)
P16_D=(gt10b_bank_2 // gt10b_pgrm_64)
P17_A=(gt10b_bank_2 // gt10b_pgrm_65)
P17_B=(gt10b_bank_2 // gt10b_pgrm_66)
P17_C=(gt10b_bank_2 // gt10b_pgrm_67)
P17_D=(gt10b_bank_2 // gt10b_pgrm_68)
P18_A=(gt10b_bank_2 // gt10b_pgrm_69)
P18_B=(gt10b_bank_2 // gt10b_pgrm_70)
P18_C=(gt10b_bank_2 // gt10b_pgrm_71)
P18_D=(gt10b_bank_2 // gt10b_pgrm_72)
P19_A=(gt10b_bank_2 // gt10b_pgrm_73)
P19_B=(gt10b_bank_2 // gt10b_pgrm_74)
P19_C=(gt10b_bank_2 // gt10b_pgrm_75)
P19_D=(gt10b_bank_2 // gt10b_pgrm_76)
P20_A=(gt10b_bank_2 // gt10b_pgrm_77)
P20_B=(gt10b_bank_2 // gt10b_pgrm_78)
P20_C=(gt10b_bank_2 // gt10b_pgrm_79)
P20_D=(gt10b_bank_2 // gt10b_pgrm_80)
P21_A=(gt10b_bank_2 // gt10b_pgrm_81)
P21_B=(gt10b_bank_2 // gt10b_pgrm_82)
P21_C=(gt10b_bank_2 // gt10b_pgrm_83)
P21_D=(gt10b_bank_2 // gt10b_pgrm_84)
P22_A=(gt10b_bank_2 // gt10b_pgrm_85)
P22_B=(gt10b_bank_2 // gt10b_pgrm_86)
P22_C=(gt10b_bank_2 // gt10b_pgrm_87)
P22_D=(gt10b_bank_2 // gt10b_pgrm_88)
P23_A=(gt10b_bank_2 // gt10b_pgrm_89)
P23_B=(gt10b_bank_2 // gt10b_pgrm_90)
P23_C=(gt10b_bank_2 // gt10b_pgrm_91)
P23_D=(gt10b_bank_2 // gt10b_pgrm_92)
P24_A=(gt10b_bank_2 // gt10b_pgrm_93)
P24_B=(gt10b_bank_2 // gt10b_pgrm_94)
P24_C=(gt10b_bank_2 // gt10b_pgrm_95)
P24_D=(gt10b_bank_2 // gt10b_pgrm_96)
P25_A=(gt10b_bank_2 // gt10b_pgrm_97)
P25_B=(gt10b_bank_2 // gt10b_pgrm_98)
P25_C=(gt10b_bank_2 // gt10b_pgrm_99)
P25_D=(gt10b_bank_2 // gt10b_pgrm_100)
# gt10b_bank 3
P26_A=(gt10b_bank_3 // gt10b_pgrm_1 )
P26_B=(gt10b_bank_3 // gt10b_pgrm_2 )
P26_C=(gt10b_bank_3 // gt10b_pgrm_3 )
P26_D=(gt10b_bank_3 // gt10b_pgrm_4 )
P27_A=(gt10b_bank_3 // gt10b_pgrm_5 )
P27_B=(gt10b_bank_3 // gt10b_pgrm_6 )
P27_C=(gt10b_bank_3 // gt10b_pgrm_7 )
P27_D=(gt10b_bank_3 // gt10b_pgrm_8 ) 
P28_A=(gt10b_bank_3 // gt10b_pgrm_9 )
P28_B=(gt10b_bank_3 // gt10b_pgrm_10)
P28_C=(gt10b_bank_3 // gt10b_pgrm_11)
P28_D=(gt10b_bank_3 // gt10b_pgrm_12)
P29_A=(gt10b_bank_3 // gt10b_pgrm_13)
P29_B=(gt10b_bank_3 // gt10b_pgrm_14)
P29_C=(gt10b_bank_3 // gt10b_pgrm_15)
P29_D=(gt10b_bank_3 // gt10b_pgrm_16)
P30_A=(gt10b_bank_3 // gt10b_pgrm_17)
P30_B=(gt10b_bank_3 // gt10b_pgrm_18)
P30_C=(gt10b_bank_3 // gt10b_pgrm_19)
P30_D=(gt10b_bank_3 // gt10b_pgrm_20)
P31_A=(gt10b_bank_3 // gt10b_pgrm_21)
P31_B=(gt10b_bank_3 // gt10b_pgrm_22)
P31_C=(gt10b_bank_3 // gt10b_pgrm_23)
P31_D=(gt10b_bank_3 // gt10b_pgrm_24)
P32_A=(gt10b_bank_3 // gt10b_pgrm_25)
P32_B=(gt10b_bank_3 // gt10b_pgrm_26)
P32_C=(gt10b_bank_3 // gt10b_pgrm_27)
P32_D=(gt10b_bank_3 // gt10b_pgrm_28)
P33_A=(gt10b_bank_3 // gt10b_pgrm_29)
P33_B=(gt10b_bank_3 // gt10b_pgrm_30)
P33_C=(gt10b_bank_3 // gt10b_pgrm_31)
P33_D=(gt10b_bank_3 // gt10b_pgrm_32)
P34_A=(gt10b_bank_3 // gt10b_pgrm_33)
P34_B=(gt10b_bank_3 // gt10b_pgrm_34)
P34_C=(gt10b_bank_3 // gt10b_pgrm_35)
P34_D=(gt10b_bank_3 // gt10b_pgrm_36)
P35_A=(gt10b_bank_3 // gt10b_pgrm_37)
P35_B=(gt10b_bank_3 // gt10b_pgrm_38)
P35_C=(gt10b_bank_3 // gt10b_pgrm_39)
P35_D=(gt10b_bank_3 // gt10b_pgrm_40)
P36_A=(gt10b_bank_3 // gt10b_pgrm_41)
P36_B=(gt10b_bank_3 // gt10b_pgrm_42)
P36_C=(gt10b_bank_3 // gt10b_pgrm_43)
P36_D=(gt10b_bank_3 // gt10b_pgrm_44)
P37_A=(gt10b_bank_3 // gt10b_pgrm_45)
P37_B=(gt10b_bank_3 // gt10b_pgrm_46)
P37_C=(gt10b_bank_3 // gt10b_pgrm_47)
P37_D=(gt10b_bank_3 // gt10b_pgrm_48)
P38_A=(gt10b_bank_3 // gt10b_pgrm_49)
P38_B=(gt10b_bank_3 // gt10b_pgrm_50)
P38_C=(gt10b_bank_3 // gt10b_pgrm_51)
P38_D=(gt10b_bank_3 // gt10b_pgrm_52)
P39_A=(gt10b_bank_3 // gt10b_pgrm_53)
P39_B=(gt10b_bank_3 // gt10b_pgrm_54)
P39_C=(gt10b_bank_3 // gt10b_pgrm_55)
P39_D=(gt10b_bank_3 // gt10b_pgrm_56)
P40_A=(gt10b_bank_3 // gt10b_pgrm_57)
P40_B=(gt10b_bank_3 // gt10b_pgrm_58)
P40_C=(gt10b_bank_3 // gt10b_pgrm_59)
P40_D=(gt10b_bank_3 // gt10b_pgrm_60)
P41_A=(gt10b_bank_3 // gt10b_pgrm_61)
P41_B=(gt10b_bank_3 // gt10b_pgrm_62)
P41_C=(gt10b_bank_3 // gt10b_pgrm_63)
P41_D=(gt10b_bank_3 // gt10b_pgrm_64)
P42_A=(gt10b_bank_3 // gt10b_pgrm_65)
P42_B=(gt10b_bank_3 // gt10b_pgrm_66)
P42_C=(gt10b_bank_3 // gt10b_pgrm_67)
P42_D=(gt10b_bank_3 // gt10b_pgrm_68)
P43_A=(gt10b_bank_3 // gt10b_pgrm_69)
P43_B=(gt10b_bank_3 // gt10b_pgrm_70)
P43_C=(gt10b_bank_3 // gt10b_pgrm_71)
P43_D=(gt10b_bank_3 // gt10b_pgrm_72)
P44_A=(gt10b_bank_3 // gt10b_pgrm_73)
P44_B=(gt10b_bank_3 // gt10b_pgrm_74)
P44_C=(gt10b_bank_3 // gt10b_pgrm_75)
P44_D=(gt10b_bank_3 // gt10b_pgrm_76)
P45_A=(gt10b_bank_3 // gt10b_pgrm_77)
P45_B=(gt10b_bank_3 // gt10b_pgrm_78)
P45_C=(gt10b_bank_3 // gt10b_pgrm_79)
P45_D=(gt10b_bank_3 // gt10b_pgrm_80)
P46_A=(gt10b_bank_3 // gt10b_pgrm_81)
P46_B=(gt10b_bank_3 // gt10b_pgrm_82)
P46_C=(gt10b_bank_3 // gt10b_pgrm_83)
P46_D=(gt10b_bank_3 // gt10b_pgrm_84)
P47_A=(gt10b_bank_3 // gt10b_pgrm_85)
P47_B=(gt10b_bank_3 // gt10b_pgrm_86)
P47_C=(gt10b_bank_3 // gt10b_pgrm_87)
P47_D=(gt10b_bank_3 // gt10b_pgrm_88)
P48_A=(gt10b_bank_3 // gt10b_pgrm_89)
P48_B=(gt10b_bank_3 // gt10b_pgrm_90)
P48_C=(gt10b_bank_3 // gt10b_pgrm_91)
P48_D=(gt10b_bank_3 // gt10b_pgrm_92)
P49_A=(gt10b_bank_3 // gt10b_pgrm_93)
P49_B=(gt10b_bank_3 // gt10b_pgrm_94)
P49_C=(gt10b_bank_3 // gt10b_pgrm_95)
P49_D=(gt10b_bank_3 // gt10b_pgrm_96)
P50_A=(gt10b_bank_3 // gt10b_pgrm_97)
P50_B=(gt10b_bank_3 // gt10b_pgrm_98)
P50_C=(gt10b_bank_3 // gt10b_pgrm_99)
P50_D=(gt10b_bank_3 // gt10b_pgrm_100)

# PortU, _Channel, CC, Value
#FootsUiw_tch
#GT10BU_F_S1=Ctrl(3,9,51,64)
#GT10BU_F_S2=Ctrl(3,9,52,64)
#GT10BU_F_S3=Ctrl(3,9,53,64)
#GT10BU_F_S4=Ctrl(3,9,54,64)
#GT10BU_F_S5=Ctrl(3,9,55,64)
#GT10BU_F_S6=Ctrl(3,9,56,64)
#GT10BU_F_S7=Ctrl(3,9,57,64)
#GT10BU_F_S8=Ctrl(3,9,58,64)
#GT10BU_T_OE=Ctrl(3,9,59,64)

#-----------------------------------------------------------------------------------------------------------
# Patches configuration
# patches.py
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# PROGRAM CHANGE SECTION
#-----------------------------------------------------------------------------------------------
phantom=Velocity(fixed=0) >> Output('SD90_PARTA', channel=1, program=((96*128),1), volume=0)

# Works great in init_patch
#Chorus=Ctrl(3,1,93,127)
#Reverb =Ctrl(3,1,93,127)

# PORTAMENTO 
portamento_base=Ctrl(1,1,5,50)
portamento_off=Ctrl(1,1,65,0)	# Switch OFF
portamento_on=Ctrl(1,1,65,127)  # Switch ON
portamento_up=(portamento_base // portamento_on)
portamento_off=(portamento_base // portamento_off)

#Pas de resultat encore
#legato=Ctrl(1,1,120,0)

# Simple output patch for testing equipment
#SD90_PARTA=cf >> Output('SD90_PARTA', channel=1, program=1, volume=100)
#SD90_PARTA=cf >> Output('SD90_PARTA', channel=2, program=1, volume=100)
#SD90_PARTA_drum=cf >> Channel(10) >> Transpose(-24) >> Output('SD90_PARTA', channel=10, program=1, volume=100)
d4=cf >> Output('SD90_PARTA', channel=10, program=1, volume=100)
d4_tom=cf >> Output('SD90_PARTA', channel=11, program=((96*128)+1,118), volume=100)

### SD-90 Full Patch implementation
#TODO


# FX Section
explosion = cf >> Key(0) >> Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------
violon = cf >> Output('SD90_PARTA', channel=1, program=((96*128),41))
piano_base = cf >> Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((96*128),1))
nf_piano = Output('SD90_PARTA', channel=1, program=((96*128),2), volume=100)
piano = ChannelFilter(1) >> Velocity(fixed=80) >> Output('SD90_PARTA', channel=3, program=((96*128),1), volume=100)
piano2 = Output('SD90_PARTA', channel=2, program=((96*128),2), volume=100)

# Patch Synth
keysynth = cf >> Velocity(fixed=80) >> Output('SD90_PARTA', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
# Q49 only
marathon_intro=(q49>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output('SD90_PARTA', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

# Note : ChannelFilter 2 - Enable PK5 message only
marathon_chords=(pk5 >> LatchNotes(False, reset='c4') >> Velocity(fixed=80) >>
	(

		# From first to last...
		(KeyFilter('e3') >> Key('b3') >> Harmonize('b','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('c3') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('d3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //

		# From first to last 2 frets higher
		(KeyFilter('a3') >> Key('c#4') >> Harmonize('c#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('f3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('g3') >> Key('g#3') >> Harmonize('g#','major',['unison', 'third', 'fifth', 'octave'])) // 

        # Isolated note
        (KeyFilter('b3') >> Key('a6'))

	) >> Transpose(-24) >> Output('SD90_PARTA', channel=4, program=((96*128)+1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(q49 >> 
	( 
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output('SD90_PARTA', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(q49 >>
	( 
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output('SD90_PARTA', channel=4, program=((96*128),51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(q49 >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output('SD90_PARTB', channel=11, program=((99*128),99), volume=80))

marathon_bridge_split=cf>> KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
lowsynth2 = cf >> Velocity(fixed=115) >> Output('SD90_PARTA', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('SD90_PARTA', channel=1, program=((99*128),15), volume=100)
closer_base = Velocity(fixed=100) >> Output('SD90_PARTA', channel=2, program=((99*128),51), volume=100)
closer_main = cf >> KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('SD90_PARTA', channel=3, program=((99*128),92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('SD90_PARTA', channel=3, program=((99*128),92), volume=100)
tss_keyboard_main = cf >> KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('SD90_PARTA', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('SD90_PARTA', channel=2, program=((99*128),103), volume=100)
tss_foot_main = cf >> KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('SD90_PARTA',channel=1,program=((98*128),53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('SD90_PARTA',channel=1,program=((98*128),53),volume=100,ctrls={91:75}))
analogkid_high = Output('SD90_PARTA', channel=2, program=((98*128),53), volume=100, ctrls={93:75, 91:100})
analogkid_main = cf >> KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending = cf >> Key('a1') >> Output('SD90_PARTA', channel=5, program=((81*128),68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight = cf >> Key('d#6') >> Output('SD90_PARTA', channel=16, program=((80*128),12), volume=100)

# Patch Centurion
centurion_synth = (Velocity(fixed=110) >> 
	(
		Output('SD90_PARTA', channel=1, program=((99*128),96), volume=110) // 
		Output('SD90_PARTA', channel=2, program=((99*128),82), volume=110)
	))

# Patch Centurion Video
centurion_video=( System('./vp.sh /mnt/flash/live/video/centurion_silent.avi') )

# Patch Centurion Hack 
centurion_patch=(cf >> LatchNotes(True,reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) // 
		(KeyFilter('E3') >> Key('D2')) // 
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> centurion_synth)

# PAD SECTION --------------------------------------------------------------------------------------------------

# Hack SD90_PARTA - Closer to the heart
closer_celesta_d4 =Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((98*128),11), volume=110)
#closer_celesta_d4 = (
#	(
#		Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((98*128),11), volume=110) //
#		(Velocity(fixed=100) >> Transpose(-72) >> Output('SD90_PARTA', channel=2, program=((99*128),96), volume=80))
#	))

closer_patch_celesta_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('A5')) //
    	(KeyFilter('D1') >> Key('B5')) //
    	(KeyFilter('E1') >> Key('G5')) //
    	(KeyFilter('F1') >> Key('D6')) //
    	(KeyFilter('G1') >> Key('F5')) //
    	(KeyFilter('A1') >> Key('C#6')) 
   ) >> closer_celesta_d4)

#closer_patch_celesta_d4=(cf >> 
#    (
#		(~KeyFilter(notes=[36,38,40,41,43,45])) //
#    	(KeyFilter('C1') >> Key('A5')) //
#    	(KeyFilter('D1') >> Key('G5')) //
#    	(KeyFilter('E1') >> Key('D6')) //
#    	(KeyFilter('F1') >> Key('F5')) //
#    	(KeyFilter('G1') >> Key('B5')) //
#    	(KeyFilter('A1') >> Key('C#6')) 
#   ) >> closer_celesta_d4)

closer_bell_d4 = Velocity(fixed=100) >> Output('SD90_PARTA', channel=1, program=((99*128),15), volume=100)
closer_patch_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('D4')) //
    	(KeyFilter('E1') >> Key('A3')) //
    	(KeyFilter('G1') >> Key('G3')) //
    	(KeyFilter('D1') >> Key('F#3')) 
   ) >> closer_bell_d4)

# YYZ
yyz_bell=Output('SD90_PARTA', channel=10, program=1, volume=100)
yyz=(cf >>
	(
		(KeyFilter('A1') >> Key('A4')) //
		(KeyFilter('F1') >> Key('G#4')) 
	) >> yyz_bell)

# Time Stand Steel
# Instruments
d4_melo_tom=Velocity(fixed=100) >> Output('SD90_PARTA', channel=11, program=((99*128)+1,118), volume=100)
d4_castanet=Velocity(fixed=100) >> Output('SD90_PARTA', channel=12, program=((99*128)+1,116), volume=100)
d4_808_tom=Velocity(fixed=80) >> Output('SD90_PARTA', channel=13, program=((99*128)+1,119), volume=100)

# Sons 1 et 2
tss_d4_melo_tom_A=cf >>KeyFilter('E1') >> Key('E6') >> d4_melo_tom

# Son 3
tss_d4_castanet=cf >>KeyFilter('G1') >> Key('a#2') >> d4_castanet

# Son 4
tss_d4_melo_tom_B=cf >>KeyFilter('F1') >> Key('a4') >> d4_808_tom

# Son 5
tss_d4_808_tom=cf >>KeyFilter('A1') >> Key('f#5') >> d4_808_tom

#--------------------------------------------
# SD-90 # DRUM MAPPING
#--------------------------------------------
# Classical Set
StandardSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,1))
RoomSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,9))
PowerSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,17))
ElectricSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,25))
AnalogSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,26))
JazzSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,33))
BrushSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,41))
OrchestraSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,49))
SFXSet=cf>>Output('SD90_PARTA',channel=10,program=(13312,57))
# Contemporary Set
StandardSet2=cf>>Output('SD90_PARTA',channel=10,program=(13440,1))
RoomSet2=cf>>Output('SD90_PARTA',channel=10,program=(13440,9))
PowerSet2=cf>>Output('SD90_PARTA',channel=10,program=(13440,17))
DanceSet=cf>>Output('SD90_PARTA',channel=10,program=(13440,25))
RaveSet=cf>>Output('SD90_PARTA',channel=10,program=(13440,26))
JazzSet2=cf>>Output('SD90_PARTA',channel=10,program=(13440,33))
BrushSet2=cf>>Output('SD90_PARTA',channel=10,program=(13440,41))
# Solo Set
St_Standard=cf>>Output('SD90_PARTA',channel=10,program=(13568,1))
St_Room=cf>>Output('SD90_PARTA',channel=10,program=(13568,9))
St_Power=cf>>Output('SD90_PARTA',channel=10,program=(13568,17))
RustSet=cf>>Output('SD90_PARTA',channel=10,program=(13568,25))
Analog2Set=cf>>Output('SD90_PARTA',channel=10,program=(13568,26))
St_Jazz=cf>>Output('SD90_PARTA',channel=10,program=(13568,33))
St_Brush=cf>>Output('SD90_PARTA',channel=10,program=(13568,41))
# Enhanced Set
Amb_Standard=cf>>Output('SD90_PARTA',channel=10,program=(13696,1))
Amb_Room=cf>>Output('SD90_PARTA',channel=10,program=(13696,9))
GatedPower=cf>>Output('SD90_PARTA',channel=10,program=(13696,17))
TechnoSet=cf>>Output('SD90_PARTA',channel=10,program=(13696,25))
BullySet=cf>>Output('SD90_PARTA',channel=10,program=(13696,26))
Amb_Jazz=cf>>Output('SD90_PARTA',channel=10,program=(13696,33))
Amb_Brush=cf>>Output('SD90_PARTA',channel=10,program=(13696,41))
#-------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Scenes region
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=InitSoundModule, patch=piano_base),
    # No impact filter to break all events
    2: Scene("Mp3PianoPlayer", Filter(SYSRT_RESET))
    #2: Scene("Mp3PianoPlayer", Pass())
}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
_pre  = Print('input', portnames='in')
_post = Print('output',portnames='out')

# TODO repenser ce token (fit pas avec le reste)
_ctrl=keyboard

run(
    control=_ctrl,
    scenes=_scenes, 
    #pre=_pre, 
    #post=_post,
)
