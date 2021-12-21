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

from plugins.audioplayer.mp3 import Mp3Player, Playlist
from plugins.lighting.philips import HueScene, HueBlackout

# Setup path
sys.path.append(os.path.realpath('.'))

# Config file
with open('config.json') as json_file:
    configuration = json.load(json_file)

# Plugins config
plugins=configuration['plugins']
hue_config=plugins['lightning']
key_config=plugins['audioplayer']
playlist_config=key_config["playlist"]
net_config=plugins['net']

config(

    # Defaults
    # initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    # 
    #   Device name                     # Description               #
    #  

    # Ports are tokenized and sed/awk by script_builder.sh

    out_ports = [

        ('SD90-PART-A', '__SD-90 Part A__'),
        ('SD90-PART-B', '__SD-90 Part B__'),
        ('SD90-MIDI-OUT-1', '__SD-90 MIDI 1__',),
        ('SD90-MIDI-OUT-2', '__SD-90 MIDI 2__',),

        ('GT10B-MIDI-OUT-1', '__GT-10B MIDI 1__',),

        ('UM2-MIDI-OUT-1', '__UM-2 MIDI 1__',),
        ('UM2-MIDI-OUT-2', '__UM-2 MIDI 2__',),

    ],

    in_ports = [

        ('SD90-MIDI-IN-1','__SD-90 MIDI 1__',),
        ('SD90-MIDI-IN-2','__SD-90 MIDI 2__',),

        ('GT10B-MIDI-IN-1', '__GT-10B MIDI 1__',),

        ('UM2-MIDI-IN-1', '__UM-2 MIDI 1__',),

        ('Q49', '__Q49 MIDI 1__',),

        ('CME', '__CME M-KEY MIDI 1__',),
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
# Patches body
# patches.py
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# Control body
# control.py
__CONTROL__
#-----------------------------------------------------------------------------------------------------------

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
pre  = ~ChannelFilter(8,9)
post = Pass()

# DEBUG
#pre  = Print('input', portnames='in')
#post = Print('output',portnames='out')

run(
    control=_control,
    scenes=_scenes,
    pre=pre,
    post=post,
)
