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

config(

    client_name='SD-90',
    backend='alsa',

    in_ports=[
        ('IN0', '20:0'),
        ('IN1', '20:1'),
        ('IN2', '20:2'),
        ('IN3', '20:3'),
        # ('Q49', '24:0'),
    ],

    out_ports=[('OUT', '20:0'), ],  # MIDI OUTPUT

)

piano = Output('OUT', channel=1, program=((96 * 128), 1))
_scenes = {
    1: Scene("Piano", piano),
    2: Scene("Piano2", piano)
}

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

run(
    scenes=_scenes,
    pre=_pre,
    post=_post
)
