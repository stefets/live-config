#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

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

# Port name alias
midimix_midi = "midimix"

q49_midi     = "q49_midi"

behringer    = "behringer"

sd90_port_a  = "sd90_port_a"
sd90_port_b  = "sd90_port_b"
sd90_midi_1  = "sd90_midi_1"
sd90_midi_2  = "sd90_midi_2"

mpk_port_a   = "mpk_port_a"
mpk_port_b   = "mpk_port_b"
mpk_midi     = "mpk_midi"
mpk_remote   = "mpk_remote"
virtual      = "virtual"
rt_midi      = "rt_midi"

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
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port A.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),
        #(virtual,      '.*VirMIDI 31-0.*',),
        #(rt_midi,      '.*RtMidi output.*',),
    ],

    in_ports = [
        (midimix_midi, ".*MIDI Mix MIDI 1.*",),
        (sd90_port_a,  '.*SD-90 Part A.*'),
        (sd90_port_b,  '.*SD-90 Part B.*'),
        (sd90_midi_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_2,  '.*SD-90 MIDI 2.*',),
        (behringer,    '.*UMC204HD 192k MIDI 1.*'),
        (q49_midi,     '.*Q49 MIDI 1.*',),
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port A.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),
        #(virtual,      '.*VirMIDI 31-0.*',),
        #(rt_midi,      '.*RtMidi output.*',),
    ],
)

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene(".hook.memorize_scene")
)

_pre_patch  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
_post_patch = Print('output',portnames='out')

# TODO Not working fine
EQ_Low = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,20,21,08,00,00,00,25,f7", 13, 6)

run(
    control=Pass(),
    scenes = {1:Scene("Debug", init_patch=Pass(), patch=Pass())},
    pre=_pre_patch,
    post=_post_patch,
)

