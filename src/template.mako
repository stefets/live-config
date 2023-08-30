#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Thanks to the programmer Dominic Sacre for that masterpiece
https://github.com/mididings/mididings (Maintained)
https://github.com/dsacre/mididings (Abandonned)
'''

import os
import sys
import json
from threading import Timer
from time import sleep

from mididings.extra import *
from mididings.extra.osc import *
from mididings import engine
from mididings.extra.inotify import *
from mididings.event import PitchbendEvent, MidiEvent, NoteOnEvent, NoteOffEvent
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene, output_event

# Setup path
sys.path.append(os.path.realpath('.'))

# Environment
from dotenv import load_dotenv
load_dotenv()

# Services
from services.mp3 import *
from services.vlc import *
from services.philips import *
from services.spotify import *
from services.midimix import *
from services.httpclient import *

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

    # __Ports__ are changed by live.sh with sed/awk
    out_ports = [

        (midimix_midi, "${midimix}",),  
        (sd90_port_a,  '__SD-90 Part A__'),
        (sd90_port_b,  '__SD-90 Part B__'),
        (sd90_midi_1,  '__SD-90 MIDI 1__',),
        (sd90_midi_2,  '__SD-90 MIDI 2__',),
        (behringer,    '__UMC204HD 192k MIDI 1__'),
        (q49_midi,     '__Q49 MIDI 1__',),
        (gt10b_midi,   '__GT-10B MIDI 1__',),
        (mpk_port_a,   '__MPK249 Port A__',),
        (mpk_port_b,   '__MPK249 Port B__',),
        (mpk_midi,     '__MPK249 MIDI__',),
        (mpk_remote,   '__MPK249 Remote__',),

    ],

    in_ports = [

        (midimix_midi, "${midimix}",),
        (sd90_port_a,  '__SD-90 Part A__'),
        (sd90_port_b,  '__SD-90 Part B__'),
        (sd90_midi_1,  '__SD-90 MIDI 1__',),
        (sd90_midi_2,  '__SD-90 MIDI 2__',),
        (behringer,    '__UMC204HD 192k MIDI 1__'),
        (q49_midi,     '__Q49 MIDI 1__',),
        (gt10b_midi,   '__GT-10B MIDI 1__',),
        (mpk_port_a,   '__MPK249 Port A__',),
        (mpk_port_b,   '__MPK249 Port B__',),
        (mpk_midi,     '__MPK249 MIDI__',),
        (mpk_remote,   '__MPK249 Remote__',),

    ],

)

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene("${memorize}")
)

# Patches and callable functions
% for element in body_definition:
    % with open(element, 'r') as file:
        ${file.read()}
    % endwith
% endfor

# Scenes
_scenes = {
% with open(scene_definition, 'r') as file:
    ${file.read()}
% endwith
}


# PROD
pre  = ~Filter(SYSRT_CLOCK) >> ~ChannelFilter(8, 9, 11) 
post = Pass()

# DEBUG
#pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
#post = Print('output',portnames='out')

% with open(control_definition, 'r') as file:
    ${file.read()}
% endwith

run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)
