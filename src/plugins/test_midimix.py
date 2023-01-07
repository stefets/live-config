#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to test the MidiMix Led toggling
#

from mididings import *
from mididings.extra.inotify import *

from midimix import MidiMix, MidiMixLed

config(
    in_ports= [('MIDIMIX', '28:0'),],
    out_ports=[('MIDIMIX', '28:0'),],
)

hook(AutoRestart())

pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
post = Print('output', portnames='out')
control=Pass()

midimix=Filter(NOTEON) >> Process(MidiMix()) >> Process(MidiMixLed())

scenes = {
    1: Scene("Test", patch=midimix),
}

run(
    control=control,
    scenes=scenes,
    pre=pre,
    post=post,
)
