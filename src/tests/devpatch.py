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
     ],
)

#target = Output('OUT', channel=9, program=((96 * 128), 1))
#target = Output('OUT', channel=9, program=(53, 1))
big_country = (CtrlFilter(20) >> (
                                    Ctrl(51, 64) //
                                    Ctrl(52, 64) //
                                    Ctrl(54, 64)
                                  )
               ) 

_scenes = {
    1: Scene("BigCountry", big_country)
}

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

run(
    scenes=_scenes,
    pre=_pre,
    post=_post
)
