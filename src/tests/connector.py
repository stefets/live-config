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
        ('PART-A', '20:0'),
        ('PART-B', '20:1'),
        ('IN-1', '20:2'),
        ('IN-2', '20:3'),
        # ('Q49', '24:0'),
    ],
    out_ports=[
        ('PART-A', '20:0'),
        ('PART-B', '20:1'),
    ],


)
hook(
    AutoRestart()
)

fcb1010 = (
    ChannelFilter(9) >>
    CtrlFilter(20,22) >>
    CtrlSplit({
        20: Call(NavigateToScene),
        22: reset,
    })
)

keyboard = (
    ChannelFilter(8) >>
    (
        (CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
        (Filter(NOTEON) >> Transpose(-36))
    )
) >> Call(MPG123())

_control = (fcb1010 // keyboard)


piano = Output('PART-A', channel=1, program=((96 * 128), 100))
_scenes = {
    1: Scene("Piano", piano),
    2: Scene("Piano2", piano)
}

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

run(
    scenes=_scenes,
    pre=_pre,
    post=_post,
    control=_control,
)
