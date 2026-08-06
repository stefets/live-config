#!/usr/bin/env python
#-*- coding: utf-8 -*-


from mididings import engine
from mididings.extra import *
from mididings.extra.osc import *
from mididings.extra.inotify import *


config(
    backend = 'alsa',
    initial_scene = 1,
    client_name = 'mididings',

    in_ports = [
        ("vm_0",'.*VirMIDI.*-0$',),
        ],

    out_ports = [
        ("vm_0",'.*VirMIDI.*-0$',),
        ],
)

hook(
    OSCInterface(),
)

_scenes = {
    1: SceneGroup("Scene 1", 
        [
            Scene("SubScene 1", init_patch=Discard(), patch=Discard()),
            Scene("SubScene 2", init_patch=Discard(), patch=Discard())
        ]),
    2: SceneGroup("Scene 2", 
        [
            Scene("SubScene 1", init_patch=Discard(), patch=Discard()),
            Scene("SubScene 2", init_patch=Discard(), patch=Discard())
        ]),
}

run(
    scenes = _scenes,
    control = Pass(),
    pre  = Print('input  (pre )', portnames='in'),
    post = Print('output (post)', portnames='out'),
)
