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
graviton     = "graviton"

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
        (graviton,     '.*Graviton USB-MIDI MIDI 1.*',),
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
        (graviton,     '.*Graviton USB-MIDI MIDI 1.*',),
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


# Audio FX
MasteringEffect = SysEx(sd90_port_a,"f0,41,10,00,48,12,02,10,20,00,78,56,f7")
AfxOn  = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,11,43,01,19,f7")
AfxOff = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,11,43,00,1a,f7")

# Audio Mixer
MixToAfx = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,10,00,06,58,f7")

# Audio Level Control
WaveLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,20,00,3f,f7", 10, 6)
InstLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,30,00,3f,f7", 10, 6)
MicGtLevel = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,00,00,3f,f7", 10, 6)

# SD-90 Bank Patch
SP1  =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,50,00,00,7c,f7")
SP2  =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,51,00,00,7b,f7")
CLASIC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,60,00,00,6c,f7")
CONTEM = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,61,00,00,6b,f7")
SOLO =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,62,00,00,6a,f7")
ENHANC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,63,00,00,69,f7")

SD90_Initialize = [
    Reset, 
    MasteringEffect,
    MixToAfx,
    AfxOn, 
    InitPitchBend, 
]

        
#
# The Boss GT-10B definition file for mididings
# This device has 4 banks, each bank contains 100 programs 
#

# Internal Midi channel configured in the GT10B USB options
GT10BChannel = 16

GT10BankSelector = CtrlValueFilter(0, 3) >> [
      Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE), 
      Ctrl(gt10b_midi, GT10BChannel, 32, 0),
]
GT10Bank0 = Ctrl(0, 0) >> GT10BankSelector
GT10Bank1 = Ctrl(0, 1) >> GT10BankSelector
GT10Bank2 = Ctrl(0, 2) >> GT10BankSelector
GT10Bank3 = Ctrl(0, 3) >> GT10BankSelector

GT10BProgramSelector = Program(gt10b_midi, channel = GT10BChannel, program = EVENT_VALUE)

# Send CC
GT10B_Ctrl =  Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)

# Send CC aliases
GT10B_Tuner = Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)    
GT10B_Volume = GT10B_Ctrl
GT10B_Expression = GT10B_Ctrl

# Mididings control patch
gt10b_control = (Filter(CTRL) >> 
    CtrlSplit({
          4: GT10B_Tuner,
          7: GT10B_Volume,
         20: GT10BProgramSelector
    }))
        
#
# The Line 6 POD-HD-500 definition patches for mididings
#

# Listen channel
hd500_channel = 15

# Connecté a quel port MIDI ?
hd500_port = mpk_midi

# Programmes
HD500ProgramSelector = Program(hd500_port, channel = hd500_channel, program = EVENT_VALUE)

# Abstract patch (must be chained before by a Ctrl(c,v))
# Example: 
#       Ctrl(69, 127) >> CtrlPod will set the tuner on.
# mean  Ctrl(hd500_port, hd500_channel, 69, 127)
CtrlPodBase = Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)

# Footswitch
FS1 = Ctrl(51, 64) >> CtrlPodBase
FS2 = Ctrl(52, 64) >> CtrlPodBase
FS3 = Ctrl(53, 64) >> CtrlPodBase
FS4 = Ctrl(54, 64) >> CtrlPodBase
FS5 = Ctrl(55, 64) >> CtrlPodBase
FS6 = Ctrl(56, 64) >> CtrlPodBase
FS7 = Ctrl(57, 64) >> CtrlPodBase
FS8 = Ctrl(58, 64) >> CtrlPodBase
TOE = Ctrl(59, 64) >> CtrlPodBase

# Exp1 et Exp2
HD500_Expr1 = Ctrl(1, EVENT_VALUE) >> CtrlPodBase
HD500_Expr2 = Ctrl(2, EVENT_VALUE) >> CtrlPodBase

# HD500_Tuner (shortcut)
HD500_Tuner = CtrlPodBase

HD500_TunerOn  = Ctrl(hd500_port, hd500_channel, 69, 127)
HD500_TunerOff = Ctrl(hd500_port, hd500_channel, 69, 0)

# Looper
HD500_Looper = CtrlFilter(60, 61, 62, 63, 65, 67, 68, 99) >> CtrlPodBase

# Tap
# Expected EVENT_VALUE between 64 and 127
HD500_Tap = Ctrl(hd500_port, hd500_channel, 64, EVENT_VALUE)

# Mididings HD500 control patch
hd500_control = (Filter(CTRL) >>
    CtrlSplit({
          1: HD500_Expr1,
          2: HD500_Expr2,
         69: HD500_Tuner,
         20: HD500ProgramSelector
    }))
        
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

def cursor_value_converter(ev):
    return ev.data2 * ratio

def ui_knob(ev):
    return cursor_value_converter(ev)

def mute_value_converter(ev):
    return 1 if ev.data2==127 else 0

''' Return the controller value for SendOsc '''
def event_value_converter(ev, offset=0):
    return ev.ctrl+offset if ev.type == CTRL else -1

''' Wrapper over ui_event '''
def ui_left(ev):
    return event_value_converter(ev)

''' Wrapper over ui_event '''
def ui_right(ev):
    return event_value_converter(ev, 1)


# Osc Soundcraft Bridge definition
osb_port = 56420
mix_path = "/mix"
mute_path = "/mute"
master_path = "/master"

mute_room_path = "/room/mute"
mute_delay_path = "/delay/mute"
mute_chorus_path = "/chorus/mute"
mute_reverb_path = "/reverb/mute"

room_path = "/room"
delay_path = "/delay"
chorus_path = "/chorus"
reverb_path = "/reverb"

rectoggle_path= "/rectoggle"

bass_path = "/bass"
mid_path = "/mid"
treble_path = "/treble"


# Main volume
ui_master=SendOSC(osb_port, master_path, cursor_value_converter)

# Mono patches / stands for all XLR+1/4 sockets
# Stereo patches must target left channel, right channel will change in the same time
mix_mono = SendOSC(osb_port, mix_path,  event_value_converter, cursor_value_converter, "i")
mix_stereo = [
        SendOSC(osb_port, mix_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, mix_path, ui_right, cursor_value_converter, "i"),
    ]

reverb_mono = SendOSC(osb_port, reverb_path,  event_value_converter, cursor_value_converter, "i")
reverb_stereo = [
        SendOSC(osb_port, reverb_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, reverb_path, ui_right, cursor_value_converter, "i"),
    ]

chorus_mono = SendOSC(osb_port, chorus_path,  event_value_converter, cursor_value_converter, "i")
chorus_stereo = [
        SendOSC(osb_port, chorus_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, chorus_path, ui_right, cursor_value_converter, "i"),
    ]

delay_mono = SendOSC(osb_port, delay_path,  event_value_converter, cursor_value_converter, "i")
delay_stereo = [
        SendOSC(osb_port, delay_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, delay_path, ui_right, cursor_value_converter, "i"),
    ]

room_mono = SendOSC(osb_port, room_path,  event_value_converter, cursor_value_converter, "i")
room_stereo = [
        SendOSC(osb_port, room_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, room_path, ui_right, cursor_value_converter, "i"),
    ]

mute_mono = SendOSC(osb_port, mute_path, event_value_converter, mute_value_converter, "i")
mute_stereo = [
        SendOSC(osb_port, mute_path, ui_left,  mute_value_converter, "i"),    
        SendOSC(osb_port, mute_path, ui_right, mute_value_converter, "i"),
    ]

mute_reverb_mono = SendOSC(osb_port, mute_reverb_path, event_value_converter, mute_value_converter, "i")
mute_delay_mono = SendOSC(osb_port, mute_delay_path, event_value_converter, mute_value_converter, "i")
mute_chorus_mono = SendOSC(osb_port, mute_chorus_path, event_value_converter, mute_value_converter, "i")
mute_room_mono = SendOSC(osb_port, mute_room_path, event_value_converter, mute_value_converter, "i")

mute_delay_stereo = [
    SendOSC(osb_port, mute_delay_path, ui_left, mute_value_converter, "i"),
    SendOSC(osb_port, mute_delay_path, ui_right, mute_value_converter, "i"),
]

# Equalizer
bass_mono = SendOSC(osb_port, bass_path, event_value_converter, cursor_value_converter, "i")
bass_stereo = [
        SendOSC(osb_port, bass_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, bass_path, ui_right, cursor_value_converter, "i"),
    ]

mid_mono = SendOSC(osb_port, mid_path, event_value_converter, cursor_value_converter, "i")
mid_stereo = [
        SendOSC(osb_port, mid_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, mid_path, ui_right, cursor_value_converter, "i"),
    ]

treble_mono = SendOSC(osb_port, treble_path, event_value_converter, cursor_value_converter, "i")
treble_stereo = [
        SendOSC(osb_port, treble_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, treble_path, ui_right, cursor_value_converter, "i"),
    ]


# Static stereo inputs
# Line patches
ui_line_mute=[
        SendOSC(osb_port, mute_path, 0, mute_value_converter, "l"),    
        SendOSC(osb_port, mute_path, 1, mute_value_converter, "l"),
    ]
    
ui_line_mix=[
        SendOSC(osb_port, mix_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, mix_path, 1, cursor_value_converter, "l"),
    ]

line_bass = [
        SendOSC(osb_port, bass_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, bass_path, 1, cursor_value_converter, "l"),
    ]
line_mid = [
        SendOSC(osb_port, mid_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, mid_path, 1, cursor_value_converter, "l"),
    ]
line_treble = [
        SendOSC(osb_port, treble_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, treble_path, 1, cursor_value_converter, "l"),
    ]

# Player patches
ui_player_mute=[
        SendOSC(osb_port, mute_path, 0, mute_value_converter, "p"),    
        SendOSC(osb_port, mute_path, 1, mute_value_converter, "p"),
    ]
    
ui_player_mix=[
        SendOSC(osb_port, mix_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, mix_path, 1, cursor_value_converter, "p"),
    ]

player_bass = [
        SendOSC(osb_port, bass_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, bass_path, 1, cursor_value_converter, "p"),
    ]
player_mid = [
        SendOSC(osb_port, mid_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, mid_path, 1, cursor_value_converter, "p"),
    ]
player_treble = [
        SendOSC(osb_port, treble_path, 0, cursor_value_converter, "p"),
        SendOSC(osb_port, treble_path, 1, cursor_value_converter, "p"),
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

ui_rectoggle = SendOSC(osb_port, rectoggle_path) 

# Mididings SoundCraft UI control patch
soundcraft_control=[Filter(NOTEON) >> 
                    
        Process(MidiMix()) >> [
        
        KeyFilter(1) >> Ctrl(0, EVENT_VALUE) >> mute_mono,
        KeyFilter(2) >> Pass(),
        KeyFilter(3) >> Pass(),

        KeyFilter(4) >> Ctrl(1, EVENT_VALUE) >> mute_mono,
        KeyFilter(5) >> Pass(),
        KeyFilter(6) >> Pass(),


        KeyFilter(7)  >> Ctrl(2, EVENT_VALUE) >> mute_stereo,
        KeyFilter(9)  >> Ctrl(2, EVENT_VALUE) >> mute_delay_stereo,
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

# Setup controllers
cw_rew  = 115
cw_fwd  = 116
cw_stop = 117
cw_play = 118
cw_rec  = 119

# Allowed controllers
ctrls = [cw_rec, cw_stop, cw_play, cw_rec, cw_fwd]

# Trigger value
cw_trigger_value = 127

# Listen channel
cw_channel = 1

# Output port
cw_port = sd90_midi_2

# ---------------

# Execution patches
CakewalkController = CtrlFilter(ctrls) >> Ctrl(cw_port, cw_channel, EVENT_CTRL, cw_trigger_value) 

# Direct DAW patch
CakeStop   = Ctrl(cw_stop, EVENT_VALUE) >> CakewalkController
CakePlay   = Ctrl(cw_play, EVENT_VALUE) >> CakewalkController
CakeRecord = Ctrl(cw_rec,  EVENT_VALUE) >> CakewalkController

# WIP
CakeRewind = Ctrl(cw_rew, EVENT_VALUE) >> CakewalkController
CakeForward= Ctrl(cw_fwd, EVENT_VALUE) >> CakewalkController

        
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


# Base patches (WIP)
p_hd500_filter_base = [
    (KeyFilter(notes=[65]) >> FS1),
    (KeyFilter(notes=[67]) >> FS2),
    (KeyFilter(notes=[69]) >> FS3),
    (KeyFilter(notes=[71]) >> FS4),
]

p_hue_live = [
    KeyFilter(notes=[61]) >> HueStudioOff,
    KeyFilter(notes=[63]) >> HueNormal,
    KeyFilter(notes=[66]) >> HueGalaxie,
    KeyFilter(notes=[68]) >> HueGalaxieMax,
    KeyFilter(notes=[70]) >> HueDemon,
]

p_base = [
    p_hue_live,
    p_hd500_filter_base, 
]

p_pk5ctrl_generic = pk5 >> Filter(NOTEON)

# 

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
# Init patch - set HD500 to patch 14A
i_big_country = [Program(53) >> HD500ProgramSelector]

# Execution patch
p_big_country = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[65]) >> FS1),
             (KeyFilter(notes=[67]) >> FS2),
             #(KeyFilter(notes=[69]) >> FS3),
             (KeyFilter(notes=[69]) >> FS4),
             (KeyFilter(notes=[71]) >> [HueGalaxie, FS2, Ctrl(3,85)  >> HD500_Expr2]),
             (KeyFilter(notes=[72]) >> [HueSoloRed, FS2, Ctrl(3,127) >> HD500_Expr2])
         ])

p_big_country = p_pk5ctrl_generic >> [
    p_base,
    (KeyFilter(notes=[66]) >> [HueGalaxie, FS2, Ctrl(3,85) >> HD500_Expr2]),
    (KeyFilter(notes=[67]) >> [HueSoloRed, Ctrl(3,127) >> HD500_Expr2])
]

# Song : In a big country - recording
i_big_country_live = []
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
i_octobre = []

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
i_rush = [Program(5) >> HD500ProgramSelector, Ctrl(3,100) >> HD500_Expr2]

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
i_rush_sub=[Program(5) >> HD500ProgramSelector, FS3, Ctrl(3,100) >> HD500_Expr2]

# Grand Designs

# Init patch
i_rush_gd = [Program(5) >> HD500ProgramSelector, FS1, FS3, Ctrl(3,127) >> HD500_Expr2] 

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
i_rush_trees = [Program(5) >> HD500ProgramSelector, FS3, Ctrl(3,100) >> HD500_Expr2] 

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

# Muse Band
p_muse = p_pk5ctrl_generic >> p_base
p_muse_stockholm = pk5 >> [
    KeyFilter(notes=[60]) >> [
        Key('d2') >> Harmonize('d', 'major', ['unison', 'octave']),
        HueDemon
    ],
    KeyFilter(notes=[62]) >> [
        Key('e2') >> Harmonize('e', 'major', ['unison', 'octave']),
        HueGalaxieMax
    ],
    KeyFilter(notes=[64]) >> [
        Key('f2') >> Harmonize('f', 'major', ['unison', 'octave']),
        HueGalaxie
    ],
] >> Velocity(fixed=127) >> Output(sd90_port_b, channel=14, program=(Special2,106), volume=127, ctrls={93:75, 91:75})


p_rush = p_pk5ctrl_generic >> p_base

p_wonderland_init = [
    Ctrl(mpk_port_a, 3, 2, 64) >> ui_standard_stereo_fx,
    Program(56) >> HD500ProgramSelector
]
p_wonderland = p_pk5ctrl_generic >> [
     p_base,
     KeyFilter(72) >> NoteOn(9, 127) >> Port(midimix_midi) >> soundcraft_control,
]

# ---
# Daw + Hue helper for recording
p_transport = (pk5 >> [
            p_hue_live,
            Filter(NOTEON)  >> KeyFilter(notes=[60])    >> [CakePlay],
            Filter(NOTEON)  >> KeyFilter(notes=[62])    >> [CakeRecord],
            Filter(NOTEOFF) >> KeyFilter(notes=[60,62]) >> [HueGalaxieMax], 
        ])

# Interlude patch, between two songs
interlude = mpk_b >> ChannelFilter(16) >> KeyFilter(notes=[0,49]) >> Velocity(fixed=50) >> LatchNotes(reset=0) >> [Oxigenizer]

# Glissando
p_glissando=(Filter(NOTEON) >> Call(glissando, 48, 84, 100, 0.01, -1, sd90_port_a))

        
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

# VLC player - Singleton
VLC_BASE = Filter(NOTEON) >> Call(VlcPlayer())

# Playlist
VLC_PL   = NoteOn(EVENT_DATA1, 0) >> VLC_BASE

# Commands
VLC_STOP  = NoteOn(37, 0) >> VLC_BASE
VLC_PLAY  = NoteOn(39, 0) >> VLC_BASE
VLC_PAUSE = NoteOn(44, 0) >> VLC_BASE
VLC_REPEAT_ON     = NoteOn(43, 0)  >> VLC_BASE
VLC_REPEAT_OFF    = NoteOn(45, 0)  >> VLC_BASE
VLC_TOGGLE_LOOP   = NoteOn(127, 0) >> VLC_BASE
VLC_TOGGLE_REPEAT = NoteOn(126, 0) >> VLC_BASE

# MPG123 multiple instances allow me to play sounds in parallal (dmix)
#MPG123_GT10B  = Call(Mp3Player("GT10B"))
MPG123_U192k  = Call(Mp3Player("U192k"))
MPG123_SD90_A = Call(Mp3Player("SD90"))
MPG123_SD90_B = Call(Mp3Player("SD90"))
# Playlist according to current scene, a singleton is enough
MPG123_PLAYLIST = Call(Playlist())

        
#
# Patches for the run().control patch
#

# Transport filter Filter for MPG123 and Spotipy and VLC
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

key_mp3_control = transport_filter >> MPG123_SD90_A
pk5_mp3_control = transport_filter >> MPG123_SD90_B
q49_mp3_control = transport_filter >> MPG123_U192k
mpk_vlc_control = trigger_filter >> VLC_BASE
q49_vlc_control = trigger_filter >> VLC_BASE

# Spotify
spotify_control = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())

mpk_soundcraft_control=Filter(CTRL|NOTE) >> [
        Filter(CTRL) >> Pass(),
        Filter(NOTE) >> NoteOn(EVENT_NOTE, 127) >> Port(midimix_midi),
    ] >> soundcraft_control

# FCB1010 to MPK249-Midi IN and MPK OUT to POD HD500 IN
fcb1010_control = [
    (CtrlFilter(1, 2, 51, 52, 53, 54, 69) >> CtrlPodBase),
    (CtrlFilter(20) >> CtrlValueSplit({
          1: [CakePlay, HueGalaxie],
          2: [CakeStop, HueNormal],
          3: [CakeRecord, HueGalaxie],
          4: [CakeRecord, HueGalaxieMax],
    }))
]

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : pk5_mp3_control,
        15 : fcb1010_control
    }),
    mpk_port_a : ChannelSplit({
         1 : mpk_soundcraft_control,
         8 : key_mp3_control,
        11 : (Channel(16) >> CtrlMap(11, 7) >> GT10B_Volume),  # Akai MPK249 Expression pedal
        12 : mpk_vlc_control,
        13 : p_hue,
        #14 : spotify_control,
        15 : hd500_control,
        16 : gt10b_control
    }),
    mpk_port_b : ChannelSplit({
         1 : CakewalkController,                # patches/cakewalk.py
         4 : pk5_mp3_control,
        11 : HD500_Expr1,             # Akai MPK249 Expression pedal
    }),
    q49_midi : ChannelSplit({
         1 : q49_mp3_control,
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})


# Scenes
    
_scenes = {
    1: Scene("Initialize All", init_patch = SD90_Initialize, patch = Discard()),
    2: SceneGroup("Rush", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Generic", init_patch = MPG123_PLAYLIST, patch = Discard()//p_rush),
            Scene("Subdivisions", init_patch = i_rush_sub//MPG123_PLAYLIST, patch = Discard()//p_rush),
            Scene("TheTrees", init_patch = i_rush_trees//MPG123_PLAYLIST, patch = Discard()//p_rush_trees),
            Scene("Grand Designs", init_patch = i_rush_gd, patch = Discard()//p_rush_gd),
            Scene("Marathon", init_patch = i_rush, patch = Discard()),
            Scene("YYZ", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("Limelight", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("FlyByNight", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("RedBarchetta", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("Freewill", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("SpritOfRadio", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("TomSawyer", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("CloserToTheHeart", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
        ]),
    3: SceneGroup("BassCover", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Default", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Queen", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("T4F", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Toto", init_patch = MPG123_PLAYLIST, patch = Discard()),
        ]),
    4: SceneGroup("Recording", [
            Scene("Bass", init_patch = Discard(), patch = p_transport),
        ]),
    5: SceneGroup("BigCountry", [
            Scene("BassCover", init_patch = MPG123_PLAYLIST//Discard(), patch = Discard()),
            Scene("InBigCountry", init_patch = i_big_country, patch = p_big_country),
            Scene("HighlandScenery", init_patch = Discard(), patch = p_highland_scenery),
            Scene("Inwards", init_patch = Discard(), patch = p_pk5ctrl_generic>>p_base),
            Scene("AnglePark", init_patch = Discard(), patch = p_pk5ctrl_generic>>p_base),
            Scene("Wonderland", init_patch = p_wonderland_init, patch = p_wonderland),
        ]),
    6: SceneGroup("GrandDesignsStudio", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = p_rush_gd_demo),
            Scene("Futur", init_patch = Discard(), patch = p_transport),
        ]),
    7: SceneGroup("Keyboard", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Init SD90", init_patch = SD90_Initialize, patch = Discard()),
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
            Scene("NatureSound", akai_pad_nature),
        ]),
    8: SceneGroup("Cakewalk", [ 
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Play", init_patch = CakePlay, patch = Discard()),
            Scene("Stop", init_patch = CakeStop, patch = Discard()),
            Scene("Record", init_patch = CakeRecord, patch = Discard()),
            Scene("Rewind", init_patch = CakeRewind, patch = Discard()),
            Scene("Forward", init_patch = CakeForward, patch = Discard()),
        ]),
    9: SceneGroup("MP3Player", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Hits", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Middleage", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("TV", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("NinaHagen", init_patch = MPG123_PLAYLIST, patch = Discard()),            
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("GraceUnderPressure", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("SteveMorse", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Colocs", init_patch = MPG123_PLAYLIST, patch = Discard()),
        ]),
    10: SceneGroup("Spotify", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Rush", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch = Discard(),  init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Studio.Normal", init_patch = HueNormal, patch = Discard()),
            Scene("Studio.Galaxie", init_patch = HueGalaxie, patch = Discard()),
            Scene("Studio.Demon", init_patch = HueDemon, patch = Discard()),
            Scene("Studio.SoloRed", init_patch = HueSoloRed, patch = Discard()),
            Scene("Studio.Detente", init_patch = HueDetente, patch = Discard()),
            Scene("Studio.Veilleuse", init_patch = HueVeilleuse, patch = Discard()),
            Scene("Studio.Lecture", init_patch = HueLecture, patch = Discard()),
            Scene("Studio.FullBlanc", init_patch = HueSsFullBlanc, patch = Discard()),
            Scene("Cuisine.Minimal", init_patch = HueCuisine, patch = Discard()),
            Scene("Chambre.Minimal", init_patch = HueChambreMaitre, patch = Discard()),
            Scene("AllOff", init_patch = HueAllOff, patch = Discard()),
        ]),
    12: SceneGroup("SoundcraftUI", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Record", init_patch = ui_rectoggle, patch = Discard()),
        
        ]),
    13: SceneGroup("SD90", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Init SD90", init_patch = SD90_Initialize, patch = Discard()),
            Scene("Special1", init_patch = SP1, patch = Discard()),
            Scene("Special2", init_patch = SP2, patch = Discard()),
            Scene("Classical", init_patch = CLASIC, patch = Discard()),
            Scene("Contemporary", init_patch = CONTEM, patch = Discard()),
            Scene("Solo", init_patch = SOLO, patch = Discard()),
            Scene("Enhanced", init_patch = ENHANC, patch = Discard()),
        ]),
    14: SceneGroup("MUSE", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Assassin", init_patch = Discard(), patch = p_muse),
            Scene("Hysteria", init_patch = Discard(), patch = p_muse),
            Scene("Cydonia",  init_patch = Discard(), patch = p_muse),
            Scene("Starlight", init_patch = Discard(), patch = p_muse),
            Scene("Stockholm", init_patch = Discard(), patch = [p_muse_stockholm, p_muse]),
        ]),
    15:  SceneGroup("Sampler", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Track1", init_patch = Discard(), patch = Discard()),
        ]),
    16:  SceneGroup("POC", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("INTERLUDE", patch = pk5 >> Filter(NOTEON) >> NoteOn(0, 0) >> VLC_PL, init_patch = Pass()),

        ]),
    17:  SceneGroup("VLC", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Stop", init_patch = VLC_STOP, patch = Discard()),
            Scene("Play", init_patch = VLC_PLAY, patch = Discard()),
            Scene("Pause", init_patch = VLC_PAUSE, patch = Discard()),
            Scene("Repeat-ON", init_patch =  VLC_REPEAT_ON, patch = Pass()),
            Scene("Repeat-OFF", init_patch = VLC_REPEAT_OFF, patch = Pass ()),
            Scene("Toggle-Loop", init_patch = VLC_TOGGLE_LOOP, patch = Pass ()),
            Scene("Toggle-Repeat", init_patch = VLC_TOGGLE_REPEAT, patch = Pass ()),
            Scene("Playlist item 1", init_patch = NoteOn(0, 0) >> VLC_PL, patch = Discard()),
            Scene("Playlist item 2", init_patch = Ctrl(1, 0) >> VLC_PL, patch = Discard()),
        ]),        
    18:  SceneGroup("GT10B", [
            Scene("Select a Bank", init_patch = Discard(), patch = Discard()),
            Scene("U01_A", init_patch = [GT10Bank0, Program(1) >> GT10BProgramSelector], patch = Discard()),
            Scene("U01_B", init_patch = [GT10Bank0, Program(2) >> GT10BProgramSelector], patch = Discard()),
    ]),
    19:  SceneGroup("HD500", [
            Scene("Select option", init_patch = Discard(), patch = Discard()),
            Scene("FS1", init_patch = [FS1], patch = Discard()),
            Scene("FS2", init_patch = [FS2], patch = Discard()),
    ]),    
    20:  SceneGroup("Futur", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
    ]),    
}


# PROD
pre  = ~Filter(SYSRT_CLOCK) >> ~ChannelFilter(8, 9, 11) 
post = Pass()

# DEBUG
#pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
#post = Print('output',portnames='out')

run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)

