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

from plugins.mp3 import Mp3Player, Playlist
from plugins.philips import HueScene, HueBlackout
from plugins.spotify import SpotifyPlayer
from plugins.midimix import MidiMix, MidiMixLed

# Setup path
sys.path.append(os.path.realpath('.'))

# Environment
from dotenv import load_dotenv
load_dotenv()

# Configuration
with open('config.json') as json_file:
    configuration = json.load(json_file)

# Plugins config
plugins=configuration['plugins']
hue_config=plugins['lightning']
key_config=plugins['mp3player']
playlist_config=key_config["playlist"]
net_config=plugins['net']
spotify_config=plugins['spotify']

config(

# Defaults
# initial_scene = 1,
# backend = 'alsa',
# client_name = 'mididings',

# __Ports__ are changed by live.sh with sed/awk
out_ports = [

    ('MIDIMIX', '__MIDI Mix MIDI 1__',),  

    ('SD90-PART-A', '__SD-90 Part A__'),
    ('SD90-PART-B', '__SD-90 Part B__'),
    ('SD90-MIDI-OUT-1', '__SD-90 MIDI 1__',),
    ('SD90-MIDI-OUT-2', '__SD-90 MIDI 2__',),

    ('BEHRINGER', '__UMC204HD 192k MIDI 1__'),
   
    ('Q49-MIDI-IN', '__Q49 MIDI 1__',),

    ('GT10B-MIDI-OUT-1', '__GT-10B MIDI 1__',),
    
    ('MPK-MIDI-1', '__MPK249 MIDI 1__',), # USB A ch.1-16
    ('MPK-MIDI-2', '__MPK249 MIDI 2__',), # USB B ch.1-16
    ('MPK-MIDI-OUT-3', '__MPK249 MIDI 3__',), # 5 PIN MIDI OUT
    ('MPK-MIDI-4', '__MPK249 MIDI 4__',), # Remote 

],

in_ports = [

    ('MIDIMIX', '__MIDI Mix MIDI 1__',),

    ('SD90-PART-A', '__SD-90 Part A__'),
    ('SD90-PART-B', '__SD-90 Part B__'),
    ('SD90-MIDI-IN-1','__SD-90 MIDI 1__',),
    ('SD90-MIDI-IN-2','__SD-90 MIDI 2__',),

    ('BEHRINGER', '__UMC204HD 192k MIDI 1__'),

    ('Q49-MIDI-IN', '__Q49 MIDI 1__',),
    ('GT10B-MIDI-OUT-1', '__GT-10B MIDI 1__',),

    ('MPK-MIDI-IN-1', '__MPK249 MIDI 1__',), # USB A ch.1-16
    ('MPK-MIDI-IN-2', '__MPK249 MIDI 2__',), # USB B ch.1-16
    ('MPK-MIDI-IN-3', '__MPK249 MIDI 3__',), # 5 PIN MIDI IN 
    ('MPK-MIDI-IN-4', '__MPK249 MIDI 4__',), # Remote 

],

)

hook(
    #AutoRestart(), # Use when debug directly in script.py
    OSCInterface(),
    MemorizeScene("memorize_scene.txt")
)

#-----------------------------------------------------------------------------------------------------------
# Class and function body
__MODULES__

#-----------------------------------------------------------------------------------------------------------
# Patches body
# patches/*.py
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# Scenes body
# scenes/*.py
#-----------------------------------------------------------------------------------------------------------
_scenes = {
__SCENES__
}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
# PROD
pre  = ~ChannelFilter(8, 9, 11) // ~Filter(SYSRT_CLOCK)
post = Pass()

# DEBUG
#pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
#post = Print('output',portnames='out')

run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)
