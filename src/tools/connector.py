#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Script for POC
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
        ('MIDI-MIX', '28:0'),
        ('PART-A', '36:0'),
        ('PART-B', '36:1'),
        ('PART-B', '36:2'),
        ('PART-B', '36:3'),

    ],
    out_ports=[
        ('MPK-MIDI1', '32:0'),
        ('MPK-MIDI2', '32:1'),
        ('MPK-MIDI3', '32:2'),
        ('MPK-MIDI4', '32:3'),
        ('MIDI-MIX', '28:0'),
        ('PART-A', '36:0'),
        ('PART-B', '36:1'),
        ('PART-B', '36:2'),
        ('PART-B', '36:3'),

    ],
)

hook(
    AutoRestart()
)

_pre  = Print('input', portnames='in')
_post = Print('output', portnames='out')


# 
value_index = 10
checksum_index = 6

pattern = "f0,41,10,00,48,12,02,10,11,00,00,3f,f7"

volume = Port('PART-A') >> CtrlToSysEx(7, pattern, value_index, checksum_index) 

_scenes = {
    1: Scene("Test", patch=volume),
}


run(
    control=Pass(),
    scenes=_scenes,
    pre=_pre,
    post=_post
)
