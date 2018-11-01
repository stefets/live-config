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

#stefets@rpi2:~/project/live-config$ aconnect -l
#client 0: 'System' [type=kernel]
#    0 'Timer           '
#    1 'Announce        '
#        Connecting To: 15:0
#client 14: 'Midi Through' [type=kernel]
#    0 'Midi Through Port-0'
#client 15: 'OSS sequencer' [type=kernel]
#    0 'Receiver        '
#        Connected From: 0:1
#client 20: 'SD-90' [type=kernel]
#    0 'SD-90 Part A    '
#    1 'SD-90 Part B    '
#    2 'SD-90 MIDI 1    '
#    3 'SD-90 MIDI 2    '
#client 24: 'Q49' [type=kernel]
#    0 'Q49 MIDI 1      '

    out_ports = [ 
        ('D4',  '20:0',),
        ('Q49', '20:0',),
        ('PK5', '20:0',),
        ('PODHD500', '20:2',), ],

    in_ports = [ 
        ('Q49  - MIDI IN 1', '24:0',), # Alesis Q49 in USB MODE
        ('SD90 - MIDI IN 1', '20:2',),
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
def SendSysex(ev):
    return SysExEvent(ev.port, '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')

# Scene navigation
def MoveNext(ev):
    switch_scene(current_scene()+1)

def NavigateToScene(ev):
    nb_scenes = len(scenes())    
    if ev.ctrl == 20:
        cs=current_scene()
        if ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs+1)
        elif ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
        elif ev.value == 3:
            css=current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css+1)
            else:
                switch_subscene(1)
    elif ev.ctrl == 22:
        # Reset logic
        subprocess.Popen(['/bin/bash', './kill.sh'])


#def init_pod(ev):
#    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    
# Audio and midi players
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
# CONFIGURATION SECTION
#-----------------------------------------------------------------------------------------------------------

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

# Reset logic (LIVE MODE)
# Controller pour le changement de scene (fcb1010 actual)
reset=Filter(CTRL) >> CtrlFilter(22) >> Process(SendSysex)
_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(20,22) >> Process(NavigateToScene)
#_control = Filter(NOTEON) >> KeyFilter(37) >> Process(MoveNext)

# Reset logic (DEBUG MODE)
#reset=Filter(NOTEOFF) >> Process(SendSysex)
#_control = ChannelFilter(1) >> Filter(CTRL) >> CtrlFilter(1) >> CtrlValueFilter(0) >> Call(gliss_exec)
#_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter([20,22]) >> Process(Glissando)
#_control = Filter(NOTE) >> Filter(NOTEON) >> Call(arpeggiator_exec)

# Channel 9 filter (my fcb1010 in my case)
cf=~ChannelFilter(9)

# Shortcut (Play switch)
PlayButton=Filter(NOTEOFF)	# for fast test
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)


#-----------------------------------------------------------------------------------------------------------
# PATCHES (token)
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# SCENES - (token)
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Reset",  reset),
__SCENES__
}

# ---------------------------
# MAIN
# ---------------------------
run(
    control=_control,
    #pre=_pre, 
    post=_post,
    scenes=_scenes, 
)
