#!/usr/bin/env python
#-*- coding: utf-8 -*-

import mididings

config(
    backend = 'alsa',
    initial_scene = 1,
    client_name = 'mididings',

    in_ports = [
        ("q49", '.*Q49 MIDI 1.*'),
    ],

    out_ports = [
        ("q49", '.*Q49 MIDI 1.*'),
    ],
)

run(
    scenes = {1:Pass()},
    control = Pass(),
    pre  = Print('input  (pre )', portnames='in'),
    post = Print('output (post)', portnames='out'),
)
