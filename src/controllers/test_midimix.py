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

from midimix import *


config(
    in_ports= [('MIDIMIX', '28:0'),],
    out_ports=[('MIDIMIX', '28:0'),],
)

hook(AutoRestart())

_pre =  Print('input', portnames='in')
_post = Print('output', portnames='out')
_control=Pass()

midimix=Filter(NOTEON) >> Process(MidiMix())

_scenes = {
    1: Scene("Test", patch=midimix),
}

run(
    control=_control,
    scenes=_scenes,
    pre=_pre,
    post=_post,
)
