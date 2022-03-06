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
        #('IN-1', '24:2'),
        #('IN-2', '24:3'),
        ('MPK-MIDI1', '28:0'),
        ('MPK-MIDI2', '28:1'),
        ('MPK-MIDI3', '28:2'),
        ('MPK-MIDI4', '28:3'),
        #('GT', '20:0'),
    ],
    out_ports=[
        ('MPK-MIDI1', '28:0'),
        ('MPK-MIDI2', '28:1'),
        ('MPK-MIDI3', '28:2'),
        ('MPK-MIDI4', '28:3'),
        #('PART-A', '24:0'),
        #('PART-B', '24:1'),
        #('OUT-1', '24:2'),
        #('OUT-2', '24:3'),
        #('GT', '20:0'),
    ],


)

#hook(
#    AutoRestart()
#)

#piano = Output('PART-A', channel=1, program=((96 * 128), 100))
_scenes = {
    1: Scene("Akai", patch=Port('MPK-MIDI3')),
    #1: Scene("Piano", init_patch=Ctrl('OUT-2',1,3,67), patch=piano),
}

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

run(
    scenes=_scenes,
    pre=_pre,
    post=_post,
)
