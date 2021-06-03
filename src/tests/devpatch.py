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

config(
     in_ports=[
         ('PART-A', '20:0'),
         ('PART-B', '20:1'),
         ('IN-1', '20:2'),
         ('IN-2', '20:3'),
         # ('Q49', '24:0'),
     ],
     out_ports=[
         ('PART-A', '20:0'),
         ('PART-B', '20:1'),
         ('THRU-1', '20:2'),
         ('OUT-2', '20:3'),
     ],
)

hook(
    AutoRestart(),
)

#target = Output('OUT', channel=9, program=((96 * 128), 1))
#target = Output('OUT', channel=9, program=(53, 1))

piano=~ChannelFilter(9) >> Output('PART-A', channel=3, program=((96*128),1), volume=100)

# Big Country
init = Program(3, channel=9, program=53) // Ctrl(3,9,1,40) // Ctrl(3,9,2,100) // Ctrl(3,9,53,100) // Ctrl(3,9,54,100)

big_country = (Filter(NOTEON) >>
        (
            (KeyFilter(notes=[72]) >> (Ctrl(3,9,51, 64) // Ctrl(3,9,52, 64) // Ctrl(3,9,2,127))) //
            (KeyFilter(notes=[71]) >> (Ctrl(3,9,51, 64) // Ctrl(3,9,52, 64) // Ctrl(3,9,2,100)))
        ) >> Port('THRU-1'))


_scenes = {
    1: Scene("BigCountry", init_patch=init, patch=big_country)
}

#_pre = ~ChannelFilter(9)
_pre  = Print('input', portnames='in')
_post = Print('output',portnames='out')


run(
    scenes=_scenes,
    pre=_pre,
    post=_post
)
