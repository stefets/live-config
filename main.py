#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import subprocess
from threading import Timer
from time import sleep
from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.inotify import AutoRestart

config(

    backend = 'alsa',
    client_name = 'Master',

    out_ports = [ 
        ('Q49', '20:0',),					# Edirol SD-90 PART A
        ('PK5', '20:0',),					# Edirol SD-90 PART B available at 20:1
        ('D4',  '20:0',),
        ('PODHD500', '20:2',), ],

    in_ports = [ 
        ('Q49  - MIDI IN 1', '24:0',), 		# Alesis Q49 in USB MODE
        ('SD90 - MIDI IN 1', '20:2',),		# Edirol SD-90 has 2 MIDI IN 
        ('SD90 - MIDI IN 2', '20:3',) ],

    initial_scene = 1,
)

hook(
    #MemorizeScene('scene.txt'),
    #AutoRestart(),
)
#--------------------------------------------------------------------
# Class
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
# Test
def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev
#--------------------------------------------------------------------

# Glissando
def gliss_function(note, note_max, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    note += 1
    if note < note_max:
        Timer(.01, lambda: gliss_function(note, note_max, port, chan, vel)).start()

def gliss_exec(e):
    gliss_function(120, 168, e.port, e.channel, 100)

# Arpeggiator
def arpeggiator_function(current, max,note, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    current += 1
    if current < max:
        Timer(.15, lambda: arpeggiator_function(current, max, note,  port, chan, vel)).start()

def arpeggiator_exec(e):
    arpeggiator_function(0,16, 50,  e.port, e.channel, 100)

#-------------------------------------------------------------------------------------------

# Change the HEX string according to your sound module
# Reset string for Edirol SD-90
# Obsolete : Use the builin mididings function
#def SendSysex(ev):
#   return SysExEvent(ev.port, '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')

# Scene navigation
def MoveNext(ev):
    switch_scene(current_scene()+1)

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
#    elif ev.ctrl == 22:
#       # Reset logic
#       subprocess.Popen(['/bin/bash', './kill.sh'])


# Stop audio processing
def AllAudioOff(ev):
    return "/bin/bash ./kill.sh"

# Audio and midi players suitable for my SD-90
def play_file(filename):
    fname, fext = os.path.splitext(filename)
    path=" /home/shared/soundlib/"
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

#-----------------------------------------------------------------------------------------------------------
# 											CONFIGURATION SECTION
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# 											CONTROL SECTION


# This control have the same behavior than the NavigateToScene python function above
# EXCEPT that there is NO wrap parameter for SceneSwitch
# The NavigateToScene can wrap Scenets
#_control=(ChannelFilter(9) >> Filter(CTRL) >>
#	(
#		(CtrlFilter(20) >> CtrlValueFilter(1) >> SceneSwitch(offset=-1)) //
#		(CtrlFilter(20) >> CtrlValueFilter(2) >> SceneSwitch(offset=1))  //
#		(CtrlFilter(20) >> CtrlValueFilter(3) >> SubSceneSwitch(offset=1, wrap=True))
#	))

# Stop the audio and send the reset Sysex to the SD-90
reset=(System(AllAudioOff) // SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7'))

# Used by patches to exclude anything from channel 9
# Don't want Channel 9 interfere with anything
cf=~ChannelFilter(9) 	

# Configuring my controllers
fcb1010=(ChannelFilter(9) >> Filter(CTRL) >> 
	(
		(CtrlFilter(20) >> Process(NavigateToScene)) // 
		(CtrlFilter(22) >> reset)
		 
	))

keyboard = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(20,22) >> Process(NavigateToScene)

# 											CONTROL SECTION
#-----------------------------------------------------------------------------------------------------------


# Reset logic (DEBUG MODE)
#reset=Filter(NOTEOFF) >> Process(SendSysex)
#_control = ChannelFilter(1) >> Filter(CTRL) >> CtrlFilter(1) >> CtrlValueFilter(0) >> Call(gliss_exec)
#_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter([20,22]) >> Process(Glissando)
#_control = Filter(NOTE) >> Filter(NOTEON) >> Call(arpeggiator_exec)


# Shortcut (Play switch)
PlayButton=Filter(NOTEOFF)	# for fast test
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)

initialize=ChannelFilter(1)
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# 											PATCHES
__PATCHES__
# 											PATCHES
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# 											SCENES
_scenes = {
    1: Scene("Initialize",  initialize),
__SCENES__
}
# 											SCENES
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# 											MAIN
_pre  = Print('input', portnames='in')
_post = Print('output', portnames='out')
run(
    control=fcb1010,
    scenes=_scenes, 
    #pre=_pre, 
    #post=_post,
)
# 											MAIN
#-----------------------------------------------------------------------------------------------------------
