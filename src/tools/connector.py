#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# SCRIPT TO SETUP THE IN/OUT PORTS ONLY
#

from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.inotify import *

config(
    in_ports=[
        ('MPK-MIDI1', '32:0'),
        ('MPK-MIDI2', '32:1'),
        ('MPK-MIDI3', '32:2'),
        ('MPK-MIDI4', '32:3'),
        #('MIDI-MIX', '28:0'),
        #('PART-A', '36:0'),
        #('PART-B', '36:1'),

    ],
    out_ports=[
        ('MPK-MIDI1', '32:0'),
        ('MPK-MIDI2', '32:1'),
        ('MPK-MIDI3', '32:2'),
        ('MPK-MIDI4', '32:3'),
        #('MIDI-MIX', '28:0'),
        #('PART-A', '36:0'),
        #('PART-B', '36:1'),

    ],
)

hook(
    AutoRestart()
)

#_pre = ~Filter(SYSRT_CLOCK) 
_pre =  ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in')
_post = Print('output', portnames='out')
_control=Pass()

_scenes = {
    1: Scene("Test", patch=Pass()),
}


run(
    control=_control,
    scenes=_scenes,
    pre=_pre,
    post=_post
)
