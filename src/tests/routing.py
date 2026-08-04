#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mididings import engine
from mididings.extra import *
from mididings.extra.osc import *
from mididings.extra.inotify import *
from mididings.event import *
from mididings.engine import *

# Port name alias
sd90_midi_in_1  = "sd90_midi_in_1"
sd90_midi_in_2  = "sd90_midi_in_2"
sd90_midi_out_1 = "sd90_midi_out_1"
sd90_midi_out_2 = "sd90_midi_out_2"

um2_midi_in_1 = "um2_midi_in_1"
um2_midi_in_2 = "um2_midi_in_2"
um2_midi_out_1 = "um2_midi_out_1"
um2_midi_out_2 = "um2_midi_out_2"

config(

    initial_scene = 1,
    backend = 'alsa',
    client_name = 'mididings',

    out_ports = [
        (sd90_midi_out_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_out_2,  '.*SD-90 MIDI 2.*',),
        (um2_midi_out_1,'.*UM-2 MIDI 1.*',),
        (um2_midi_out_2,'.*UM-2 MIDI 2.*',),
    ],

    in_ports = [
        (sd90_midi_in_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_in_2,  '.*SD-90 MIDI 2.*',),
        (um2_midi_in_1,'.*UM-2 MIDI 1.*',),
    ],
)

hook(
    AutoRestart(),
)

pre  = Print('input', portnames='in') 
post = Print('output',portnames='out')

run(
    control=Pass(),
    scenes = {
        1 : Scene("Fix Loopback", init_patch = Discard(), patch = [
            # 1. Routage propre du UM-2 vers ses deux sorties physiques
            PortFilter(um2_midi_in_1) >> [Port(um2_midi_out_1), Port(um2_midi_out_2)],
            
            # 2. On bloque le port 2 pour qu'il ne renvoie rien par défaut (idx fallback)
            PortFilter(sd90_midi_in_2) >> Pass(),
            
            # 3. On bloque le port 1 s'il s'agit du canal 15 (le rebond du UM-2)
            PortFilter(sd90_midi_in_1) >> [
                ChannelFilter(15) >> Discard(),
                ~ChannelFilter(15) >> Pass() # Prêt pour tes vrais instruments plus tard !
        ]   
]


        ),
    },
    pre=pre,
    post=post,
)
                               