#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Thanks to the programmer Dominic Sacre for that masterpiece
http://das.nasophon.de/mididings/
https://github.com/dsacre
'''

import os
import sys
import json
from threading import Timer
from time import sleep

from mididings.extra import *
from mididings.extra.osc import *
from mididings import engine
from mididings.extra.inotify import *
from mididings.event import PitchbendEvent, MidiEvent, NoteOnEvent, NoteOffEvent
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene, output_event

from plugins.mp3player.galk import Mp3Player
from plugins.philips.wrappers import Hue

# Setup path
sys.path.append(os.path.realpath('.'))

# Config file
with open('config.json') as json_file:
    configuration = json.load(json_file)

config(

    # Defaults
    initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    # 
    #   Device name                     # Description               #
    #  

    out_ports = [

        ('SD90-PART-A', '20:0'),        # Edirol SD-90 PART A       Port(1)
        ('SD90-PART-B', '20:1'),        # Edirol SD-90 PART B       Port(2)
        ('SD90-MIDI-OUT-1', '20:2',),   # Edirol SD-90 MIDI OUT 1   Port(3)
        ('SD90-MIDI-OUT-2', '20:3',),   # Edirol SD-90 MIDI OUT 2   Port(4)

        ('GT10B-MIDI-OUT-1', '24:0',),  # Boss GT10B MIDI OUT 1     Port(5)

        ('UM2-MIDI-OUT-1', '28:0',),    # Edirol UM-2eX MIDI OUT 1  Port(6)
        ('UM2-MIDI-OUT-2', '28:1',),    # Edirol UM-2eX MIDI OUT 2  Port(7)

    ],

    in_ports = [

        ('SD90-MIDI-IN-1','20:2',),     # Edirol SD-90 MIDI IN 1
        ('SD90-MIDI-IN-2','20:3',),     # Edirol SD-90 MIDI IN 2

        ('GT10B-MIDI-IN-1', '24:0',),   # Boss GT10B MIDI IN 1

        ('UM2-MIDI-IN-1', '28:0',),     # Edirol UM-2eX MIDI IN-1
    ],

)

hook(
    #AutoRestart(),
    OSCInterface(),
)

#-----------------------------------------------------------------------------------------------------------
# Class and function body
# functions.py
__FUNCTIONS__

#-----------------------------------------------------------------------------------------------------------
# Filters body
# filters.py
#-----------------------------------------------------------------------------------------------------------
__FILTERS__

#-----------------------------------------------------------------------------------------------------------
# Devices body
__DEVICES__

#-----------------------------------------------------------------------------------------------------------
# Control body
# control.py
__CONTROL__
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Patches body
# patches.py
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# Scenes body
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=InitSoundModule, patch=Discard()),
__SCENES__
}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
# PROD
# Exclus les controllers
#pre  = ~ChannelFilter(8,9)
#post = Pass()

# DEBUG
pre  = Print('input', portnames='in')
post = Print('output',portnames='out')

run(
    control=_control,
    scenes=_scenes,
    pre=pre,
    post=post,
)
