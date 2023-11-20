#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Thanks to the programmer Dominic Sacre for that unbeatable MIDI engine - a true masterpiece

https://github.com/mididings/mididings (Community version! My prayers have been answered)

(DEPRECATED VERSION) https://github.com/dsacre/mididings (Sadly, abandonned since 2015)
'''

import os
import sys
import json
from time import sleep
from threading import Timer

from mididings import engine
from mididings.extra import *
from mididings.extra.osc import *
from mididings.extra.inotify import *
from mididings.event import PitchbendEvent, MidiEvent, NoteOnEvent, NoteOffEvent
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene, output_event

# Setup path
sys.path.append(os.path.realpath('.'))

# Environment
from dotenv import load_dotenv
load_dotenv()

# Extensions
from extensions.mp3 import *
from extensions.vlc import *
from extensions.philips import *
from extensions.spotify import *
from extensions.midimix import *
from extensions.httpclient import *

# Port name alias
midimix_midi = "midimix"

q49_midi     = "q49_midi"

gt10b_midi   = "gt10b_midi"

behringer    = "behringer"

sd90_port_a  = "sd90_port_a"
sd90_port_b  = "sd90_port_b"
sd90_midi_1  = "sd90_midi_1"
sd90_midi_2  = "sd90_midi_2"

mpk_port_a   = "mpk_port_a"
mpk_port_b   = "mpk_port_b"
mpk_midi     = "mpk_midi"
mpk_remote   = "mpk_remote"

config(

    initial_scene = 1,
    backend = 'alsa',
    client_name = 'mididings',

    out_ports = [

        (midimix_midi, ".*MIDI Mix MIDI 1.*",),
        (sd90_port_a,  '.*SD-90 Part A.*'),
        (sd90_port_b,  '.*SD-90 Part B.*'),
        (sd90_midi_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_2,  '.*SD-90 MIDI 2.*',),
        (behringer,    '.*UMC204HD 192k MIDI 1.*'),
        (q49_midi,     '.*Q49 MIDI 1.*',),
        (gt10b_midi,   '.*GT-10B MIDI 1.*',),
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port A.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),

    ],

    in_ports = [

        (midimix_midi, ".*MIDI Mix MIDI 1.*",),
        (sd90_port_a,  '.*SD-90 Part A.*'),
        (sd90_port_b,  '.*SD-90 Part B.*'),
        (sd90_midi_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_2,  '.*SD-90 MIDI 2.*',),
        (behringer,    '.*UMC204HD 192k MIDI 1.*'),
        (q49_midi,     '.*Q49 MIDI 1.*',),
        (gt10b_midi,   '.*GT-10B MIDI 1.*',),
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port A.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),

    ],

)

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene(".hook.memorize_scene")
)

# Patches and callable functions
        # --------------------------------------------------------------------
# Helper functions available for patches and controllers
# --------------------------------------------------------------------

# Glissando -------------------------------------------------------------------------------------------

def glissando_process(ev, from_note, to_note, vel, duration, direction, port, on):
    output_event(NoteOnEvent(port, ev.channel, from_note, vel)) if on else output_event(NoteOffEvent(port, ev.channel, from_note))
    if not on:
        from_note += 1
    if from_note < to_note:
        Timer(duration, lambda: glissando_process(ev, from_note, to_note, vel, duration, direction, port, not on)).start()

def glissando(ev, from_note, to_note, vel, duration, direction, port):
    glissando_process(ev, from_note, to_note, vel, duration, direction, port, True)

# -------------------------------------------------------------------------------------------

def NavigateToScene(ev):
    ''' 
    Navigate through Scenes and Sub-Scenes
    
    MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    
    With that function, you can wrap trough Scenes AND SubScenes
    
    That function assume that the first SceneNumber is 1
    '''
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

# ---------------------------------------------------------------------------------------------------------

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
''' Set or overwrite an environment variable '''
def setenv(ev, key, value):
    os.environ[key] = value

# ---------------------------------------------------------------------------------------------------------

def OnDebug(ev):
    print(ev)

# ---------------------------------------------------------------------------------------------------------

        
#
# Pre-buit filters for patches
#

mpk_a = PortFilter(mpk_port_a)
mpk_b = PortFilter(mpk_port_b)
pk5   = PortFilter(mpk_midi) >> ChannelFilter(3)
q49   = PortFilter(q49_midi)

# -------------------------------

        
#
# The EDIROL SD-90 Studio Canvas sound module definition patches for mididings (not fully implemented)
#

factor = 128

'''
Inst part: 
80(50H) = Special 1 set
81(51H) = Special 2 set
96(60H) = Classical set
97(61H) = Contemporary set
98(62H) = Solo set
99(63H) = Enhanced set
'''
Special1=80*factor
Special2=81*factor
Classical=96*factor
Contemporary=97*factor
Solo=98*factor
Enhanced=99*factor

'''
Drum part: 
104(60H) = Classical set
105(61H) = Contemporary set
106(62H) = Solo set
107(63H) = Enhanced set
'''
ClassicalDrum=104*factor
ContemporaryDrum=105*factor
SoloDrum=106*factor
EnhancedDrum=107*factor

'''
Variation
'''
Var1=1
Var2=2
Var3=3
Var4=4
Var5=5
Var6=6
Var7=7
Var8=8
Var9=9

# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01 = (Ctrl(sd90_port_a, 1, 100, 0) // Ctrl(sd90_port_a, 1, 101, 0) // Ctrl(sd90_port_a, 1, 6, 12) // Ctrl(sd90_port_a, 1, 38, 0))
PB_A02 = (Ctrl(sd90_port_a, 2, 100, 0) // Ctrl(sd90_port_a, 2, 101, 0) // Ctrl(sd90_port_a, 2, 6, 12) // Ctrl(sd90_port_a, 2, 38, 0))
PB_A03 = (Ctrl(sd90_port_a, 3, 100, 0) // Ctrl(sd90_port_a, 3, 101, 0) // Ctrl(sd90_port_a, 3, 6, 12) // Ctrl(sd90_port_a, 3, 38, 0))
PB_A04 = (Ctrl(sd90_port_a, 4, 100, 0) // Ctrl(sd90_port_a, 4, 101, 0) // Ctrl(sd90_port_a, 4, 6, 12) // Ctrl(sd90_port_a, 4, 38, 0))
PB_A05 = (Ctrl(sd90_port_a, 5, 100, 0) // Ctrl(sd90_port_a, 5, 101, 0) // Ctrl(sd90_port_a, 5, 6, 12) // Ctrl(sd90_port_a, 5, 38, 0))
PB_A06 = (Ctrl(sd90_port_a, 6, 100, 0) // Ctrl(sd90_port_a, 6, 101, 0) // Ctrl(sd90_port_a, 6, 6, 12) // Ctrl(sd90_port_a, 6, 38, 0))
PB_A07 = (Ctrl(sd90_port_a, 7, 100, 0) // Ctrl(sd90_port_a, 7, 101, 0) // Ctrl(sd90_port_a, 7, 6, 12) // Ctrl(sd90_port_a, 7, 38, 0))
PB_A08 = (Ctrl(sd90_port_a, 8, 100, 0) // Ctrl(sd90_port_a, 8, 101, 0) // Ctrl(sd90_port_a, 8, 6, 12) // Ctrl(sd90_port_a, 8, 38, 0))
PB_A09 = (Ctrl(sd90_port_a, 9, 100, 0) // Ctrl(sd90_port_a, 9, 101, 0) // Ctrl(sd90_port_a, 9, 6, 12) // Ctrl(sd90_port_a, 9, 38, 0))
PB_A10 = (Ctrl(sd90_port_a, 10, 100, 0) // Ctrl(sd90_port_a, 10, 101, 0) // Ctrl(sd90_port_a, 10, 6, 12) // Ctrl(sd90_port_a, 10, 38, 0))
PB_A11 = (Ctrl(sd90_port_a, 11, 100, 0) // Ctrl(sd90_port_a, 11, 101, 0) // Ctrl(sd90_port_a, 11, 6, 12) // Ctrl(sd90_port_a, 11, 38, 0))
PB_A12 = (Ctrl(sd90_port_a, 12, 100, 0) // Ctrl(sd90_port_a, 12, 101, 0) // Ctrl(sd90_port_a, 12, 6, 12) // Ctrl(sd90_port_a, 12, 38, 0))
PB_A13 = (Ctrl(sd90_port_a, 13, 100, 0) // Ctrl(sd90_port_a, 13, 101, 0) // Ctrl(sd90_port_a, 13, 6, 12) // Ctrl(sd90_port_a, 13, 38, 0))
PB_A14 = (Ctrl(sd90_port_a, 14, 100, 0) // Ctrl(sd90_port_a, 14, 101, 0) // Ctrl(sd90_port_a, 14, 6, 12) // Ctrl(sd90_port_a, 14, 38, 0))
PB_A15 = (Ctrl(sd90_port_a, 15, 100, 0) // Ctrl(sd90_port_a, 15, 101, 0) // Ctrl(sd90_port_a, 15, 6, 12) // Ctrl(sd90_port_a, 15, 38, 0))
PB_A16 = (Ctrl(sd90_port_a, 16, 100, 0) // Ctrl(sd90_port_a, 16, 101, 0) // Ctrl(sd90_port_a, 16, 6, 12) // Ctrl(sd90_port_a, 16, 38, 0))

# SD-90 Part B - All Channel
PB_B01 = (Ctrl(sd90_port_b, 1, 100, 0) // Ctrl(sd90_port_b, 1, 101, 0) // Ctrl(sd90_port_b, 1, 6, 12) // Ctrl(sd90_port_b, 1, 38, 0))
PB_B02 = (Ctrl(sd90_port_b, 2, 100, 0) // Ctrl(sd90_port_b, 2, 101, 0) // Ctrl(sd90_port_b, 2, 6, 12) // Ctrl(sd90_port_b, 2, 38, 0))
PB_B03 = (Ctrl(sd90_port_b, 3, 100, 0) // Ctrl(sd90_port_b, 3, 101, 0) // Ctrl(sd90_port_b, 3, 6, 12) // Ctrl(sd90_port_b, 3, 38, 0))
PB_B04 = (Ctrl(sd90_port_b, 4, 100, 0) // Ctrl(sd90_port_b, 4, 101, 0) // Ctrl(sd90_port_b, 4, 6, 12) // Ctrl(sd90_port_b, 4, 38, 0))
PB_B05 = (Ctrl(sd90_port_b, 5, 100, 0) // Ctrl(sd90_port_b, 5, 101, 0) // Ctrl(sd90_port_b, 5, 6, 12) // Ctrl(sd90_port_b, 5, 38, 0))
PB_B06 = (Ctrl(sd90_port_b, 6, 100, 0) // Ctrl(sd90_port_b, 6, 101, 0) // Ctrl(sd90_port_b, 6, 6, 12) // Ctrl(sd90_port_b, 6, 38, 0))
PB_B07 = (Ctrl(sd90_port_b, 7, 100, 0) // Ctrl(sd90_port_b, 7, 101, 0) // Ctrl(sd90_port_b, 7, 6, 12) // Ctrl(sd90_port_b, 7, 38, 0))
PB_B08 = (Ctrl(sd90_port_b, 8, 100, 0) // Ctrl(sd90_port_b, 8, 101, 0) // Ctrl(sd90_port_b, 8, 6, 12) // Ctrl(sd90_port_b, 8, 38, 0))
PB_B09 = (Ctrl(sd90_port_b, 9, 100, 0) // Ctrl(sd90_port_b, 9, 101, 0) // Ctrl(sd90_port_b, 9, 6, 12) // Ctrl(sd90_port_b, 9, 38, 0))
PB_B10 = (Ctrl(sd90_port_b, 10, 100, 0) // Ctrl(sd90_port_b, 10, 101, 0) // Ctrl(sd90_port_b, 10, 6, 12) // Ctrl(sd90_port_b, 10, 38, 0))
PB_B11 = (Ctrl(sd90_port_b, 11, 100, 0) // Ctrl(sd90_port_b, 11, 101, 0) // Ctrl(sd90_port_b, 11, 6, 12) // Ctrl(sd90_port_b, 11, 38, 0))
PB_B12 = (Ctrl(sd90_port_b, 12, 100, 0) // Ctrl(sd90_port_b, 12, 101, 0) // Ctrl(sd90_port_b, 12, 6, 12) // Ctrl(sd90_port_b, 12, 38, 0))
PB_B13 = (Ctrl(sd90_port_b, 13, 100, 0) // Ctrl(sd90_port_b, 13, 101, 0) // Ctrl(sd90_port_b, 13, 6, 12) // Ctrl(sd90_port_b, 13, 38, 0))
PB_B14 = (Ctrl(sd90_port_b, 14, 100, 0) // Ctrl(sd90_port_b, 14, 101, 0) // Ctrl(sd90_port_b, 14, 6, 12) // Ctrl(sd90_port_b, 14, 38, 0))
PB_B15 = (Ctrl(sd90_port_b, 15, 100, 0) // Ctrl(sd90_port_b, 15, 101, 0) // Ctrl(sd90_port_b, 15, 6, 12) // Ctrl(sd90_port_b, 15, 38, 0))
PB_B16 = (Ctrl(sd90_port_b, 16, 100, 0) // Ctrl(sd90_port_b, 16, 101, 0) // Ctrl(sd90_port_b, 16, 6, 12) // Ctrl(sd90_port_b, 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------

# Generic 
Piano = Output(sd90_port_a, channel=1, program=(1))

# Classical Set
StandardSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 1))
RoomSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 9))
PowerSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 17))
ElectricSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 25))
AnalogSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 26))
JazzSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 33))
BrushSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 41))
OrchestraSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 49))
SFXSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 57))

# Contemporary Set
StandardSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 1))
RoomSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 9))
PowerSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 17))
DanceSet =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 25))
RaveSet =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 26))
JazzSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 33))
BrushSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 41))

# Solo Set
St_Standard =  Output(sd90_port_a, channel=10, program=(SoloDrum, 1))
St_Room =  Output(sd90_port_a, channel=10, program=(SoloDrum, 9))
St_Power =  Output(sd90_port_a, channel=10, program=(SoloDrum, 17))
RustSet =  Output(sd90_port_a, channel=10, program=(SoloDrum, 25))
Analog2Set =  Output(sd90_port_a, channel=10, program=(SoloDrum, 26))
St_Jazz =  Output(sd90_port_a, channel=10, program=(SoloDrum, 33))
St_Brush =  Output(sd90_port_a, channel=10, program=(SoloDrum, 41))

# Enhanced Set
Amb_Standard =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 1))
Amb_Room =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 9))
GatedPower =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 17))
TechnoSet =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 25))
BullySet =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 26))
Amb_Jazz =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 33))
Amb_Brush =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 41))

# WIP SD-90 Full Patch implementation 
# Special 1 instrument part
DLAPad=Output(sd90_port_a, channel=1, program=(Special1, 1))
BrushingSaw=Output(sd90_port_a, channel=1, program=(Special1, 2))
Xtremities=Output(sd90_port_a, channel=1, program=(Special1, 3))
Atmostrings=Output(sd90_port_a, channel=1, program=(Special1, 4))
NooTongs=Output(sd90_port_a, channel=1, program=(Special1, 5))
Mistery=Output(sd90_port_a, channel=1, program=(Special1, 6))
EastrnEurope=Output(sd90_port_a, channel=1, program=(Special1, 7))
HarpsiAndStr=Output(sd90_port_a, channel=1, program=(Special1, 8))
ShoutGt=Output(sd90_port_a, channel=1, program=(Special1,9))
CleanChorus=Output(sd90_port_a, channel=1, program=(Special1, 10))
MidBoostGt=Output(sd90_port_a, channel=1, program=(Special1, 11))
Guitarvibe=Output(sd90_port_a, channel=1, program=(Special1, 12))
ClusterSect=Output(sd90_port_a, channel=1, program=(Special1, 13))
MariachiTp=Output(sd90_port_a, channel=1, program=(Special1, 14))
NYTenor=Output(sd90_port_a, channel=1, program=(Special1, 15))
JazzClub=Output(sd90_port_a, channel=1, program=(Special1, 16))
MoodyAlto=Output(sd90_port_a, channel=1, program=(Special1, 17))
FujiYama=Output(sd90_port_a, channel=1, program=(Special1, 18))
SDPiano=Output(sd90_port_a, channel=1, program=(Special1, 19))

# Special 2 instrument part
RichChoir=Output(sd90_port_a, channel=1, program=(Special2, 18))
OBBorealis=Output(sd90_port_a, channel=1, program=(Special2, 80))
VintagePhase=Output(sd90_port_a, channel=1, program=(Special2, 82))
FifthAtmAft=Output(sd90_port_a, channel=1, program=(Special2, 85))
Borealis=Output(sd90_port_a, channel=1, program=(Special2, 106))
CircularPad=Output(sd90_port_a, channel=1, program=(Special2, 107))
Oxigenizer=Output(sd90_port_a, channel=1, program=(Special2, 108))
Quasar=Output(sd90_port_a, channel=1, program=(Special2, 109))
HellSection=Output(sd90_port_a, channel=1, program=(Special2, 111))


# Classical instrument part
BirdTweet=Output(sd90_port_b, channel=4, program=(Classical, 124))
Applause=Output(sd90_port_b, channel=8, program=(Classical, 127))

# Classical instrument part - Variation 1
Itopia=Output(sd90_port_b, channel=1, program=(Classical+Var1, 92))
Kalimba=Output(sd90_port_b, channel=1, program=(Classical+Var1, 109))
BagPipe=Output(sd90_port_b, channel=1, program=(Classical+Var1, 110))
Dog=Output(sd90_port_b, channel=14, program=(Classical+Var1, 124))
Telephone2=Output(sd90_port_b, channel=1, program=(Classical+Var1, 125))
CarEngine=Output(sd90_port_b, channel=1, program=(Classical+Var1, 126))
Laughing=Output(sd90_port_b, channel=1, program=(Classical+Var1, 127))

# Classical instrument part - Variation 2
Screaming=Output(sd90_port_b, channel=13, program=(Classical+Var2, 127))
DoorCreak=Output(sd90_port_b, channel=1, program=(Classical+Var2, 125))
Thunder=Output(sd90_port_b, channel=15, program=(Classical+Var2, 123))

# Classical instrument part - Variation 3
Wind=Output(sd90_port_b, channel=3, program=(Classical+Var3, 123))
Explosion=Output(sd90_port_b, channel=7, volume=100, program=(Classical+Var3, 128))

# Classical instrument part - Variation 4
Stream=Output(sd90_port_b, channel=12, program=(Classical+Var4, 123))


# Classical instrument part - Variation 5
Siren=Output(sd90_port_b, channel=5, program=(Classical+Var5, 126))
Bubble=Output(sd90_port_b, channel=1, program=(Classical+Var5, 123))

# Classical instrument part - Variation 6
Train=Output(sd90_port_b, channel=6, program=(Classical+Var6, 126))

# Classical instrument part - Variation 7
Jetplane=Output(sd90_port_b, channel=1, program=(Classical+Var7, 126))

# Classical instrument part - Variation 8
Starship=Output(sd90_port_b, channel=1, program=(Classical+Var8, 126))

# Contemporary instrument part
Helicpoter=Output(sd90_port_b, channel=1, program=(Contemporary, 126))
Seashore=Output(sd90_port_b, channel=2, program=(Contemporary, 123))

# Contemporary instrument part - Variation 1
Rain=Output(sd90_port_b, channel=1, program=(Contemporary+Var1, 123))


### End SD-90 Patch list
# -------------------------------------------------------------------
# SD Mixer config 

Reset = SysEx(sd90_port_a, "f0,41,10,00,48,12,00,00,00,00,00,00,f7")
MixToAfx = SysEx(sd90_port_a,"f0,41,10,00,48,12,02,10,10,00,06,58,f7")
MasterEffect = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,20,00,78,56,f7")

# Audio Level Control
WaveLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,20,00,3f,f7", 10, 6)
InstLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,30,00,3f,f7", 10, 6)
MicGtLevel = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,00,00,3f,f7", 10, 6)


# SD-90 Bank Patch
SP1 = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,50,00,7d,7f,f7")
SP2 = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,51,00,7d,7e,f7")
SOLO = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,62,00,7d,6d,f7")
CLASIC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,60,00,7d,6f,f7")
CONTEM = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,61,00,7d,6e,f7")
ENHANC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,63,00,7d,6c,f7")

SD90_Initialize = [
    Reset, MixToAfx, MasterEffect, InitPitchBend
]

        
#
# The Boss GT-10B definition file for mididings
# This device has 4 banks, each bank contains 100 programs 
#

# Midi channel defined in the GT10B itself
GT10BChannel = 16

# Banks
GT10B_bank_0 = (Ctrl(gt10b_midi, GT10BChannel, 0, 0) // Ctrl(gt10b_midi, GT10BChannel, 32, 0))
GT10B_bank_1 = (Ctrl(gt10b_midi, GT10BChannel, 0, 1) // Ctrl(gt10b_midi, GT10BChannel, 32, 0))
GT10B_bank_2 = (Ctrl(gt10b_midi, GT10BChannel, 0, 2) // Ctrl(gt10b_midi, GT10BChannel, 32, 0))
GT10B_bank_3 = (Ctrl(gt10b_midi, GT10BChannel, 0, 3) // Ctrl(gt10b_midi, GT10BChannel, 32, 0))

# Program (same for the 4 banks)
GT10B_pgrm_1 = Program(gt10b_midi, channel=GT10BChannel, program=1)
GT10B_pgrm_2 = Program(gt10b_midi, channel=GT10BChannel, program=2)
GT10B_pgrm_3 = Program(gt10b_midi, channel=GT10BChannel, program=3)
GT10B_pgrm_4 = Program(gt10b_midi, channel=GT10BChannel, program=4)
GT10B_pgrm_5 = Program(gt10b_midi, channel=GT10BChannel, program=5)
GT10B_pgrm_6 = Program(gt10b_midi, channel=GT10BChannel, program=6)
GT10B_pgrm_7 = Program(gt10b_midi, channel=GT10BChannel, program=7)
GT10B_pgrm_8 = Program(gt10b_midi, channel=GT10BChannel, program=8)
GT10B_pgrm_9 = Program(gt10b_midi, channel=GT10BChannel, program=9)
GT10B_pgrm_10 = Program(gt10b_midi, channel=GT10BChannel, program=10)
GT10B_pgrm_11 = Program(gt10b_midi, channel=GT10BChannel, program=11)
GT10B_pgrm_12 = Program(gt10b_midi, channel=GT10BChannel, program=12)
GT10B_pgrm_13 = Program(gt10b_midi, channel=GT10BChannel, program=13)
GT10B_pgrm_14 = Program(gt10b_midi, channel=GT10BChannel, program=14)
GT10B_pgrm_15 = Program(gt10b_midi, channel=GT10BChannel, program=15)
GT10B_pgrm_16 = Program(gt10b_midi, channel=GT10BChannel, program=16)
GT10B_pgrm_17 = Program(gt10b_midi, channel=GT10BChannel, program=17)
GT10B_pgrm_18 = Program(gt10b_midi, channel=GT10BChannel, program=18)
GT10B_pgrm_19 = Program(gt10b_midi, channel=GT10BChannel, program=19)
GT10B_pgrm_20 = Program(gt10b_midi, channel=GT10BChannel, program=20)
GT10B_pgrm_21 = Program(gt10b_midi, channel=GT10BChannel, program=21)
GT10B_pgrm_22 = Program(gt10b_midi, channel=GT10BChannel, program=22)
GT10B_pgrm_23 = Program(gt10b_midi, channel=GT10BChannel, program=23)
GT10B_pgrm_24 = Program(gt10b_midi, channel=GT10BChannel, program=24)
GT10B_pgrm_25 = Program(gt10b_midi, channel=GT10BChannel, program=25)
GT10B_pgrm_26 = Program(gt10b_midi, channel=GT10BChannel, program=26)
GT10B_pgrm_27 = Program(gt10b_midi, channel=GT10BChannel, program=27)
GT10B_pgrm_28 = Program(gt10b_midi, channel=GT10BChannel, program=28)
GT10B_pgrm_29 = Program(gt10b_midi, channel=GT10BChannel, program=29)
GT10B_pgrm_30 = Program(gt10b_midi, channel=GT10BChannel, program=30)
GT10B_pgrm_31 = Program(gt10b_midi, channel=GT10BChannel, program=31)
GT10B_pgrm_32 = Program(gt10b_midi, channel=GT10BChannel, program=32)
GT10B_pgrm_33 = Program(gt10b_midi, channel=GT10BChannel, program=33)
GT10B_pgrm_34 = Program(gt10b_midi, channel=GT10BChannel, program=34)
GT10B_pgrm_35 = Program(gt10b_midi, channel=GT10BChannel, program=35)
GT10B_pgrm_36 = Program(gt10b_midi, channel=GT10BChannel, program=36)
GT10B_pgrm_37 = Program(gt10b_midi, channel=GT10BChannel, program=37)
GT10B_pgrm_38 = Program(gt10b_midi, channel=GT10BChannel, program=38)
GT10B_pgrm_39 = Program(gt10b_midi, channel=GT10BChannel, program=39)
GT10B_pgrm_40 = Program(gt10b_midi, channel=GT10BChannel, program=40)
GT10B_pgrm_41 = Program(gt10b_midi, channel=GT10BChannel, program=41)
GT10B_pgrm_42 = Program(gt10b_midi, channel=GT10BChannel, program=42)
GT10B_pgrm_43 = Program(gt10b_midi, channel=GT10BChannel, program=43)
GT10B_pgrm_44 = Program(gt10b_midi, channel=GT10BChannel, program=44)
GT10B_pgrm_45 = Program(gt10b_midi, channel=GT10BChannel, program=45)
GT10B_pgrm_46 = Program(gt10b_midi, channel=GT10BChannel, program=46)
GT10B_pgrm_47 = Program(gt10b_midi, channel=GT10BChannel, program=47)
GT10B_pgrm_48 = Program(gt10b_midi, channel=GT10BChannel, program=48)
GT10B_pgrm_49 = Program(gt10b_midi, channel=GT10BChannel, program=49)
GT10B_pgrm_50 = Program(gt10b_midi, channel=GT10BChannel, program=50)
GT10B_pgrm_51 = Program(gt10b_midi, channel=GT10BChannel, program=51)
GT10B_pgrm_52 = Program(gt10b_midi, channel=GT10BChannel, program=52)
GT10B_pgrm_53 = Program(gt10b_midi, channel=GT10BChannel, program=53)
GT10B_pgrm_54 = Program(gt10b_midi, channel=GT10BChannel, program=54)
GT10B_pgrm_55 = Program(gt10b_midi, channel=GT10BChannel, program=55)
GT10B_pgrm_56 = Program(gt10b_midi, channel=GT10BChannel, program=56)
GT10B_pgrm_57 = Program(gt10b_midi, channel=GT10BChannel, program=57)
GT10B_pgrm_58 = Program(gt10b_midi, channel=GT10BChannel, program=58)
GT10B_pgrm_59 = Program(gt10b_midi, channel=GT10BChannel, program=59)
GT10B_pgrm_60 = Program(gt10b_midi, channel=GT10BChannel, program=60)
GT10B_pgrm_61 = Program(gt10b_midi, channel=GT10BChannel, program=61)
GT10B_pgrm_62 = Program(gt10b_midi, channel=GT10BChannel, program=62)
GT10B_pgrm_63 = Program(gt10b_midi, channel=GT10BChannel, program=63)
GT10B_pgrm_64 = Program(gt10b_midi, channel=GT10BChannel, program=64)
GT10B_pgrm_65 = Program(gt10b_midi, channel=GT10BChannel, program=65)
GT10B_pgrm_66 = Program(gt10b_midi, channel=GT10BChannel, program=66)
GT10B_pgrm_67 = Program(gt10b_midi, channel=GT10BChannel, program=67)
GT10B_pgrm_68 = Program(gt10b_midi, channel=GT10BChannel, program=68)
GT10B_pgrm_69 = Program(gt10b_midi, channel=GT10BChannel, program=69)
GT10B_pgrm_70 = Program(gt10b_midi, channel=GT10BChannel, program=70)
GT10B_pgrm_71 = Program(gt10b_midi, channel=GT10BChannel, program=71)
GT10B_pgrm_72 = Program(gt10b_midi, channel=GT10BChannel, program=72)
GT10B_pgrm_73 = Program(gt10b_midi, channel=GT10BChannel, program=73)
GT10B_pgrm_74 = Program(gt10b_midi, channel=GT10BChannel, program=74)
GT10B_pgrm_75 = Program(gt10b_midi, channel=GT10BChannel, program=75)
GT10B_pgrm_76 = Program(gt10b_midi, channel=GT10BChannel, program=76)
GT10B_pgrm_77 = Program(gt10b_midi, channel=GT10BChannel, program=77)
GT10B_pgrm_78 = Program(gt10b_midi, channel=GT10BChannel, program=78)
GT10B_pgrm_79 = Program(gt10b_midi, channel=GT10BChannel, program=79)
GT10B_pgrm_80 = Program(gt10b_midi, channel=GT10BChannel, program=80)
GT10B_pgrm_81 = Program(gt10b_midi, channel=GT10BChannel, program=81)
GT10B_pgrm_82 = Program(gt10b_midi, channel=GT10BChannel, program=82)
GT10B_pgrm_83 = Program(gt10b_midi, channel=GT10BChannel, program=83)
GT10B_pgrm_84 = Program(gt10b_midi, channel=GT10BChannel, program=84)
GT10B_pgrm_85 = Program(gt10b_midi, channel=GT10BChannel, program=85)
GT10B_pgrm_86 = Program(gt10b_midi, channel=GT10BChannel, program=86)
GT10B_pgrm_87 = Program(gt10b_midi, channel=GT10BChannel, program=87)
GT10B_pgrm_88 = Program(gt10b_midi, channel=GT10BChannel, program=88)
GT10B_pgrm_89 = Program(gt10b_midi, channel=GT10BChannel, program=89)
GT10B_pgrm_90 = Program(gt10b_midi, channel=GT10BChannel, program=90)
GT10B_pgrm_91 = Program(gt10b_midi, channel=GT10BChannel, program=91)
GT10B_pgrm_92 = Program(gt10b_midi, channel=GT10BChannel, program=92)
GT10B_pgrm_93 = Program(gt10b_midi, channel=GT10BChannel, program=93)
GT10B_pgrm_94 = Program(gt10b_midi, channel=GT10BChannel, program=94)
GT10B_pgrm_95 = Program(gt10b_midi, channel=GT10BChannel, program=95)
GT10B_pgrm_96 = Program(gt10b_midi, channel=GT10BChannel, program=96)
GT10B_pgrm_97 = Program(gt10b_midi, channel=GT10BChannel, program=97)
GT10B_pgrm_98 = Program(gt10b_midi, channel=GT10BChannel, program=98)
GT10B_pgrm_99 = Program(gt10b_midi, channel=GT10BChannel, program=99)
GT10B_pgrm_100 = Program(gt10b_midi, channel=GT10BChannel, program=100)

# GT10B_bank 0
#U01_A = [
#       Ctrl(gt10b_midi, GT10BChannel,10, 127),
#       Ctrl(gt10b_midi, GT10BChannel,10, 0),
#       Ctrl(gt10b_midi, GT10BChannel,11, 127),
#       Ctrl(gt10b_midi, GT10BChannel,11, 0),
#       Ctrl(gt10b_midi, GT10BChannel,7, 127),
#       ]

#U01_A = (GT10B_bank_0 // GT10B_pgrm_1 // Ctrl(gt10b_midi, GT10BChannel, 7,127))
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

# Send CC
GT10B_Ctrl =  Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)

# Send CC aliases
GT10B_Tuner = Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)    
GT10B_Volume = GT10B_Ctrl
GT10B_Expression = GT10B_Ctrl

        
#
# The Line 6 POD-HD-500 definition patches for mididings
#

# Channel d'écoute
hd500_channel = 15

# Connecté a quel port MIDI ?
hd500_port = mpk_midi

# Programmes
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

# Abstract patch (must be chained before by a Ctrl(c,v))
# Example: 
#       Ctrl(69, 127) >> CtrlPod will set the tuner on.
# mean  Ctrl(hd500_port, hd500_channel, 69, 127)
CtrlPod = Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)

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

# Exp1 et Exp2
HD500_Expr1 = Ctrl(hd500_port, hd500_channel, 1, EVENT_VALUE)
HD500_Expr2 = Ctrl(hd500_port, hd500_channel, 2, EVENT_VALUE)

# HD500_Tuner (shortcut)
HD500_Tuner = CtrlPod

HD500_TunerOn  = Ctrl(hd500_port, hd500_channel, 69, 127)
HD500_TunerOff = Ctrl(hd500_port, hd500_channel, 69, 0)

# Looper
HD500_Looper = CtrlFilter(60, 61, 62, 63, 65, 67, 68, 99) >> CtrlPod

# Tap
# Expected EVENT_VALUE between 64 and 127
HD500_Tap = Ctrl(hd500_port, hd500_channel, 64, EVENT_VALUE)

        
'''
    The Soundcraft UI 16 patches for mididings
    Those patches use the OSC protocol to communicate with the Osc Soundcraft Bridge daemon
    The CC number correspond to the SoundCraft input channel
    The CC value correspond to the SoundCraft cursor value 
    https://github.com/stefets/osc-soundcraft-bridge
'''

#
# Helper functions used by the Soundcraft UI patches
#

# 0-127 to 0-1
ratio=0.7874015748 / 100

def ui_cursor(ev):
    return ev.data2 * ratio

def ui_knob(ev):
    return ui_cursor(ev)

def ui_mute(ev):
    return 1 if ev.data2==127 else 0

''' Return the controller value for SendOsc '''
def ui_event(ev, offset=0):
    return ev.ctrl+offset if ev.type == CTRL else -1

''' Wrapper over ui_event '''
def ui_left(ev):
    return ui_event(ev)

''' Wrapper over ui_event '''
def ui_right(ev):
    return ui_event(ev, 1)


# Osc Soundcraft Bridge definition
osb_port = 56420
master_path = "/master"
mix_path = "/mix"
reverb_path = "/reverb"
chorus_path = "/chorus"
delay_path = "/delay"
room_path = "/room"
mute_path = "/mute"
bass_path = "/bass"
mid_path = "/mid"
treble_path = "/treble"


# Main volume
ui_master=SendOSC(osb_port, master_path, ui_cursor)

# Mono patches / stands for all XLR+1/4 sockets
# Stereo patches must target left channel, right channel will change in the same time
mix_mono = SendOSC(osb_port, mix_path,  ui_event, ui_cursor, "i")
mix_stereo = [
        SendOSC(osb_port, mix_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, mix_path, ui_right, ui_cursor, "i"),
    ]

reverb_mono = SendOSC(osb_port, reverb_path,  ui_event, ui_cursor, "i")
reverb_stereo = [
        SendOSC(osb_port, reverb_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, reverb_path, ui_right, ui_cursor, "i"),
    ]

chorus_mono = SendOSC(osb_port, chorus_path,  ui_event, ui_cursor, "i")
chorus_stereo = [
        SendOSC(osb_port, chorus_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, chorus_path, ui_right, ui_cursor, "i"),
    ]

delay_mono = SendOSC(osb_port, delay_path,  ui_event, ui_cursor, "i")
delay_stereo = [
        SendOSC(osb_port, delay_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, delay_path, ui_right, ui_cursor, "i"),
    ]

room_mono = SendOSC(osb_port, room_path,  ui_event, ui_cursor, "i")
room_stereo = [
        SendOSC(osb_port, room_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, room_path, ui_right, ui_cursor, "i"),
    ]


mute_mono = SendOSC(osb_port, mute_path, ui_event, ui_mute, "i")
mute_stereo = [
        SendOSC(osb_port, mute_path, ui_left,  ui_mute, "i"),    
        SendOSC(osb_port, mute_path, ui_right, ui_mute, "i"),
    ]

# Equalizer
bass_mono = SendOSC(osb_port, bass_path, ui_event, ui_cursor, "i")
bass_stereo = [
        SendOSC(osb_port, bass_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, bass_path, ui_right, ui_cursor, "i"),
    ]

mid_mono = SendOSC(osb_port, mid_path, ui_event, ui_cursor, "i")
mid_stereo = [
        SendOSC(osb_port, mid_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, mid_path, ui_right, ui_cursor, "i"),
    ]

treble_mono = SendOSC(osb_port, treble_path, ui_event, ui_cursor, "i")
treble_stereo = [
        SendOSC(osb_port, treble_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, treble_path, ui_right, ui_cursor, "i"),
    ]


# Static stereo inputs
# Line patches
ui_line_mute=[
        SendOSC(osb_port, mute_path, 0, ui_mute, "l"),    
        SendOSC(osb_port, mute_path, 1, ui_mute, "l"),
    ]
    
ui_line_mix=[
        SendOSC(osb_port, mix_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, mix_path, 1, ui_cursor, "l"),
    ]

line_bass = [
        SendOSC(osb_port, bass_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, bass_path, 1, ui_cursor, "l"),
    ]
line_mid = [
        SendOSC(osb_port, mid_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, mid_path, 1, ui_cursor, "l"),
    ]
line_treble = [
        SendOSC(osb_port, treble_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, treble_path, 1, ui_cursor, "l"),
    ]

# Player patches
ui_player_mute=[
        SendOSC(osb_port, mute_path, 0, ui_mute, "p"),    
        SendOSC(osb_port, mute_path, 1, ui_mute, "p"),
    ]
    
ui_player_mix=[
        SendOSC(osb_port, mix_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, mix_path, 1, ui_cursor, "p"),
    ]

player_bass = [
        SendOSC(osb_port, bass_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, bass_path, 1, ui_cursor, "p"),
    ]
player_mid = [
        SendOSC(osb_port, mid_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, mid_path, 1, ui_cursor, "p"),
    ]
player_treble = [
        SendOSC(osb_port, treble_path, 0, ui_cursor, "p"),
        SendOSC(osb_port, treble_path, 1, ui_cursor, "p"),
    ]

# -----------------------------------------------------
# Group patch by channel
ui_standard_fx = ChannelSplit({
            1:mix_mono,
            2:reverb_mono,
            3:delay_mono,
            4:chorus_mono,
        })

ui_standard_stereo_fx = ChannelSplit({
            1:mix_stereo,
            2:reverb_stereo,
            3:delay_stereo,
            4:chorus_stereo,
        })     

# 
ui_standard_stereo_eq = ChannelSplit({
            1:mix_stereo,
            2:bass_stereo,
            3:mid_stereo,
            4:treble_stereo,
        })

ui_line_mix_eq = ChannelSplit({
            1:ui_line_mix,
            2:line_bass,
            3:line_mid,
            4:line_treble,
        })

ui_player_mix_eq = ChannelSplit({
            1:ui_player_mix,
            2:player_bass,
            3:player_mid,
            4:player_treble,
        })
        
#
# Philips Hue Patches
#

# HueScene(ZoneId, SceneName)
# HueBlackout(ZoneId)

studio=2
HueNormal=Call(HueScene(studio, "Normal"))
HueGalaxie=Call(HueScene(studio, "Galaxie"))
HueGalaxieMax=Call(HueScene(studio, "GalaxieMax"))
HueDemon=Call(HueScene(studio, "Demon"))
HueDetente=Call(HueScene(studio, "Détente"))
HueVeilleuse=Call(HueScene(studio, "Veilleuse"))
HueLecture=Call(HueScene(studio, "Lecture"))
HueSsFullBlanc=Call(HueScene(studio, "SsFullBlanc"))
HueSoloRed=Call(HueScene(studio, "SoloRed"))

cuisine=4
HueCuisine=Call(HueScene(cuisine, "Minimal"))

chambre=1
HueChambreMaitre=Ctrl(3, 100) >> Call(HueScene(chambre, "Normal"))

HueStudioOff=[
    Call(HueBlackout(2))
]

HueAllOff=[
    Call(HueBlackout(1)),
    Call(HueBlackout(2)),
    Call(HueBlackout(4)),
]

p_hue = Filter(NOTEON) >> [
    KeyFilter(notes=[101]) >> HueNormal,
    KeyFilter(notes=[102]) >> HueDetente,
    KeyFilter(notes=[103]) >> HueLecture,
    KeyFilter(notes=[104]) >> HueVeilleuse,
    KeyFilter(notes=[105]) >> HueGalaxie,
    KeyFilter(notes=[106]) >> HueGalaxieMax,
    KeyFilter(notes=[107]) >> HueDemon,
    KeyFilter(notes=[108]) >> HueStudioOff,
    KeyFilter(notes=[109]) >> Ctrl(3, 50) >> HueLecture,
    KeyFilter(notes=[116]) >> HueCuisine
]

        
#
# Cakewalk Generic Control Surface definition -----------------------------------------------
#
CakePlay=Ctrl(mpk_midi, 1, 118, 127)
CakeStop=Ctrl(mpk_midi, 1, 119, 127)
CakeRecord=Ctrl(mpk_midi, 1, 119, 127)

        
# -----------------------------------------------------------------------------------------------
# Execution patches
# -----------------------------------------------------------------------------------------------
# Notes :
# - Ctrl #3 est Undefined selon la documentation du protocole MIDI; donc libre d'utilisation.
# - L'utilisation du Ctrl(3,value) sert a passer le value dans EVENT_VALUE pour l'unité suivante dans une série d'unité
# - Soit pour assigner une valeur au pédales d'expression du POD HD 500
# - Soit pour déterminer la valeur d'une transition pour le chargement d'une scène du Philips HUE
# - Soit pour contrôler Cakewalk
#
# Controller 3 : ref.: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
# CC      Bin             Hex     Control function    Value       Used as
# 3	00000011	03	Undefined	    0-127	MSB

akai_pad_nature = [
    ~Filter(PITCHBEND) >> KeyFilter(notes=[109]) >> LatchNotes(polyphonic=True) >> Key(0) >> Rain,
    KeyFilter(notes=[110]) >> Key(12) >> Thunder,
    KeyFilter(notes=[111]) >> Key(48) >> Dog,
    KeyFilter(notes=[112]) >> Key(24) >> BirdTweet,
    KeyFilter(notes=[113]) >> Key(72) >> Screaming,
    KeyFilter(notes=[114]) >> Key(48) >> Velocity(fixed=100) >> Explosion, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[115]) >> Key(12) >> Wind, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[116]) >> LatchNotes(polyphonic=True) >> Key(36) >> Applause, 
]

# Patch Synth
keysynth =  Velocity(fixed=80) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
marathon_intro=(mpk_a
>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

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

	) >> Transpose(-24) >> Output(sd90_port_a, channel=4, program=(Classical+Var1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(mpk_a
 >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(mpk_a
 >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output(sd90_port_a, channel=4, program=(Classical,51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(mpk_a
 >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output(sd90_port_b, channel=11, program=(Enhanced,99), volume=80))

marathon_bridge_split= KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth2 =  Velocity(fixed=115) >> Output(sd90_port_a, channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output(sd90_port_a, channel=1, program=(Enhanced,15), volume=100)
closer_base = Velocity(fixed=100) >> Output(sd90_port_a, channel=2, program=(Enhanced,51), volume=100)
closer_main =  KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output(sd90_port_a, channel=3, program=(Enhanced,92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output(sd90_port_a, channel=3, program=(Enhanced,92), volume=100)
tss_keyboard_main =  KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=2, program=(Enhanced,103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=2, program=(Enhanced,103), volume=100)
tss_foot_main =  KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output(sd90_port_a,channel=1,program=(Solo,53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output(sd90_port_a,channel=1,program=(Solo,53),volume=100,ctrls={91:75}))
analogkid_high = Output(sd90_port_a, channel=2, program=(Solo,53), volume=100, ctrls={93:75, 91:100})
analogkid_main =  KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending =  Key('a1') >> Output(sd90_port_a, channel=5, program=(Special2,68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight =  Key('d#6') >> Output(sd90_port_a, channel=16, program=(Special1,12), volume=100)

# Band : Moi ----------------------------------------------------

# Song : Centurion 

# Init patch 
i_centurion = [
        Call(Playlist()), 
        P02A, Ctrl(3,127) >> HD500_Expr2
]

# Execution patch
seq_centurion = (Velocity(fixed=110) >>	
    [
		Output(sd90_port_a, channel=1, program=(Enhanced,96), volume=110, pan=32),
		Output(sd90_port_a, channel=2, program=(Enhanced,82), volume=110, pan=96)
	])

# Filter
p_centurion = (LatchNotes(True, reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) //
		(KeyFilter('E3') >> Key('D2')) //
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> seq_centurion)


# Band : Big Country ------------------------------------------

# Song : In a big country
i_big_country = [U01_A, P14A, FS1, FS3, Ctrl(3,127) >> HD500_Expr2]
p_big_country = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[65]) >> FS1),
             (KeyFilter(notes=[67]) >> FS2),
             #(KeyFilter(notes=[69]) >> FS3),
             (KeyFilter(notes=[69]) >> FS4),
             (KeyFilter(notes=[71]) >> [HueGalaxie, FS2, Ctrl(3,85)  >> HD500_Expr2]),
             (KeyFilter(notes=[72]) >> [HueSoloRed, FS2, Ctrl(3,127) >> HD500_Expr2])
         ])

# Song : In a big country - recording
i_big_country_live = [P14C]
p_big_country_live = (pk5 >> Filter(NOTEON) >>
        [
            # Daw control
            KeyFilter(notes=[60]) >> HueStudioOff,
            KeyFilter(notes=[61]) >> CakeRecord,
            KeyFilter(notes=[62]) >> HueSsFullBlanc,
            KeyFilter(notes=[63]) >> Pass(),
            KeyFilter(notes=[64]) >> HueStudioOff,
            # Guitar control
            KeyFilter(notes=[65]) >> FS4,   # F / Delay
            KeyFilter(notes=[66]) >> Ctrl(3,100) >> HD500_Expr2,   # F#
            KeyFilter(notes=[67]) >> [FS2],   # G
            KeyFilter(notes=[68]) >> Ctrl(3,127) >> HD500_Expr2,   # G#
            KeyFilter(notes=[69]) >> [FS2, Ctrl(3,100) >> HD500_Expr2], # A
        ])

# Song : Highland Scenery
p_highland_scenery = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[65]) >> FS1),
             (KeyFilter(notes=[67]) >> FS2),
             (KeyFilter(notes=[69]) >> FS3),
             (KeyFilter(notes=[71]) >> FS4),
             (KeyFilter(notes=[72]) >> [FS3, FS4])
         ])


# Big Country fin de section ------------------------------------------

# Band : Octobre ------------------------------------------

# Init patch (Intro)
i_octobre = [P09A, FS1, FS3, FS4, Ctrl(3,127) >> HD500_Expr2]

# Execution patch
p_octobre = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[64]) >> [FS4, Ctrl(3,120) >> HD500_Expr2]),
             (KeyFilter(notes=[65]) >> [FS1, Ctrl(3,100) >> HD500_Expr2]),
             (KeyFilter(notes=[67]) >> [FS1, FS2, FS4, Ctrl(3,65) >> HD500_Expr2]),
             (KeyFilter(notes=[69]) >> [FS2, Ctrl(3,127) >> HD500_Expr2]),
             (KeyFilter(notes=[71]) >> [FS1, FS4, Ctrl(3,100 ) >> HD500_Expr2])
         ])


# Octobre fin de section ------------------------------------------

# Band : Rush ------------------------------------------

# Default init patch
i_rush = [P02A, Ctrl(3,100) >> HD500_Expr2]

# Default patch - tout en paralelle mais séparé par contexte
p_rush = (pk5 >> Filter(NOTEON) >>
    [
        [
            KeyFilter(notes=[60]) >> HueStudioOff,
            KeyFilter(notes=[62]) >> HueGalaxie,
            KeyFilter(notes=[64]) >> HueSoloRed
        ],                
        [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, FS4, Ctrl(3,100) >> HD500_Expr2, HueGalaxie],
            KeyFilter(notes=[72]) >> [FS1, FS4, Ctrl(3,120) >> HD500_Expr2, HueSoloRed]
        ]
    ])

# Subdivisions

# Init patch
i_rush_sub=[P02A, FS3, Ctrl(3,100) >> HD500_Expr2]

# Grand Designs

# Init patch
i_rush_gd = [P02A, FS1, FS3, Ctrl(3,127) >> HD500_Expr2] 

# Execution patch
p_rush_gd = (pk5 >> 
    [
        Filter(NOTEON) >> [
                [ 
                    KeyFilter(notes=[60]) >> HueStudioOff,
                    KeyFilter(notes=[61]) >> Ctrl(3, 1) >> HueDemon,
                    KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxie,
                    KeyFilter(notes=[64, 72]) >> Ctrl(3, 1) >> HueSoloRed,
                ],
                [
                    KeyFilter(notes=[67]) >> FS4,
                    KeyFilter(notes=[69]) >> [Ctrl(3, 100) >> HD500_Expr2, FS4],
                    KeyFilter(notes=[71]) >> [Ctrl(3, 127) >> HD500_Expr2, FS4],
                    KeyFilter(notes=[72]) >>  Ctrl(3, 127) >> HD500_Expr2
                ],
            ],
        Filter(NOTEOFF) >> [
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 1) >> HueGalaxie
                ],
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 100) >> HD500_Expr2
                ]
            ],
    ])

# Youtube SoundCraftBridge Demo
p_rush_gd_demo = (ChannelFilter(16) >> 
    [
        Filter(NOTEON) >> [
                [ 
                    KeyFilter(notes=[113]) >> Ctrl(3, 50) >> HueLecture,
                    #KeyFilter(notes=[61]) >> Ctrl(3, 1) >> HueDemon,
                    #KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxie,
                    #KeyFilter(notes=[64, 72]) >> Ctrl(3, 1) >> HueSoloRed,
                ],
                [
                    #KeyFilter(notes=[67]) >> FS4,
                    #KeyFilter(notes=[69]) >> [Ctrl(3, 100) >> HD500_Expr2, FS4],
                    #KeyFilter(notes=[71]) >> [Ctrl(3, 127) >> HD500_Expr2, FS4],
                    #KeyFilter(notes=[72]) >>  Ctrl(3, 127) >> HD500_Expr2
                ],
            ],
        Filter(NOTEOFF) >> [
                [
                    #KeyFilter(notes=[72]) >> Ctrl(3, 1) >> HueGalaxie
                ],
                [
                    #KeyFilter(notes=[72]) >> Ctrl(3, 100) >> HD500_Expr2
                ]
            ],
    ])

# The Trees

# Init patch
i_rush_trees = [P02A, FS3, Ctrl(3,100) >> HD500_Expr2] 

# Foot keyboard output
p_rush_trees_foot = Velocity(fixed=110) >> Output(sd90_port_a, channel=1, program=(Classical,51), volume=110, ctrls={93:75, 91:75})

# Execution patch
p_rush_trees=(pk5 >>
    [
        # Controle de l'éclairage
        Filter(NOTEON) >> [
            KeyFilter('C3') >> HueGalaxie,
            KeyFilter(notes=[71]) >> HueGalaxie,
            KeyFilter(notes=[72]) >> HueSoloRed,
        ],
        # Controle du POD HD500 
        Filter(NOTEON) >> [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, Ctrl(3,100) >> HD500_Expr2],
            KeyFilter(notes=[72]) >> [FS1, Ctrl(3,120) >> HD500_Expr2],
        ],
        # Controle du séquenceur 
        # Il faut laisser passer f3 dans un filtre dummy car il sert de Latch
        [
            KeyFilter('C3') >> Key('A0'),
            KeyFilter('D3') >> Key('B0'),
            KeyFilter('E3') >> Key('D1'),
            KeyFilter('f3') >> Pass(),
        ] >> LatchNotes(False, reset='f3') >> p_rush_trees_foot
    ])

# Rush fin de section ------------------------------------------
p_hd500_base = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[65]) >> FS1),
             (KeyFilter(notes=[67]) >> FS2),
             (KeyFilter(notes=[69]) >> FS3),
             (KeyFilter(notes=[71]) >> FS4),
             (KeyFilter(notes=[72]) >> [FS3, FS4])
         ])

# ---
# Daw helper
p_transport = (pk5 >> 
        [
            Filter(NOTEON)  >> KeyFilter(notes=[60])    >> [CakePlay],
            Filter(NOTEON)  >> KeyFilter(notes=[61])    >> [HueStudioOff],
            Filter(NOTEON)  >> KeyFilter(notes=[62])    >> [CakeRecord],
            Filter(NOTEOFF) >> KeyFilter(notes=[60,62]) >> [HueSsFullBlanc], 
        ])

# Interlude patch, between two songs
interlude = mpk_b >> ChannelFilter(16) >> KeyFilter(notes=[0,49]) >> Velocity(fixed=50) >> LatchNotes(reset=0) >> [Oxigenizer]

# Glissando
p_glissando=(Filter(NOTEON) >> Call(glissando, 48, 84, 100, 0.01, -1, sd90_port_a))


# Scenes
_scenes = {
        1: Scene("Initialize", init_patch=SD90_Initialize, patch=Discard()),
    2: SceneGroup("RUSH",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Generic", init_patch=Call(Playlist()), patch=Discard()//p_rush),
            Scene("Subdivisions", init_patch=i_rush_sub//Call(Playlist()), patch=Discard()//p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist()), patch=Discard()//p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush_gd, patch=Discard()//p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
            Scene("YYZ", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("Limelight", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("FlyByNight", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("RedBarchetta", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("Freewill", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("SpritOfRadio", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("TomSawyer", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
            Scene("CloserToTheHeart", init_patch=i_rush//Call(Playlist()), patch=p_hd500_base),
        ]),
    3: SceneGroup("BassCover",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Default", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Queen", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("T4F", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Toto", init_patch=Call(Playlist())//U01_A, patch=Discard()),
        ]),
    4: SceneGroup("Recording",
        [
            Scene("Bass", init_patch=Discard(), patch=p_transport),
        ]),
    5: SceneGroup("BigCountry",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("InBigCountry", init_patch=i_big_country, patch=p_big_country),
            Scene("HighlandScenery", init_patch=U01_B // P14B, patch=p_highland_scenery),
            Scene("Inwards", init_patch=U01_B // P14B, patch=p_highland_scenery),
            Scene("AnglePark", init_patch=U01_B // P14B, patch=p_transport // p_highland_scenery),
        ]),
    6: SceneGroup("GrandDesignsStudio",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("PowerWindows", init_patch=Call(Playlist()), patch=p_rush_gd_demo),
            Scene("Futur", init_patch=Discard(), patch=p_transport),
        ]),
    7: SceneGroup("Keyboard",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("BrushingSaw", LatchNotes(False, reset='f3') >> Transpose(-24) >> BrushingSaw),
            Scene("Xtremities", Xtremities),
            Scene("BagPipe", BagPipe),
            Scene("Borealis", Borealis),
            Scene("FifthAtmAft", FifthAtmAft),
            Scene("RichChoir", RichChoir),
            Scene("CircularPad", CircularPad),
            Scene("Oxigenizer", Oxigenizer),
            Scene("Quasar", Quasar),
            Scene("HellSection", HellSection),
            Scene("Itopia", Itopia),
            Scene("Kalimba", Kalimba),
            Scene("Dog", Dog),
            Scene("Siren", Siren),
            Scene("Explosion", Explosion),
            Scene("Thunder", Thunder),
            Scene("DoorCreak", DoorCreak),
            Scene("Laughing", Laughing),
            Scene("Applause", Applause),
            Scene("Telephone2", Telephone2),
            Scene("Rain", Rain),
            Scene("Drums", Amb_Room),
        ]),
    8: SceneGroup("Libre",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
        ]),
    9: SceneGroup("MP3Player",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("TV", init_patch=Call(Playlist()), patch=Discard()),
            Scene("GraceUnderPressure", init_patch=Call(Playlist()), patch=Discard()),
            Scene("Hits", init_patch=Call(Playlist()), patch=Discard()),
            Scene("Majestyx", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Middleage", init_patch=Call(Playlist()), patch=Discard()),
            Scene("NinaHagen", init_patch=Call(Playlist()), patch=Discard()),            
            Scene("PowerWindows", init_patch=Call(Playlist()), patch=Discard()),
            Scene("SteveMorse", init_patch=Call(Playlist()), patch=Discard()),
        ]),
    10: SceneGroup("Spotify", 
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Rush", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch=Discard(),  init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Studio.Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Studio.Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Studio.Demon", init_patch=HueDemon, patch=Discard()),
            Scene("Studio.SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Studio.Detente", init_patch=HueDetente, patch=Discard()),
            Scene("Studio.Veilleuse", init_patch=HueVeilleuse, patch=Discard()),
            Scene("Studio.Lecture", init_patch=HueLecture, patch=Discard()),
            Scene("Studio.FullBlanc", init_patch=HueSsFullBlanc, patch=Discard()),
            Scene("Cuisine.Minimal", init_patch=HueCuisine, patch=Discard()),
            Scene("Chambre.Minimal", init_patch=HueChambreMaitre, patch=Discard()),
            Scene("AllOff", init_patch=HueAllOff, patch=Discard()),
        ]),
    12: SceneGroup("Libre",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
        ]),
    13: SceneGroup("SD90-BANK",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Special1", init_patch=SP1, patch=Discard()),
            Scene("Special2", init_patch=SP2, patch=Discard()),
            Scene("Classical", init_patch=CLASIC, patch=Discard()),
            Scene("Contemporary", init_patch=CONTEM, patch=Discard()),
            Scene("Solo", init_patch=SOLO, patch=Discard()),
            Scene("Enhanced", init_patch=ENHANC, patch=Discard()),
        ]),
    14: SceneGroup("MUSE",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Assassin", init_patch=P01A, patch=Discard()),
            Scene("Hysteria", init_patch=P01A, patch=Discard()),
            Scene("Cydonia", init_patch=P01A, patch=Discard()),
            Scene("Starlight", init_patch=P01A, patch=Discard()),
            Scene("Stockholm", init_patch=P01A, patch=Discard()),
        ]),

}

# PROD
pre  = ~Filter(SYSRT_CLOCK) >> ~ChannelFilter(8, 9, 11) 
post = Pass()

# DEBUG
#pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
#post = Print('output',portnames='out')

    
#
# Patches for the run().control patch
#

# TO REWORK
wip_controller = (Filter(CTRL) >>
    CtrlSplit({
         20: Call(NavigateToScene),
        100: Ctrl(sd90_port_a, 1, 7, EVENT_VALUE),
        101: Program(sd90_port_a, 1, EVENT_VALUE),
        102: Ctrl(sd90_port_b, 1, 7, EVENT_VALUE),
        103: Program(sd90_port_b, 1, EVENT_VALUE),
    })
)

gt10b_control = (Filter(CTRL) >>
    CtrlSplit({
          4: GT10B_Tuner,
          7: GT10B_Volume,
    }))

hd500_control = (Filter(CTRL) >>
    CtrlSplit({
          1: HD500_Expr1,
          2: HD500_Expr2,
         69: HD500_Tuner,
    }))

# Transport filter Filter for mp3 and spotify
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

key_mp3_control = transport_filter >> Call(Mp3Player("SD90"))
pk5_mp3_control = transport_filter >> Call(Mp3Player("SD90"))
mpk_vlc_control = Filter(NOTEON) >> Call(VlcPlayer())

# Spotify
spotify_control = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())


# SoundCraft UI
soundcraft_control=[
    Filter(NOTEON) >> Process(MidiMix()) >> [
        
        KeyFilter(1) >> Ctrl(0, EVENT_VALUE) >> mute_mono,
        KeyFilter(4) >> Ctrl(1, EVENT_VALUE) >> mute_mono,

        KeyFilter(7)  >> Ctrl(2, EVENT_VALUE) >> mute_stereo,
        KeyFilter(10) >> Ctrl(4, EVENT_VALUE) >> mute_stereo,
        KeyFilter(13) >> Ctrl(6, EVENT_VALUE) >> mute_stereo,

        KeyFilter(16) >> ui_line_mute,
        KeyFilter(19) >> ui_player_mute,
        
        KeyFilter(22) >> Discard(),

        Process(MidiMixLed())

    ],
    Filter(CTRL) >> [
        CtrlFilter(0,1) >> ui_standard_fx,
       
        CtrlFilter(2,3,4) >> CtrlSplit({
            2 : Pass(),
            3 : Ctrl(4, EVENT_VALUE),
            4 : Ctrl(6, EVENT_VALUE),
        }) >> ui_standard_stereo_eq,

        CtrlFilter(5) >> ui_line_mix_eq,
        CtrlFilter(6) >> ui_player_mix_eq,
        CtrlFilter(7) >> Discard(),
        CtrlFilter(100) >> ui_master,
    ],
]

# FlaskDings API control patch
flaskdings_uri = os.environ["FLASKDINGS"]
flaskdings_control = trigger_filter >> [
    KeyFilter(0) >> Call(HttpGet(flaskdings_uri + "prev_scene")),
    KeyFilter(2) >> Call(HttpGet(flaskdings_uri + "next_scene")),
]

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : pk5_mp3_control,
    }),
    mpk_port_a : ChannelSplit({
         8 : key_mp3_control,
        12 : mpk_vlc_control,
        13 : p_hue,
        14 : spotify_control,
        15 : hd500_control,
        16 : gt10b_control
    }),
    q49_midi : ChannelSplit({
         1 : flaskdings_control,
    }),
    mpk_port_b : ChannelSplit({
         4 : pk5_mp3_control,
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})


run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)

