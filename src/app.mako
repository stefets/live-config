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
from extensions.hd500 import *

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
% for element in patches:
    % with open(element, 'r') as file:
        ${file.read()}
    % endwith
% endfor

# Scenes
% with open(scenes, 'r') as file:
    ${file.read()}
% endwith

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
