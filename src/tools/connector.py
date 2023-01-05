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
        #('SD90-IN-1', '32:2'),
        #('SD90-IN-2', '32:3'),
        #('MPK-MIDI1', '28:0'),
        #('MPK-MIDI2', '28:1'),
        #('MPK-MIDI3', '28:2'),
        #('MPK-MIDI4', '28:3'),
        #('MIDI-MIX', '28:0'),
        ('PART-A', '36:0'),
        ('PART-B', '36:1'),

    ],
    out_ports=[
        #('MPK-MIDI1', '28:0'),
        #('MPK-MIDI2', '28:1'),
        #('MPK-MIDI3', '28:2'),
        #('MPK-MIDI4', '28:3'),

        ('PART-A', '36:0'),
        ('PART-B', '36:1'),

    ],
)

hook(
    AutoRestart()
)

#_pre = ~Filter(SYSRT_CLOCK) 
_pre =  Print('input', portnames='in')
_post = Print('output', portnames='out')
_control=Pass()

akai=[
        Filter(NOTEON) >> NoteOn(EVENT_NOTE, 0),
]

_scenes = {
    1: Scene("Test", patch=Pass()),
    #1: Scene("Akai", patch=~Filter() >> Port('MPK-MIDI3')),
    #1: Scene("Piano", init_patch=Ctrl('OUT-2',1,3,67), patch=piano),
}


run(
    control=_control,
    scenes=_scenes,
    pre=_pre,
    post=_post
)
