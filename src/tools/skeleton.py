#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import json
from threading import Timer
from time import sleep

#from mididings.extra import *
from mididings.extra.osc import *
#from mididings import engine
from mididings.extra.inotify import *
#from mididings.event import PitchbendEvent, MidiEvent, NoteOnEvent, NoteOffEvent
#from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene, output_event

# Setup path
sys.path.append(os.path.realpath('.'))

# Environment
from dotenv import load_dotenv
load_dotenv()

#region HELPERS
def OnDebug(ev):
    print(ev)
#endregion HELPERS

# Port name alias
sd90_port_a  = "sd90_port_a"
sd90_port_b  = "sd90_port_b"
sd90_midi_1  = "sd90_midi_1"
sd90_midi_2  = "sd90_midi_2"
behringer    = "behringer"
mpk_port_a   = "mpk_port_a"
mpk_port_b   = "mpk_port_b"
mpk_midi     = "mpk_midi"
mpk_remote   = "mpk_remote"
q49_midi     = "q49_midi"
gt10b_midi   = "gt10b_midi"
midimix_midi = "midimix"

config(

    # Defaults
    # initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    out_ports = [

        (midimix_midi,'__MIDI Mix MIDI 1__',),  
        (sd90_port_a, '__SD-90 Part A__'),
        (sd90_port_b, '__SD-90 Part B__'),
        (sd90_midi_1, '__SD-90 MIDI 1__',),
        (sd90_midi_2, '__SD-90 MIDI 2__',),
        (behringer,   '__UMC204HD 192k MIDI 1__'),
        (q49_midi,    '__Q49 MIDI 1__',),
        (gt10b_midi,  '__GT-10B MIDI 1__',),
        (mpk_port_a,  '__MPK249 Port A__',),
        (mpk_port_b,  '__MPK249 Port B__',),
        (mpk_midi,    '__MPK249 MIDI__',),
        (mpk_remote,  '__MPK249 Remote__',),

    ],

    in_ports = [

        (midimix_midi,'__MIDI Mix MIDI 1__',),
        (sd90_port_a, '__SD-90 Part A__'),
        (sd90_port_b, '__SD-90 Part B__'),
        (sd90_midi_1, '__SD-90 MIDI 1__',),
        (sd90_midi_2, '__SD-90 MIDI 2__',),
        (behringer,   '__UMC204HD 192k MIDI 1__'),
        (q49_midi,    '__Q49 MIDI 1__',),
        (gt10b_midi,  '__GT-10B MIDI 1__',),
        (mpk_port_a,  '__MPK249 Port A__',),
        (mpk_port_b,  '__MPK249 Port B__',),
        (mpk_midi,    '__MPK249 MIDI__',),
        (mpk_remote,  '__MPK249 Remote__',),

    ],

)

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene(".hook.memorize_scene")
)

_scenes = {
    1: Scene("Test", patch=Pass()),
}


# pre/post
_pre  = Print('input', portnames='in')
_post = Print('output', portnames='out')

#
run(
    control=Pass(),
    scenes=_scenes,
    pre=_pre,
    post=_post
)
