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
import sys
import json
sys.path.append(os.path.realpath('.'))
from mididings.extra import *
from mididings.extra.osc import *
from mididings import engine
#from mididings.extra.inotify import *
#from core.RangeKeyDict import  import ra
from plugins.mpg123.wrapper import *

# Global configuration file
with open('config.json') as json_file:
    configuration = json.load(json_file)

config(

    # Defaults
    # initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    out_ports = [
        # DAW
        ('SD90-PART-A', '20:0'),         # Edirol SD-90 PART A       (Port number 1)
        ('SD90-PART-B', '20:1'),         # Edirol SD-90 PART B       (Port number 2)
        ('SD90-MIDI-OUT-1', '20:2',),   # Edirol SD-90 MIDI OUT 1   (Port number 3)
        ('SD90-MIDI-OUT-2', '20:3',),   # Edirol SD-90 MIDI OUT 2   (Port number 4)
        ('UM2-MIDI-OUT-1', '24:0',),  # Edirol UM-2eX MIDI OUT 1   (Port number 4)
        ('UM2-MIDI-OUT-2', '24:1',),  # Edirol UM-2eX MIDI OUT 2   (Port number 4)

        # Clones
        ('HD500', '20:2',),     # MOVABLE
        # HD500 midi out to gt10b midi , if I output to gt10b, it goes thru pod anyway
        ('GT10B', '20:2',),     # MOVABLE
 ],

    in_ports = [
        ('Q49_MIDI_IN_1', '20:0',),  # Alesis Q49 in USB MODE
        ('UM2-MIDI-IN-1', '24:0',),  # Alesis Q49 in USB MODE

        ('SD90-MIDI-IN-1','20:2',),  # Edirol SD-90 MIDI IN 1
        ('SD90-MIDI-IN-2','20:3',)   # Edirol SD-90 MIDI IN 2
 ],

)

hook(

    #MemorizeScene('memorize-scene.txt'),
    #AutoRestart(), #AutoRestart works with mididings.extra.inotify

    #OSCInterface(port=56418, notify_ports=[56419,56420]),
    OSCInterface(),
)

#-----------------------------------------------------------------------------------------------------------
# Functions section 
# functions.py
# --------------------------------------------------------------------
# Function and classes called by scenes
# --------------------------------------------------------------------

#
# This class remove duplicate midi message by taking care of an offset logic
# NOT STABLE SUSPECT OVERFLOW 
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
        offset = now - self.prev_time
        if offset >= 0.035:
            # if ev.type == NOTEON:
            #    print "+ " + str(offset)
            r = ev
        else:
            # if ev.type == NOTEON:
            #    print "- " + str(offset)
            r = None
        self.prev_ev = ev
        self.prev_time = now
        return r


'''
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

'''


# -------------------------------------------------------------------------------------------


# Navigate through secenes and subscenes
def NavigateToScene(ev):
    # MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    # With that function, you can wrap trough Scenes AND SubScenes
    # That function assume that the first SceneNumber is 1
    # TODO field, values = dict(scenes()).items()[0]
    if ev.ctrl == 20:
        nb_scenes = len(scenes())
        cs = current_scene()
        # Scene backward
        if ev.value == 1:
            if cs > 1:
                switch_scene(cs - 1)
            # Scene forward and wrap
        elif ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs + 1)
            else:
                switch_scene(1)
            # SubScene backward
        elif ev.value == 3:
            css = current_subscene()
            if css > 1:
                switch_subscene(css - 1)
            # SubScene forward and wrap
        elif ev.value == 4:
            css = current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css + 1)
            else:
                switch_subscene(1)


# Stop any audio processing, managed by a simple bash script
def AllAudioOff(ev):
    return "/bin/bash ./kill.sh"


# Audio and midi players suitable for my SD-90
def play_file(filename):
    fname, fext = os.path.splitext(filename)
    if fext == ".mp3":
        path = " /tmp/soundlib/mp3/"
        command = "mpg123 -q"
    elif fext == ".mid":
        path = " /tmp/soundlib/midi/"
        command = "aplaymidi -p 20:1"

    return command + path + filename


# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64) * direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value * direction)

# ---------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Filters Section
# filters.py
#-----------------------------------------------------------------------------------------------------------
# # ALLOWED FILTERS : Available for patches, meaning, allow only for instance
q49 = ChannelFilter(1)  # Filter by hardware / channel
pk5 = ChannelFilter(2)  # Filter by hardware & channel
# fcb=ChannelFilter(9)
# hd500=ChannelFilter(9)
# # gt10b=ChannelFilter(16)

# Control Filter Channel (cf)
cf = ~ChannelFilter(9)

#-----------------------------------------------------------------------------------------------------------
# Hardware Section defined in /hardware/ directory
#-----------------------------------------------------------------------------------------------------------
# Edirol SD-90 Studio Canvas
#
# This is the patches specific for the sound modules configuration
#
# EDIROL SD-90
#
# Reset string
ResetSD90 = SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')

# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01 = (Ctrl(1, 1, 100, 0) // Ctrl(1, 1, 101, 0) // Ctrl(1, 1, 6, 12) // Ctrl(1, 1, 38, 0))
PB_A02 = (Ctrl(1, 2, 100, 0) // Ctrl(1, 2, 101, 0) // Ctrl(1, 2, 6, 12) // Ctrl(1, 2, 38, 0))
PB_A03 = (Ctrl(1, 3, 100, 0) // Ctrl(1, 3, 101, 0) // Ctrl(1, 3, 6, 12) // Ctrl(1, 3, 38, 0))
PB_A04 = (Ctrl(1, 4, 100, 0) // Ctrl(1, 4, 101, 0) // Ctrl(1, 4, 6, 12) // Ctrl(1, 4, 38, 0))
PB_A05 = (Ctrl(1, 5, 100, 0) // Ctrl(1, 5, 101, 0) // Ctrl(1, 5, 6, 12) // Ctrl(1, 5, 38, 0))
PB_A06 = (Ctrl(1, 6, 100, 0) // Ctrl(1, 6, 101, 0) // Ctrl(1, 6, 6, 12) // Ctrl(1, 6, 38, 0))
PB_A07 = (Ctrl(1, 7, 100, 0) // Ctrl(1, 7, 101, 0) // Ctrl(1, 7, 6, 12) // Ctrl(1, 7, 38, 0))
PB_A08 = (Ctrl(1, 8, 100, 0) // Ctrl(1, 8, 101, 0) // Ctrl(1, 8, 6, 12) // Ctrl(1, 8, 38, 0))
PB_A09 = (Ctrl(1, 9, 100, 0) // Ctrl(1, 9, 101, 0) // Ctrl(1, 9, 6, 12) // Ctrl(1, 9, 38, 0))
PB_A10 = (Ctrl(1, 10, 100, 0) // Ctrl(1, 10, 101, 0) // Ctrl(1, 10, 6, 12) // Ctrl(1, 10, 38, 0))
PB_A11 = (Ctrl(1, 11, 100, 0) // Ctrl(1, 11, 101, 0) // Ctrl(1, 11, 6, 12) // Ctrl(1, 11, 38, 0))
PB_A12 = (Ctrl(1, 12, 100, 0) // Ctrl(1, 12, 101, 0) // Ctrl(1, 12, 6, 12) // Ctrl(1, 12, 38, 0))
PB_A13 = (Ctrl(1, 13, 100, 0) // Ctrl(1, 13, 101, 0) // Ctrl(1, 13, 6, 12) // Ctrl(1, 13, 38, 0))
PB_A14 = (Ctrl(1, 14, 100, 0) // Ctrl(1, 14, 101, 0) // Ctrl(1, 14, 6, 12) // Ctrl(1, 14, 38, 0))
PB_A15 = (Ctrl(1, 15, 100, 0) // Ctrl(1, 15, 101, 0) // Ctrl(1, 15, 6, 12) // Ctrl(1, 15, 38, 0))
PB_A16 = (Ctrl(1, 16, 100, 0) // Ctrl(1, 16, 101, 0) // Ctrl(1, 16, 6, 12) // Ctrl(1, 16, 38, 0))
# SD-90 Part B - All Channel
PB_B01 = (Ctrl(2, 1, 100, 0) // Ctrl(2, 1, 101, 0) // Ctrl(2, 1, 6, 12) // Ctrl(2, 1, 38, 0))
PB_B02 = (Ctrl(2, 2, 100, 0) // Ctrl(2, 2, 101, 0) // Ctrl(2, 2, 6, 12) // Ctrl(2, 2, 38, 0))
PB_B03 = (Ctrl(2, 3, 100, 0) // Ctrl(2, 3, 101, 0) // Ctrl(2, 3, 6, 12) // Ctrl(2, 3, 38, 0))
PB_B04 = (Ctrl(2, 4, 100, 0) // Ctrl(2, 4, 101, 0) // Ctrl(2, 4, 6, 12) // Ctrl(2, 4, 38, 0))
PB_B05 = (Ctrl(2, 5, 100, 0) // Ctrl(2, 5, 101, 0) // Ctrl(2, 5, 6, 12) // Ctrl(2, 5, 38, 0))
PB_B06 = (Ctrl(2, 6, 100, 0) // Ctrl(2, 6, 101, 0) // Ctrl(2, 6, 6, 12) // Ctrl(2, 6, 38, 0))
PB_B07 = (Ctrl(2, 7, 100, 0) // Ctrl(2, 7, 101, 0) // Ctrl(2, 7, 6, 12) // Ctrl(2, 7, 38, 0))
PB_B08 = (Ctrl(2, 8, 100, 0) // Ctrl(2, 8, 101, 0) // Ctrl(2, 8, 6, 12) // Ctrl(2, 8, 38, 0))
PB_B09 = (Ctrl(2, 9, 100, 0) // Ctrl(2, 9, 101, 0) // Ctrl(2, 9, 6, 12) // Ctrl(2, 9, 38, 0))
PB_B10 = (Ctrl(2, 10, 100, 0) // Ctrl(2, 10, 101, 0) // Ctrl(2, 10, 6, 12) // Ctrl(2, 10, 38, 0))
PB_B11 = (Ctrl(2, 11, 100, 0) // Ctrl(2, 11, 101, 0) // Ctrl(2, 11, 6, 12) // Ctrl(2, 11, 38, 0))
PB_B12 = (Ctrl(2, 12, 100, 0) // Ctrl(2, 12, 101, 0) // Ctrl(2, 12, 6, 12) // Ctrl(2, 12, 38, 0))
PB_B13 = (Ctrl(2, 13, 100, 0) // Ctrl(2, 13, 101, 0) // Ctrl(2, 13, 6, 12) // Ctrl(2, 13, 38, 0))
PB_B14 = (Ctrl(2, 14, 100, 0) // Ctrl(2, 14, 101, 0) // Ctrl(2, 14, 6, 12) // Ctrl(2, 14, 38, 0))
PB_B15 = (Ctrl(2, 15, 100, 0) // Ctrl(2, 15, 101, 0) // Ctrl(2, 15, 6, 12) // Ctrl(2, 15, 38, 0))
PB_B16 = (Ctrl(2, 16, 100, 0) // Ctrl(2, 16, 101, 0) // Ctrl(2, 16, 6, 12) // Ctrl(2, 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------
# Classical Set
StandardSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 1))
RoomSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 9))
PowerSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 17))
ElectricSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 25))
AnalogSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 26))
JazzSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 33))
BrushSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 41))
OrchestraSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 49))
SFXSet = cf >> Output('SD90-PART-A', channel=10, program=(13312, 57))
# Contemporary Set
StandardSet2 = cf >> Output('SD90-PART-A', channel=10, program=(13440, 1))
RoomSet2 = cf >> Output('SD90-PART-A', channel=10, program=(13440, 9))
PowerSet2 = cf >> Output('SD90-PART-A', channel=10, program=(13440, 17))
DanceSet = cf >> Output('SD90-PART-A', channel=10, program=(13440, 25))
RaveSet = cf >> Output('SD90-PART-A', channel=10, program=(13440, 26))
JazzSet2 = cf >> Output('SD90-PART-A', channel=10, program=(13440, 33))
BrushSet2 = cf >> Output('SD90-PART-A', channel=10, program=(13440, 41))
# Solo Set
St_Standard = cf >> Output('SD90-PART-A', channel=10, program=(13568, 1))
St_Room = cf >> Output('SD90-PART-A', channel=10, program=(13568, 9))
St_Power = cf >> Output('SD90-PART-A', channel=10, program=(13568, 17))
RustSet = cf >> Output('SD90-PART-A', channel=10, program=(13568, 25))
Analog2Set = cf >> Output('SD90-PART-A', channel=10, program=(13568, 26))
St_Jazz = cf >> Output('SD90-PART-A', channel=10, program=(13568, 33))
St_Brush = cf >> Output('SD90-PART-A', channel=10, program=(13568, 41))
# Enhanced Set
Amb_Standard = cf >> Output('SD90-PART-A', channel=10, program=(13696, 1))
Amb_Room = cf >> Output('SD90-PART-A', channel=10, program=(13696, 9))
GatedPower = cf >> Output('SD90-PART-A', channel=10, program=(13696, 17))
TechnoSet = cf >> Output('SD90-PART-A', channel=10, program=(13696, 25))
BullySet = cf >> Output('SD90-PART-A', channel=10, program=(13696, 26))
Amb_Jazz = cf >> Output('SD90-PART-A', channel=10, program=(13696, 33))
Amb_Brush = cf >> Output('SD90-PART-A', channel=10, program=(13696, 41))

### SD-90 Full Patch implementation 
# TODO 
BrushingSaw = cf >> Output('SD90-PART-A', channel=1, program=((80 * 128), 2))
# TODO 
### End SD-90 Patch list
# -------------------------------------------------------------------

InitSoundModule = (ResetSD90 // InitPitchBend)

# HD500 configuration
#
# This is the patches specific for a certain device
#
# POD-HD-500
#

hd500_channel = configuration['HD500']['channel']
hd500_port = 3

P01A = Program(hd500_port, channel=hd500_channel, program=1)
P01B = Program(hd500_port, channel=hd500_channel, program=2)
P01C = Program(hd500_port, channel=hd500_channel, program=3)
P01D = Program(hd500_port, channel=hd500_channel, program=4)
P02A = Program(hd500_port, channel=hd500_channel, program=5)
P02B = Program(hd500_port, channel=hd500_channel, program=6)
P02C = Program(hd500_port, channel=hd500_channel, program=7)
P02D = Program(hd500_port, channel=hd500_channel, program=8)
P03A = Program(hd500_port, channel=hd500_channel, program=9)
P03B = Program(hd500_port, channel=hd500_channel, program=10)
P03C = Program(hd500_port, channel=hd500_channel, program=11)
P03D = Program(hd500_port, channel=hd500_channel, program=12)
P04A = Program(hd500_port, channel=hd500_channel, program=13)
P04B = Program(hd500_port, channel=hd500_channel, program=14)
P04C = Program(hd500_port, channel=hd500_channel, program=15)
P04D = Program(hd500_port, channel=hd500_channel, program=16)
P05A = Program(hd500_port, channel=hd500_channel, program=17)
P05B = Program(hd500_port, channel=hd500_channel, program=18)
P05C = Program(hd500_port, channel=hd500_channel, program=19)
P05D = Program(hd500_port, channel=hd500_channel, program=20)
P06A = Program(hd500_port, channel=hd500_channel, program=21)
P06B = Program(hd500_port, channel=hd500_channel, program=22)
P06C = Program(hd500_port, channel=hd500_channel, program=23)
P06D = Program(hd500_port, channel=hd500_channel, program=24)
P07A = Program(hd500_port, channel=hd500_channel, program=25)
P07B = Program(hd500_port, channel=hd500_channel, program=26)
P07C = Program(hd500_port, channel=hd500_channel, program=27)
P07D = Program(hd500_port, channel=hd500_channel, program=28)
P08A = Program(hd500_port, channel=hd500_channel, program=29)
P08B = Program(hd500_port, channel=hd500_channel, program=30)
P08C = Program(hd500_port, channel=hd500_channel, program=31)
P08D = Program(hd500_port, channel=hd500_channel, program=32)
P09A = Program(hd500_port, channel=hd500_channel, program=33)
P09B = Program(hd500_port, channel=hd500_channel, program=34)
P09C = Program(hd500_port, channel=hd500_channel, program=35)
P09D = Program(hd500_port, channel=hd500_channel, program=36)
P10A = Program(hd500_port, channel=hd500_channel, program=37)
P10B = Program(hd500_port, channel=hd500_channel, program=38)
P10C = Program(hd500_port, channel=hd500_channel, program=39)
P10D = Program(hd500_port, channel=hd500_channel, program=40)
P11A = Program(hd500_port, channel=hd500_channel, program=41)
P11B = Program(hd500_port, channel=hd500_channel, program=42)
P11C = Program(hd500_port, channel=hd500_channel, program=43)
P11D = Program(hd500_port, channel=hd500_channel, program=44)
P12A = Program(hd500_port, channel=hd500_channel, program=45)
P12B = Program(hd500_port, channel=hd500_channel, program=46)
P12C = Program(hd500_port, channel=hd500_channel, program=47)
P12D = Program(hd500_port, channel=hd500_channel, program=48)
P13A = Program(hd500_port, channel=hd500_channel, program=49)
P13B = Program(hd500_port, channel=hd500_channel, program=50)
P13C = Program(hd500_port, channel=hd500_channel, program=51)
P13D = Program(hd500_port, channel=hd500_channel, program=52)
P14A = Program(hd500_port, channel=hd500_channel, program=53)
P14B = Program(hd500_port, channel=hd500_channel, program=54)
P14C = Program(hd500_port, channel=hd500_channel, program=55)
P14D = Program(hd500_port, channel=hd500_channel, program=56)
P15A = Program(hd500_port, channel=hd500_channel, program=57)
P15B = Program(hd500_port, channel=hd500_channel, program=58)
P15C = Program(hd500_port, channel=hd500_channel, program=59)
P15D = Program(hd500_port, channel=hd500_channel, program=60)
P16A = Program(hd500_port, channel=hd500_channel, program=61)
P16B = Program(hd500_port, channel=hd500_channel, program=62)
P16C = Program(hd500_port, channel=hd500_channel, program=63)
P16D = Program(hd500_port, channel=hd500_channel, program=64)

#

#
# POD-HD-500 to control Fender Super60
#

# Depend on hd500.py
S60A = Program(hd500_port, channel=hd500_channel, program=61)
S60B = Program(hd500_port, channel=hd500_channel, program=62)
S60C = Program(hd500_port, channel=hd500_channel, program=63)
S60D = Program(hd500_port, channel=hd500_channel, program=64)

# hd500_port, Channel, CC, Value
# Footsiwtch
FS1 = Ctrl(hd500_port, hd500_channel, 51, 64)
FS2 = Ctrl(hd500_port, hd500_channel, 52, 64)
FS3 = Ctrl(hd500_port, hd500_channel, 53, 64)
FS4 = Ctrl(hd500_port, hd500_channel, 54, 64)
FS5 = Ctrl(hd500_port, hd500_channel, 55, 64)
FS6 = Ctrl(hd500_port, hd500_channel, 56, 64)
FS7 = Ctrl(hd500_port, hd500_channel, 57, 64)
FS8 = Ctrl(hd500_port, hd500_channel, 58, 64)
TOE = Ctrl(hd500_port, hd500_channel, 59, 64)

# Pedal - useless

# Looper

# GT10B configuration
#
# This is the patches specific for a certain device
#
# SD-90 CONFIGURATION TO CONTROL THE BOSS GT_10B
# 

# CONFIG

# Channel defined in the GT10B
GT10BChannel = configuration['GT10B']['channel']

# port number of the D
GT10BPort = 3

GT10B_volume = (ChannelFilter(9) >> Channel(16) >> CtrlFilter(1) >> CtrlMap(1, 7) >> Port(3))

# banks
GT10B_bank_0 = (Ctrl(GT10BPort, GT10BChannel, 0, 0) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_1 = (Ctrl(GT10BPort, GT10BChannel, 0, 1) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_2 = (Ctrl(GT10BPort, GT10BChannel, 0, 2) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_3 = (Ctrl(GT10BPort, GT10BChannel, 0, 3) // Ctrl(GT10BPort, GT10BChannel, 32, 0))

# program (same for the 4 banks)
GT10B_pgrm_1 = Program(GT10BPort, channel=GT10BChannel, program=1)
GT10B_pgrm_2 = Program(GT10BPort, channel=GT10BChannel, program=2)
GT10B_pgrm_3 = Program(GT10BPort, channel=GT10BChannel, program=3)
GT10B_pgrm_4 = Program(GT10BPort, channel=GT10BChannel, program=4)
GT10B_pgrm_5 = Program(GT10BPort, channel=GT10BChannel, program=5)
GT10B_pgrm_6 = Program(GT10BPort, channel=GT10BChannel, program=6)
GT10B_pgrm_7 = Program(GT10BPort, channel=GT10BChannel, program=7)
GT10B_pgrm_8 = Program(GT10BPort, channel=GT10BChannel, program=8)
GT10B_pgrm_9 = Program(GT10BPort, channel=GT10BChannel, program=9)
GT10B_pgrm_10 = Program(GT10BPort, channel=GT10BChannel, program=10)
GT10B_pgrm_11 = Program(GT10BPort, channel=GT10BChannel, program=11)
GT10B_pgrm_12 = Program(GT10BPort, channel=GT10BChannel, program=12)
GT10B_pgrm_13 = Program(GT10BPort, channel=GT10BChannel, program=13)
GT10B_pgrm_14 = Program(GT10BPort, channel=GT10BChannel, program=14)
GT10B_pgrm_15 = Program(GT10BPort, channel=GT10BChannel, program=15)
GT10B_pgrm_16 = Program(GT10BPort, channel=GT10BChannel, program=16)
GT10B_pgrm_17 = Program(GT10BPort, channel=GT10BChannel, program=17)
GT10B_pgrm_18 = Program(GT10BPort, channel=GT10BChannel, program=18)
GT10B_pgrm_19 = Program(GT10BPort, channel=GT10BChannel, program=19)
GT10B_pgrm_20 = Program(GT10BPort, channel=GT10BChannel, program=20)
GT10B_pgrm_21 = Program(GT10BPort, channel=GT10BChannel, program=21)
GT10B_pgrm_22 = Program(GT10BPort, channel=GT10BChannel, program=22)
GT10B_pgrm_23 = Program(GT10BPort, channel=GT10BChannel, program=23)
GT10B_pgrm_24 = Program(GT10BPort, channel=GT10BChannel, program=24)
GT10B_pgrm_25 = Program(GT10BPort, channel=GT10BChannel, program=25)
GT10B_pgrm_26 = Program(GT10BPort, channel=GT10BChannel, program=26)
GT10B_pgrm_27 = Program(GT10BPort, channel=GT10BChannel, program=27)
GT10B_pgrm_28 = Program(GT10BPort, channel=GT10BChannel, program=28)
GT10B_pgrm_29 = Program(GT10BPort, channel=GT10BChannel, program=29)
GT10B_pgrm_30 = Program(GT10BPort, channel=GT10BChannel, program=30)
GT10B_pgrm_31 = Program(GT10BPort, channel=GT10BChannel, program=31)
GT10B_pgrm_32 = Program(GT10BPort, channel=GT10BChannel, program=32)
GT10B_pgrm_33 = Program(GT10BPort, channel=GT10BChannel, program=33)
GT10B_pgrm_34 = Program(GT10BPort, channel=GT10BChannel, program=34)
GT10B_pgrm_35 = Program(GT10BPort, channel=GT10BChannel, program=35)
GT10B_pgrm_36 = Program(GT10BPort, channel=GT10BChannel, program=36)
GT10B_pgrm_37 = Program(GT10BPort, channel=GT10BChannel, program=37)
GT10B_pgrm_38 = Program(GT10BPort, channel=GT10BChannel, program=38)
GT10B_pgrm_39 = Program(GT10BPort, channel=GT10BChannel, program=39)
GT10B_pgrm_40 = Program(GT10BPort, channel=GT10BChannel, program=40)
GT10B_pgrm_41 = Program(GT10BPort, channel=GT10BChannel, program=41)
GT10B_pgrm_42 = Program(GT10BPort, channel=GT10BChannel, program=42)
GT10B_pgrm_43 = Program(GT10BPort, channel=GT10BChannel, program=43)
GT10B_pgrm_44 = Program(GT10BPort, channel=GT10BChannel, program=44)
GT10B_pgrm_45 = Program(GT10BPort, channel=GT10BChannel, program=45)
GT10B_pgrm_46 = Program(GT10BPort, channel=GT10BChannel, program=46)
GT10B_pgrm_47 = Program(GT10BPort, channel=GT10BChannel, program=47)
GT10B_pgrm_48 = Program(GT10BPort, channel=GT10BChannel, program=48)
GT10B_pgrm_49 = Program(GT10BPort, channel=GT10BChannel, program=49)
GT10B_pgrm_50 = Program(GT10BPort, channel=GT10BChannel, program=50)
GT10B_pgrm_51 = Program(GT10BPort, channel=GT10BChannel, program=51)
GT10B_pgrm_52 = Program(GT10BPort, channel=GT10BChannel, program=52)
GT10B_pgrm_53 = Program(GT10BPort, channel=GT10BChannel, program=53)
GT10B_pgrm_54 = Program(GT10BPort, channel=GT10BChannel, program=54)
GT10B_pgrm_55 = Program(GT10BPort, channel=GT10BChannel, program=55)
GT10B_pgrm_56 = Program(GT10BPort, channel=GT10BChannel, program=56)
GT10B_pgrm_57 = Program(GT10BPort, channel=GT10BChannel, program=57)
GT10B_pgrm_58 = Program(GT10BPort, channel=GT10BChannel, program=58)
GT10B_pgrm_59 = Program(GT10BPort, channel=GT10BChannel, program=59)
GT10B_pgrm_60 = Program(GT10BPort, channel=GT10BChannel, program=60)
GT10B_pgrm_61 = Program(GT10BPort, channel=GT10BChannel, program=61)
GT10B_pgrm_62 = Program(GT10BPort, channel=GT10BChannel, program=62)
GT10B_pgrm_63 = Program(GT10BPort, channel=GT10BChannel, program=63)
GT10B_pgrm_64 = Program(GT10BPort, channel=GT10BChannel, program=64)
GT10B_pgrm_65 = Program(GT10BPort, channel=GT10BChannel, program=65)
GT10B_pgrm_66 = Program(GT10BPort, channel=GT10BChannel, program=66)
GT10B_pgrm_67 = Program(GT10BPort, channel=GT10BChannel, program=67)
GT10B_pgrm_68 = Program(GT10BPort, channel=GT10BChannel, program=68)
GT10B_pgrm_69 = Program(GT10BPort, channel=GT10BChannel, program=69)
GT10B_pgrm_70 = Program(GT10BPort, channel=GT10BChannel, program=70)
GT10B_pgrm_71 = Program(GT10BPort, channel=GT10BChannel, program=71)
GT10B_pgrm_72 = Program(GT10BPort, channel=GT10BChannel, program=72)
GT10B_pgrm_73 = Program(GT10BPort, channel=GT10BChannel, program=73)
GT10B_pgrm_74 = Program(GT10BPort, channel=GT10BChannel, program=74)
GT10B_pgrm_75 = Program(GT10BPort, channel=GT10BChannel, program=75)
GT10B_pgrm_76 = Program(GT10BPort, channel=GT10BChannel, program=76)
GT10B_pgrm_77 = Program(GT10BPort, channel=GT10BChannel, program=77)
GT10B_pgrm_78 = Program(GT10BPort, channel=GT10BChannel, program=78)
GT10B_pgrm_79 = Program(GT10BPort, channel=GT10BChannel, program=79)
GT10B_pgrm_80 = Program(GT10BPort, channel=GT10BChannel, program=80)
GT10B_pgrm_81 = Program(GT10BPort, channel=GT10BChannel, program=81)
GT10B_pgrm_82 = Program(GT10BPort, channel=GT10BChannel, program=82)
GT10B_pgrm_83 = Program(GT10BPort, channel=GT10BChannel, program=83)
GT10B_pgrm_84 = Program(GT10BPort, channel=GT10BChannel, program=84)
GT10B_pgrm_85 = Program(GT10BPort, channel=GT10BChannel, program=85)
GT10B_pgrm_86 = Program(GT10BPort, channel=GT10BChannel, program=86)
GT10B_pgrm_87 = Program(GT10BPort, channel=GT10BChannel, program=87)
GT10B_pgrm_88 = Program(GT10BPort, channel=GT10BChannel, program=88)
GT10B_pgrm_89 = Program(GT10BPort, channel=GT10BChannel, program=89)
GT10B_pgrm_90 = Program(GT10BPort, channel=GT10BChannel, program=90)
GT10B_pgrm_91 = Program(GT10BPort, channel=GT10BChannel, program=91)
GT10B_pgrm_92 = Program(GT10BPort, channel=GT10BChannel, program=92)
GT10B_pgrm_93 = Program(GT10BPort, channel=GT10BChannel, program=93)
GT10B_pgrm_94 = Program(GT10BPort, channel=GT10BChannel, program=94)
GT10B_pgrm_95 = Program(GT10BPort, channel=GT10BChannel, program=95)
GT10B_pgrm_96 = Program(GT10BPort, channel=GT10BChannel, program=96)
GT10B_pgrm_97 = Program(GT10BPort, channel=GT10BChannel, program=97)
GT10B_pgrm_98 = Program(GT10BPort, channel=GT10BChannel, program=98)
GT10B_pgrm_99 = Program(GT10BPort, channel=GT10BChannel, program=99)
GT10B_pgrm_100 = Program(GT10BPort, channel=GT10BChannel, program=100)

# GT10B_bank 0
U01_A = (GT10B_bank_0 // GT10B_pgrm_1)
U01_B = (GT10B_bank_0 // GT10B_pgrm_2)
U01_C = (GT10B_bank_0 // GT10B_pgrm_3)
U01_D = (GT10B_bank_0 // GT10B_pgrm_4)
U02_A = (GT10B_bank_0 // GT10B_pgrm_5)
U02_B = (GT10B_bank_0 // GT10B_pgrm_6)
U02_C = (GT10B_bank_0 // GT10B_pgrm_7)
U02_D = (GT10B_bank_0 // GT10B_pgrm_8)
U03_A = (GT10B_bank_0 // GT10B_pgrm_9)
U03_B = (GT10B_bank_0 // GT10B_pgrm_10)
U03_C = (GT10B_bank_0 // GT10B_pgrm_11)
U03_D = (GT10B_bank_0 // GT10B_pgrm_12)
U04_A = (GT10B_bank_0 // GT10B_pgrm_13)
U04_B = (GT10B_bank_0 // GT10B_pgrm_14)
U04_C = (GT10B_bank_0 // GT10B_pgrm_15)
U04_D = (GT10B_bank_0 // GT10B_pgrm_16)
U05_A = (GT10B_bank_0 // GT10B_pgrm_17)
U05_B = (GT10B_bank_0 // GT10B_pgrm_18)
U05_C = (GT10B_bank_0 // GT10B_pgrm_19)
U05_D = (GT10B_bank_0 // GT10B_pgrm_20)
U06_A = (GT10B_bank_0 // GT10B_pgrm_21)
U06_B = (GT10B_bank_0 // GT10B_pgrm_22)
U06_C = (GT10B_bank_0 // GT10B_pgrm_23)
U06_D = (GT10B_bank_0 // GT10B_pgrm_24)
U07_A = (GT10B_bank_0 // GT10B_pgrm_25)
U07_B = (GT10B_bank_0 // GT10B_pgrm_26)
U07_C = (GT10B_bank_0 // GT10B_pgrm_27)
U07_D = (GT10B_bank_0 // GT10B_pgrm_28)
U08_A = (GT10B_bank_0 // GT10B_pgrm_29)
U08_B = (GT10B_bank_0 // GT10B_pgrm_30)
U08_C = (GT10B_bank_0 // GT10B_pgrm_31)
U08_D = (GT10B_bank_0 // GT10B_pgrm_32)
U09_A = (GT10B_bank_0 // GT10B_pgrm_33)
U09_B = (GT10B_bank_0 // GT10B_pgrm_34)
U09_C = (GT10B_bank_0 // GT10B_pgrm_35)
U09_D = (GT10B_bank_0 // GT10B_pgrm_36)
U10_A = (GT10B_bank_0 // GT10B_pgrm_37)
U10_B = (GT10B_bank_0 // GT10B_pgrm_38)
U10_C = (GT10B_bank_0 // GT10B_pgrm_39)
U10_D = (GT10B_bank_0 // GT10B_pgrm_40)
U11_A = (GT10B_bank_0 // GT10B_pgrm_41)
U11_B = (GT10B_bank_0 // GT10B_pgrm_42)
U11_C = (GT10B_bank_0 // GT10B_pgrm_43)
U11_D = (GT10B_bank_0 // GT10B_pgrm_44)
U12_A = (GT10B_bank_0 // GT10B_pgrm_45)
U12_B = (GT10B_bank_0 // GT10B_pgrm_46)
U12_C = (GT10B_bank_0 // GT10B_pgrm_47)
U12_D = (GT10B_bank_0 // GT10B_pgrm_48)
U13_A = (GT10B_bank_0 // GT10B_pgrm_49)
U13_B = (GT10B_bank_0 // GT10B_pgrm_50)
U13_C = (GT10B_bank_0 // GT10B_pgrm_51)
U13_D = (GT10B_bank_0 // GT10B_pgrm_52)
U14_A = (GT10B_bank_0 // GT10B_pgrm_53)
U14_B = (GT10B_bank_0 // GT10B_pgrm_54)
U14_C = (GT10B_bank_0 // GT10B_pgrm_55)
U14_D = (GT10B_bank_0 // GT10B_pgrm_56)
U15_A = (GT10B_bank_0 // GT10B_pgrm_57)
U15_B = (GT10B_bank_0 // GT10B_pgrm_58)
U15_C = (GT10B_bank_0 // GT10B_pgrm_59)
U15_D = (GT10B_bank_0 // GT10B_pgrm_60)
U16_A = (GT10B_bank_0 // GT10B_pgrm_61)
U16_B = (GT10B_bank_0 // GT10B_pgrm_62)
U16_C = (GT10B_bank_0 // GT10B_pgrm_63)
U16_D = (GT10B_bank_0 // GT10B_pgrm_64)
U17_A = (GT10B_bank_0 // GT10B_pgrm_65)
U17_B = (GT10B_bank_0 // GT10B_pgrm_66)
U17_C = (GT10B_bank_0 // GT10B_pgrm_67)
U17_D = (GT10B_bank_0 // GT10B_pgrm_68)
U18_A = (GT10B_bank_0 // GT10B_pgrm_69)
U18_B = (GT10B_bank_0 // GT10B_pgrm_70)
U18_C = (GT10B_bank_0 // GT10B_pgrm_71)
U18_D = (GT10B_bank_0 // GT10B_pgrm_72)
U19_A = (GT10B_bank_0 // GT10B_pgrm_73)
U19_B = (GT10B_bank_0 // GT10B_pgrm_74)
U19_C = (GT10B_bank_0 // GT10B_pgrm_75)
U19_D = (GT10B_bank_0 // GT10B_pgrm_76)
U20_A = (GT10B_bank_0 // GT10B_pgrm_77)
U20_B = (GT10B_bank_0 // GT10B_pgrm_78)
U20_C = (GT10B_bank_0 // GT10B_pgrm_79)
U20_D = (GT10B_bank_0 // GT10B_pgrm_80)
U21_A = (GT10B_bank_0 // GT10B_pgrm_81)
U21_B = (GT10B_bank_0 // GT10B_pgrm_82)
U21_C = (GT10B_bank_0 // GT10B_pgrm_83)
U21_D = (GT10B_bank_0 // GT10B_pgrm_84)
U22_A = (GT10B_bank_0 // GT10B_pgrm_85)
U22_B = (GT10B_bank_0 // GT10B_pgrm_86)
U22_C = (GT10B_bank_0 // GT10B_pgrm_87)
U22_D = (GT10B_bank_0 // GT10B_pgrm_88)
U23_A = (GT10B_bank_0 // GT10B_pgrm_89)
U23_B = (GT10B_bank_0 // GT10B_pgrm_90)
U23_C = (GT10B_bank_0 // GT10B_pgrm_91)
U23_D = (GT10B_bank_0 // GT10B_pgrm_92)
U24_A = (GT10B_bank_0 // GT10B_pgrm_93)
U24_B = (GT10B_bank_0 // GT10B_pgrm_94)
U24_C = (GT10B_bank_0 // GT10B_pgrm_95)
U24_D = (GT10B_bank_0 // GT10B_pgrm_96)
U25_A = (GT10B_bank_0 // GT10B_pgrm_97)
U25_B = (GT10B_bank_0 // GT10B_pgrm_98)
U25_C = (GT10B_bank_0 // GT10B_pgrm_99)
U25_D = (GT10B_bank_0 // GT10B_pgrm_100)

# GT10B_bank 1
U26_A = (GT10B_bank_1 // GT10B_pgrm_1)
U26_B = (GT10B_bank_1 // GT10B_pgrm_2)
U26_C = (GT10B_bank_1 // GT10B_pgrm_3)
U26_D = (GT10B_bank_1 // GT10B_pgrm_4)
U27_A = (GT10B_bank_1 // GT10B_pgrm_5)
U27_B = (GT10B_bank_1 // GT10B_pgrm_6)
U27_C = (GT10B_bank_1 // GT10B_pgrm_7)
U27_D = (GT10B_bank_1 // GT10B_pgrm_8)
U28_A = (GT10B_bank_1 // GT10B_pgrm_9)
U28_B = (GT10B_bank_1 // GT10B_pgrm_10)
U28_C = (GT10B_bank_1 // GT10B_pgrm_11)
U28_D = (GT10B_bank_1 // GT10B_pgrm_12)
U29_A = (GT10B_bank_1 // GT10B_pgrm_13)
U29_B = (GT10B_bank_1 // GT10B_pgrm_14)
U29_C = (GT10B_bank_1 // GT10B_pgrm_15)
U29_D = (GT10B_bank_1 // GT10B_pgrm_16)
U30_A = (GT10B_bank_1 // GT10B_pgrm_17)
U30_B = (GT10B_bank_1 // GT10B_pgrm_18)
U30_C = (GT10B_bank_1 // GT10B_pgrm_19)
U30_D = (GT10B_bank_1 // GT10B_pgrm_20)
U31_A = (GT10B_bank_1 // GT10B_pgrm_21)
U31_B = (GT10B_bank_1 // GT10B_pgrm_22)
U31_C = (GT10B_bank_1 // GT10B_pgrm_23)
U31_D = (GT10B_bank_1 // GT10B_pgrm_24)
U32_A = (GT10B_bank_1 // GT10B_pgrm_25)
U32_B = (GT10B_bank_1 // GT10B_pgrm_26)
U32_C = (GT10B_bank_1 // GT10B_pgrm_27)
U32_D = (GT10B_bank_1 // GT10B_pgrm_28)
U33_A = (GT10B_bank_1 // GT10B_pgrm_29)
U33_B = (GT10B_bank_1 // GT10B_pgrm_30)
U33_C = (GT10B_bank_1 // GT10B_pgrm_31)
U33_D = (GT10B_bank_1 // GT10B_pgrm_32)
U34_A = (GT10B_bank_1 // GT10B_pgrm_33)
U34_B = (GT10B_bank_1 // GT10B_pgrm_34)
U34_C = (GT10B_bank_1 // GT10B_pgrm_35)
U34_D = (GT10B_bank_1 // GT10B_pgrm_36)
U35_A = (GT10B_bank_1 // GT10B_pgrm_37)
U35_B = (GT10B_bank_1 // GT10B_pgrm_38)
U35_C = (GT10B_bank_1 // GT10B_pgrm_39)
U35_D = (GT10B_bank_1 // GT10B_pgrm_40)
U36_A = (GT10B_bank_1 // GT10B_pgrm_41)
U36_B = (GT10B_bank_1 // GT10B_pgrm_42)
U36_C = (GT10B_bank_1 // GT10B_pgrm_43)
U36_D = (GT10B_bank_1 // GT10B_pgrm_44)
U37_A = (GT10B_bank_1 // GT10B_pgrm_45)
U37_B = (GT10B_bank_1 // GT10B_pgrm_46)
U37_C = (GT10B_bank_1 // GT10B_pgrm_47)
U37_D = (GT10B_bank_1 // GT10B_pgrm_48)
U38_A = (GT10B_bank_1 // GT10B_pgrm_49)
U38_B = (GT10B_bank_1 // GT10B_pgrm_50)
U38_C = (GT10B_bank_1 // GT10B_pgrm_51)
U38_D = (GT10B_bank_1 // GT10B_pgrm_52)
U39_A = (GT10B_bank_1 // GT10B_pgrm_53)
U39_B = (GT10B_bank_1 // GT10B_pgrm_54)
U39_C = (GT10B_bank_1 // GT10B_pgrm_55)
U39_D = (GT10B_bank_1 // GT10B_pgrm_56)
U40_A = (GT10B_bank_1 // GT10B_pgrm_57)
U40_B = (GT10B_bank_1 // GT10B_pgrm_58)
U40_C = (GT10B_bank_1 // GT10B_pgrm_59)
U40_D = (GT10B_bank_1 // GT10B_pgrm_60)
U41_A = (GT10B_bank_1 // GT10B_pgrm_61)
U41_B = (GT10B_bank_1 // GT10B_pgrm_62)
U41_C = (GT10B_bank_1 // GT10B_pgrm_63)
U41_D = (GT10B_bank_1 // GT10B_pgrm_64)
U42_A = (GT10B_bank_1 // GT10B_pgrm_65)
U42_B = (GT10B_bank_1 // GT10B_pgrm_66)
U42_C = (GT10B_bank_1 // GT10B_pgrm_67)
U42_D = (GT10B_bank_1 // GT10B_pgrm_68)
U43_A = (GT10B_bank_1 // GT10B_pgrm_69)
U43_B = (GT10B_bank_1 // GT10B_pgrm_70)
U43_C = (GT10B_bank_1 // GT10B_pgrm_71)
U43_D = (GT10B_bank_1 // GT10B_pgrm_72)
U44_A = (GT10B_bank_1 // GT10B_pgrm_73)
U44_B = (GT10B_bank_1 // GT10B_pgrm_74)
U44_C = (GT10B_bank_1 // GT10B_pgrm_75)
U44_D = (GT10B_bank_1 // GT10B_pgrm_76)
U45_A = (GT10B_bank_1 // GT10B_pgrm_77)
U45_B = (GT10B_bank_1 // GT10B_pgrm_78)
U45_C = (GT10B_bank_1 // GT10B_pgrm_79)
U45_D = (GT10B_bank_1 // GT10B_pgrm_80)
U46_A = (GT10B_bank_1 // GT10B_pgrm_81)
U46_B = (GT10B_bank_1 // GT10B_pgrm_82)
U46_C = (GT10B_bank_1 // GT10B_pgrm_83)
U46_D = (GT10B_bank_1 // GT10B_pgrm_84)
U47_A = (GT10B_bank_1 // GT10B_pgrm_85)
U47_B = (GT10B_bank_1 // GT10B_pgrm_86)
U47_C = (GT10B_bank_1 // GT10B_pgrm_87)
U47_D = (GT10B_bank_1 // GT10B_pgrm_88)
U48_A = (GT10B_bank_1 // GT10B_pgrm_89)
U48_B = (GT10B_bank_1 // GT10B_pgrm_90)
U48_C = (GT10B_bank_1 // GT10B_pgrm_91)
U48_D = (GT10B_bank_1 // GT10B_pgrm_92)
U49_A = (GT10B_bank_1 // GT10B_pgrm_93)
U49_B = (GT10B_bank_1 // GT10B_pgrm_94)
U49_C = (GT10B_bank_1 // GT10B_pgrm_95)
U49_D = (GT10B_bank_1 // GT10B_pgrm_96)
U50_A = (GT10B_bank_1 // GT10B_pgrm_97)
U50_B = (GT10B_bank_1 // GT10B_pgrm_98)
U50_C = (GT10B_bank_1 // GT10B_pgrm_99)
U50_D = (GT10B_bank_1 // GT10B_pgrm_100)

# GT10B_bank 2
P01_A = (GT10B_bank_2 // GT10B_pgrm_1)
P01_B = (GT10B_bank_2 // GT10B_pgrm_2)
P01_C = (GT10B_bank_2 // GT10B_pgrm_3)
P01_D = (GT10B_bank_2 // GT10B_pgrm_4)
P02_A = (GT10B_bank_2 // GT10B_pgrm_5)
P02_B = (GT10B_bank_2 // GT10B_pgrm_6)
P02_C = (GT10B_bank_2 // GT10B_pgrm_7)
P02_D = (GT10B_bank_2 // GT10B_pgrm_8)
P03_A = (GT10B_bank_2 // GT10B_pgrm_9)
P03_B = (GT10B_bank_2 // GT10B_pgrm_10)
P03_C = (GT10B_bank_2 // GT10B_pgrm_11)
P03_D = (GT10B_bank_2 // GT10B_pgrm_12)
P04_A = (GT10B_bank_2 // GT10B_pgrm_13)
P04_B = (GT10B_bank_2 // GT10B_pgrm_14)
P04_C = (GT10B_bank_2 // GT10B_pgrm_15)
P04_D = (GT10B_bank_2 // GT10B_pgrm_16)
P05_A = (GT10B_bank_2 // GT10B_pgrm_17)
P05_B = (GT10B_bank_2 // GT10B_pgrm_18)
P05_C = (GT10B_bank_2 // GT10B_pgrm_19)
P05_D = (GT10B_bank_2 // GT10B_pgrm_20)
P06_A = (GT10B_bank_2 // GT10B_pgrm_21)
P06_B = (GT10B_bank_2 // GT10B_pgrm_22)
P06_C = (GT10B_bank_2 // GT10B_pgrm_23)
P06_D = (GT10B_bank_2 // GT10B_pgrm_24)
P07_A = (GT10B_bank_2 // GT10B_pgrm_25)
P07_B = (GT10B_bank_2 // GT10B_pgrm_26)
P07_C = (GT10B_bank_2 // GT10B_pgrm_27)
P07_D = (GT10B_bank_2 // GT10B_pgrm_28)
P08_A = (GT10B_bank_2 // GT10B_pgrm_29)
P08_B = (GT10B_bank_2 // GT10B_pgrm_30)
P08_C = (GT10B_bank_2 // GT10B_pgrm_31)
P08_D = (GT10B_bank_2 // GT10B_pgrm_32)
P09_A = (GT10B_bank_2 // GT10B_pgrm_33)
P09_B = (GT10B_bank_2 // GT10B_pgrm_34)
P09_C = (GT10B_bank_2 // GT10B_pgrm_35)
P09_D = (GT10B_bank_2 // GT10B_pgrm_36)
P10_A = (GT10B_bank_2 // GT10B_pgrm_37)
P10_B = (GT10B_bank_2 // GT10B_pgrm_38)
P10_C = (GT10B_bank_2 // GT10B_pgrm_39)
P10_D = (GT10B_bank_2 // GT10B_pgrm_40)
P11_A = (GT10B_bank_2 // GT10B_pgrm_41)
P11_B = (GT10B_bank_2 // GT10B_pgrm_42)
P11_C = (GT10B_bank_2 // GT10B_pgrm_43)
P11_D = (GT10B_bank_2 // GT10B_pgrm_44)
P12_A = (GT10B_bank_2 // GT10B_pgrm_45)
P12_B = (GT10B_bank_2 // GT10B_pgrm_46)
P12_C = (GT10B_bank_2 // GT10B_pgrm_47)
P12_D = (GT10B_bank_2 // GT10B_pgrm_48)
P13_A = (GT10B_bank_2 // GT10B_pgrm_49)
P13_B = (GT10B_bank_2 // GT10B_pgrm_50)
P13_C = (GT10B_bank_2 // GT10B_pgrm_51)
P13_D = (GT10B_bank_2 // GT10B_pgrm_52)
P14_A = (GT10B_bank_2 // GT10B_pgrm_53)
P14_B = (GT10B_bank_2 // GT10B_pgrm_54)
P14_C = (GT10B_bank_2 // GT10B_pgrm_55)
P14_D = (GT10B_bank_2 // GT10B_pgrm_56)
P15_A = (GT10B_bank_2 // GT10B_pgrm_57)
P15_B = (GT10B_bank_2 // GT10B_pgrm_58)
P15_C = (GT10B_bank_2 // GT10B_pgrm_59)
P15_D = (GT10B_bank_2 // GT10B_pgrm_60)
P16_A = (GT10B_bank_2 // GT10B_pgrm_61)
P16_B = (GT10B_bank_2 // GT10B_pgrm_62)
P16_C = (GT10B_bank_2 // GT10B_pgrm_63)
P16_D = (GT10B_bank_2 // GT10B_pgrm_64)
P17_A = (GT10B_bank_2 // GT10B_pgrm_65)
P17_B = (GT10B_bank_2 // GT10B_pgrm_66)
P17_C = (GT10B_bank_2 // GT10B_pgrm_67)
P17_D = (GT10B_bank_2 // GT10B_pgrm_68)
P18_A = (GT10B_bank_2 // GT10B_pgrm_69)
P18_B = (GT10B_bank_2 // GT10B_pgrm_70)
P18_C = (GT10B_bank_2 // GT10B_pgrm_71)
P18_D = (GT10B_bank_2 // GT10B_pgrm_72)
P19_A = (GT10B_bank_2 // GT10B_pgrm_73)
P19_B = (GT10B_bank_2 // GT10B_pgrm_74)
P19_C = (GT10B_bank_2 // GT10B_pgrm_75)
P19_D = (GT10B_bank_2 // GT10B_pgrm_76)
P20_A = (GT10B_bank_2 // GT10B_pgrm_77)
P20_B = (GT10B_bank_2 // GT10B_pgrm_78)
P20_C = (GT10B_bank_2 // GT10B_pgrm_79)
P20_D = (GT10B_bank_2 // GT10B_pgrm_80)
P21_A = (GT10B_bank_2 // GT10B_pgrm_81)
P21_B = (GT10B_bank_2 // GT10B_pgrm_82)
P21_C = (GT10B_bank_2 // GT10B_pgrm_83)
P21_D = (GT10B_bank_2 // GT10B_pgrm_84)
P22_A = (GT10B_bank_2 // GT10B_pgrm_85)
P22_B = (GT10B_bank_2 // GT10B_pgrm_86)
P22_C = (GT10B_bank_2 // GT10B_pgrm_87)
P22_D = (GT10B_bank_2 // GT10B_pgrm_88)
P23_A = (GT10B_bank_2 // GT10B_pgrm_89)
P23_B = (GT10B_bank_2 // GT10B_pgrm_90)
P23_C = (GT10B_bank_2 // GT10B_pgrm_91)
P23_D = (GT10B_bank_2 // GT10B_pgrm_92)
P24_A = (GT10B_bank_2 // GT10B_pgrm_93)
P24_B = (GT10B_bank_2 // GT10B_pgrm_94)
P24_C = (GT10B_bank_2 // GT10B_pgrm_95)
P24_D = (GT10B_bank_2 // GT10B_pgrm_96)
P25_A = (GT10B_bank_2 // GT10B_pgrm_97)
P25_B = (GT10B_bank_2 // GT10B_pgrm_98)
P25_C = (GT10B_bank_2 // GT10B_pgrm_99)
P25_D = (GT10B_bank_2 // GT10B_pgrm_100)
# GT10B_bank 3
P26_A = (GT10B_bank_3 // GT10B_pgrm_1)
P26_B = (GT10B_bank_3 // GT10B_pgrm_2)
P26_C = (GT10B_bank_3 // GT10B_pgrm_3)
P26_D = (GT10B_bank_3 // GT10B_pgrm_4)
P27_A = (GT10B_bank_3 // GT10B_pgrm_5)
P27_B = (GT10B_bank_3 // GT10B_pgrm_6)
P27_C = (GT10B_bank_3 // GT10B_pgrm_7)
P27_D = (GT10B_bank_3 // GT10B_pgrm_8)
P28_A = (GT10B_bank_3 // GT10B_pgrm_9)
P28_B = (GT10B_bank_3 // GT10B_pgrm_10)
P28_C = (GT10B_bank_3 // GT10B_pgrm_11)
P28_D = (GT10B_bank_3 // GT10B_pgrm_12)
P29_A = (GT10B_bank_3 // GT10B_pgrm_13)
P29_B = (GT10B_bank_3 // GT10B_pgrm_14)
P29_C = (GT10B_bank_3 // GT10B_pgrm_15)
P29_D = (GT10B_bank_3 // GT10B_pgrm_16)
P30_A = (GT10B_bank_3 // GT10B_pgrm_17)
P30_B = (GT10B_bank_3 // GT10B_pgrm_18)
P30_C = (GT10B_bank_3 // GT10B_pgrm_19)
P30_D = (GT10B_bank_3 // GT10B_pgrm_20)
P31_A = (GT10B_bank_3 // GT10B_pgrm_21)
P31_B = (GT10B_bank_3 // GT10B_pgrm_22)
P31_C = (GT10B_bank_3 // GT10B_pgrm_23)
P31_D = (GT10B_bank_3 // GT10B_pgrm_24)
P32_A = (GT10B_bank_3 // GT10B_pgrm_25)
P32_B = (GT10B_bank_3 // GT10B_pgrm_26)
P32_C = (GT10B_bank_3 // GT10B_pgrm_27)
P32_D = (GT10B_bank_3 // GT10B_pgrm_28)
P33_A = (GT10B_bank_3 // GT10B_pgrm_29)
P33_B = (GT10B_bank_3 // GT10B_pgrm_30)
P33_C = (GT10B_bank_3 // GT10B_pgrm_31)
P33_D = (GT10B_bank_3 // GT10B_pgrm_32)
P34_A = (GT10B_bank_3 // GT10B_pgrm_33)
P34_B = (GT10B_bank_3 // GT10B_pgrm_34)
P34_C = (GT10B_bank_3 // GT10B_pgrm_35)
P34_D = (GT10B_bank_3 // GT10B_pgrm_36)
P35_A = (GT10B_bank_3 // GT10B_pgrm_37)
P35_B = (GT10B_bank_3 // GT10B_pgrm_38)
P35_C = (GT10B_bank_3 // GT10B_pgrm_39)
P35_D = (GT10B_bank_3 // GT10B_pgrm_40)
P36_A = (GT10B_bank_3 // GT10B_pgrm_41)
P36_B = (GT10B_bank_3 // GT10B_pgrm_42)
P36_C = (GT10B_bank_3 // GT10B_pgrm_43)
P36_D = (GT10B_bank_3 // GT10B_pgrm_44)
P37_A = (GT10B_bank_3 // GT10B_pgrm_45)
P37_B = (GT10B_bank_3 // GT10B_pgrm_46)
P37_C = (GT10B_bank_3 // GT10B_pgrm_47)
P37_D = (GT10B_bank_3 // GT10B_pgrm_48)
P38_A = (GT10B_bank_3 // GT10B_pgrm_49)
P38_B = (GT10B_bank_3 // GT10B_pgrm_50)
P38_C = (GT10B_bank_3 // GT10B_pgrm_51)
P38_D = (GT10B_bank_3 // GT10B_pgrm_52)
P39_A = (GT10B_bank_3 // GT10B_pgrm_53)
P39_B = (GT10B_bank_3 // GT10B_pgrm_54)
P39_C = (GT10B_bank_3 // GT10B_pgrm_55)
P39_D = (GT10B_bank_3 // GT10B_pgrm_56)
P40_A = (GT10B_bank_3 // GT10B_pgrm_57)
P40_B = (GT10B_bank_3 // GT10B_pgrm_58)
P40_C = (GT10B_bank_3 // GT10B_pgrm_59)
P40_D = (GT10B_bank_3 // GT10B_pgrm_60)
P41_A = (GT10B_bank_3 // GT10B_pgrm_61)
P41_B = (GT10B_bank_3 // GT10B_pgrm_62)
P41_C = (GT10B_bank_3 // GT10B_pgrm_63)
P41_D = (GT10B_bank_3 // GT10B_pgrm_64)
P42_A = (GT10B_bank_3 // GT10B_pgrm_65)
P42_B = (GT10B_bank_3 // GT10B_pgrm_66)
P42_C = (GT10B_bank_3 // GT10B_pgrm_67)
P42_D = (GT10B_bank_3 // GT10B_pgrm_68)
P43_A = (GT10B_bank_3 // GT10B_pgrm_69)
P43_B = (GT10B_bank_3 // GT10B_pgrm_70)
P43_C = (GT10B_bank_3 // GT10B_pgrm_71)
P43_D = (GT10B_bank_3 // GT10B_pgrm_72)
P44_A = (GT10B_bank_3 // GT10B_pgrm_73)
P44_B = (GT10B_bank_3 // GT10B_pgrm_74)
P44_C = (GT10B_bank_3 // GT10B_pgrm_75)
P44_D = (GT10B_bank_3 // GT10B_pgrm_76)
P45_A = (GT10B_bank_3 // GT10B_pgrm_77)
P45_B = (GT10B_bank_3 // GT10B_pgrm_78)
P45_C = (GT10B_bank_3 // GT10B_pgrm_79)
P45_D = (GT10B_bank_3 // GT10B_pgrm_80)
P46_A = (GT10B_bank_3 // GT10B_pgrm_81)
P46_B = (GT10B_bank_3 // GT10B_pgrm_82)
P46_C = (GT10B_bank_3 // GT10B_pgrm_83)
P46_D = (GT10B_bank_3 // GT10B_pgrm_84)
P47_A = (GT10B_bank_3 // GT10B_pgrm_85)
P47_B = (GT10B_bank_3 // GT10B_pgrm_86)
P47_C = (GT10B_bank_3 // GT10B_pgrm_87)
P47_D = (GT10B_bank_3 // GT10B_pgrm_88)
P48_A = (GT10B_bank_3 // GT10B_pgrm_89)
P48_B = (GT10B_bank_3 // GT10B_pgrm_90)
P48_C = (GT10B_bank_3 // GT10B_pgrm_91)
P48_D = (GT10B_bank_3 // GT10B_pgrm_92)
P49_A = (GT10B_bank_3 // GT10B_pgrm_93)
P49_B = (GT10B_bank_3 // GT10B_pgrm_94)
P49_C = (GT10B_bank_3 // GT10B_pgrm_95)
P49_D = (GT10B_bank_3 // GT10B_pgrm_96)
P50_A = (GT10B_bank_3 // GT10B_pgrm_97)
P50_B = (GT10B_bank_3 // GT10B_pgrm_98)
P50_C = (GT10B_bank_3 // GT10B_pgrm_99)
P50_D = (GT10B_bank_3 // GT10B_pgrm_100)

# PortU, _Channel, CC, Value
# FootsUiw_tch
# GT10BU_F_S1=Ctrl(3,9,51,64)
# GT10BU_F_S2=Ctrl(3,9,52,64)
# GT10BU_F_S3=Ctrl(3,9,53,64)
# GT10BU_F_S4=Ctrl(3,9,54,64)
# GT10BU_F_S5=Ctrl(3,9,55,64)
# GT10BU_F_S6=Ctrl(3,9,56,64)
# GT10BU_F_S7=Ctrl(3,9,57,64)
# GT10BU_F_S8=Ctrl(3,9,58,64)
# GT10BU_T_OE=Ctrl(3,9,59,64)

#-----------------------------------------------------------------------------------------------------------
# Control section
# control.py
# -----------------------------------------------------------------------------------------------------------
# CONTROL SECTION
# -----------------------------------------------------------------------------------------------------------

# This control have the same behavior than the NavigateToScene python function above
# EXCEPT that there is NO wrap parameter for SceneSwitch
# The NavigateToScene CAN wrap through Scenes
# _ control=(ChannelFilter(9) >> Filter(CTRL) >>
#	(
#		(CtrlFilter(20) >> CtrlValueFilter(1) >> SceneSwitch(offset=-1)) //
#		(CtrlFilter(20) >> CtrlValueFilter(2) >> SceneSwitch(offset=1))  //
#		(CtrlFilter(20) >> CtrlValueFilter(3) >> SubSceneSwitch(offset=1, wrap=True))
#	))


# Reset all
reset = (
        System(AllAudioOff) // Pass() //
        ResetSD90 // Pass()
)

# FCB1010 UNO as controller (same as above different syntaxes)
fcb1010 = (ChannelFilter(9) >> CtrlFilter(20,22) >> CtrlSplit({
    20: Call(NavigateToScene),
    22: reset,
}))

# MIDI KEYBOARD CONTROLLER TO CONTROL MPG123 
keyboard = (
                   (CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
                   (Filter(NOTEON) >> Transpose(-36))
           ) >> Call(MPG123())

# Shortcut (Play switch)
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)
# -----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Patches configuration
# patches.py
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# PROGRAM CHANGE SECTION
#-----------------------------------------------------------------------------------------------
phantom=Velocity(fixed=0) >> Output('SD90-PART-A', channel=1, program=((96*128),1), volume=0)

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
#SD90-PART-A=cf >> Output('SD90-PART-A', channel=1, program=1, volume=100)
#SD90-PART-A=cf >> Output('SD90-PART-A', channel=2, program=1, volume=100)
#SD90-PART-A_drum=cf >> Channel(10) >> Transpose(-24) >> Output('SD90-PART-A', channel=10, program=1, volume=100)
d4=cf >> Output('SD90-PART-A', channel=10, program=1, volume=100)
d4_tom=cf >> Output('SD90-PART-A', channel=11, program=((96*128)+1,118), volume=100)

# FX Section
explosion = cf >> Key(0) >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------
violon = Output('SD90-PART-A', channel=1, program=((96*128),41))
piano_base = cf >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128),1))
nf_piano = Output('SD90-PART-A', channel=1, program=((96*128),2), volume=100)
piano = ChannelFilter(1) >> Velocity(fixed=80) >> Output('SD90-PART-A', channel=3, program=((96*128),1), volume=100)
piano2 = Output('SD90-PART-A', channel=2, program=((96*128),2), volume=100)

# Patch Synth
keysynth = cf >> Velocity(fixed=80) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
# Q49 only
marathon_intro=(q49>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

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

	) >> Transpose(-24) >> Output('SD90-PART-A', channel=4, program=((96*128)+1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(q49 >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(q49 >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output('SD90-PART-A', channel=4, program=((96*128),51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(q49 >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output('SD90-PART-B', channel=11, program=((99*128),99), volume=80))

marathon_bridge_split=cf>> KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
lowsynth2 = cf >> Velocity(fixed=115) >> Output('SD90-PART-A', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('SD90-PART-A', channel=1, program=((99*128),15), volume=100)
closer_base = Velocity(fixed=100) >> Output('SD90-PART-A', channel=2, program=((99*128),51), volume=100)
closer_main = cf >> KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=((99*128),92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=((99*128),92), volume=100)
tss_keyboard_main = cf >> KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=((99*128),103), volume=100)
tss_foot_main = cf >> KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('SD90-PART-A',channel=1,program=((98*128),53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('SD90-PART-A',channel=1,program=((98*128),53),volume=100,ctrls={91:75}))
analogkid_high = Output('SD90-PART-A', channel=2, program=((98*128),53), volume=100, ctrls={93:75, 91:100})
analogkid_main = cf >> KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending = cf >> Key('a1') >> Output('SD90-PART-A', channel=5, program=((81*128),68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight = cf >> Key('d#6') >> Output('SD90-PART-A', channel=16, program=((80*128),12), volume=100)

# Patch Centurion
centurion_synth = (Velocity(fixed=110) >>
	(
		Output('SD90-PART-A', channel=1, program=((99*128),96), volume=110) // 
		Output('SD90-PART-A', channel=2, program=((99*128),82), volume=110)
	))

# Patch Centurion Video
# TODO Ajouter vp.sh dans la configuration json
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

# Hack SD90-PART-A - Closer to the heart
closer_celesta_d4 =Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((98*128),11), volume=110)
#closer_celesta_d4 = (
#	(
#		Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((98*128),11), volume=110) //
#		(Velocity(fixed=100) >> Transpose(-72) >> Output('SD90-PART-A', channel=2, program=((99*128),96), volume=80))
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

closer_bell_d4 = Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((99*128),15), volume=100)
closer_patch_d4=(cf >>
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
        (KeyFilter('C1') >> Key('D4')) //
        (KeyFilter('E1') >> Key('A3')) //
        (KeyFilter('G1') >> Key('G3')) //
        (KeyFilter('D1') >> Key('F#3'))
   ) >> closer_bell_d4)

# YYZ
yyz_bell=Output('SD90-PART-A', channel=10, program=1, volume=100)
yyz=(cf >>
	(
		(KeyFilter('A1') >> Key('A4')) //
		(KeyFilter('F1') >> Key('G#4')) 
	) >> yyz_bell)

# Time Stand Steel
# Instruments
d4_melo_tom=Velocity(fixed=100) >> Output('SD90-PART-A', channel=11, program=((99*128)+1,118), volume=100)
d4_castanet=Velocity(fixed=100) >> Output('SD90-PART-A', channel=12, program=((99*128)+1,116), volume=100)
d4_808_tom=Velocity(fixed=80) >> Output('SD90-PART-A', channel=13, program=((99*128)+1,119), volume=100)

# Sons 1 et 2
tss_d4_melo_tom_A=cf >>KeyFilter('E1') >> Key('E6') >> d4_melo_tom

# Son 3
tss_d4_castanet=cf >>KeyFilter('G1') >> Key('a#2') >> d4_castanet

# Son 4
tss_d4_melo_tom_B=cf >>KeyFilter('F1') >> Key('a4') >> d4_808_tom

# Son 5
tss_d4_808_tom=cf >>KeyFilter('A1') >> Key('f#5') >> d4_808_tom

# Toggle Compressor + Harmonizer
big_country_pipe = ((
    CtrlFilter(21) >>
            (Ctrl(51, 64) // Ctrl(52, 64))) >> Port('SD90-MIDI-OUT-1'))

#-----------------------------------------------------------------------------------------------------------
# Scenes region
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=InitSoundModule, patch=Discard()),
    2: Scene("bass_cover", patch=Discard()),
    3: Scene("demon", patch=Discard()),
    4: Scene("styx", patch=Discard()),
    5: Scene("tabarnac", patch=Discard()),
    6: Scene("timeline", patch=Discard()),
    #7: SceneGroup("rush", [
    #       Scene("power-windows", patch = Discard()),
    #       Scene("grace-under-pressure", patch = Discard())
    #   ])
}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
_pre  = Print('input', portnames='in')
_pre  = ~ChannelFilter(9)
_post = Print('output',portnames='out')

# TODO repenser ce token (fit pas avec le reste)
_ctrl=keyboard

run(
    control=_ctrl,
    scenes=_scenes,
    #pre=_pre,
    #post=_post,
)
