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
    in_ports= [('MIDIMIX', '40:0'),],
    out_ports=[('MIDIMIX', '40:0'),],
)

hook(AutoRestart())

pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
post = Print('output', portnames='out')
control=Pass()

midimix=Filter(NOTEON) >> Process(MidiMix())

scenes = {
    1: Scene("Test", patch=midimix),
}

run(
    control=control,
    scenes=scenes,
    pre=pre,
    post=post,
)
