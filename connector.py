#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# SCRIPT TO SETUP THE IN/OUT PORTS ONLY
#

from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *

config(

    client_name = 'SD-90',
    backend = 'alsa',

    in_ports = [ ('IN', '20:2'), ], 	# MIDI INPUT
    out_ports = [ ('OUT', '20:0'), ], 	# MIDI OUTPUT

)

piano = Output('OUT', channel=1, program=((96*128),1))

run(piano)
