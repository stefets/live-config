#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mididings.extra.osc import *
from mididings.extra.inotify import *

from httpclient import HttpGet

config(
     in_ports=[
         ('Q49', '28:0'),
     ],
     out_ports=[
        ('Q49', '28:0'),
     ],
)

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene(".hook.memorize_scene")
)

p_test=Filter(NOTEON) >> Transpose(-36) >> Call(HttpGet("http://127.0.0.1:5555/switch_scene/{}"))
_scenes = {
    1: Scene("Test", init_patch=Discard(), patch=p_test)
}

run(
    control=Pass(),
    scenes=_scenes,
    pre=Print('input', portnames='in'),
    post=Print('output',portnames='out')
)
