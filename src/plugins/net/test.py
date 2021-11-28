#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Script to develop patches
#

from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.inotify import *

# Plugin
from request import *

config(
     in_ports=[
         ('Q49', '28:0'),
     ],
     out_ports=[
     ],
)

hook(
    AutoRestart(),
)

p_test=Filter(NOTEON) >> Transpose(-36) >> Call(RequestGet("http://127.0.0.1:5003/api/mididings/scenes/{}"))
_scenes = {
    1: Scene("Test", init_patch=Discard(), patch=p_test)
}

run(
    scenes=_scenes,
    pre=Print('input', portnames='in'),
    post=Print('output',portnames='out')
)
