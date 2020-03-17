#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------
# Many thanks to the programmer Dominic Sacre for that masterpiece
# http://das.nasophon.de/mididings/
# https://github.com/dsacre
#-----------------------------------------------------------------------------------------------------------
# My personal mididings script
# Stephane Gagnon
#-----------------------------------------------------------------------------------------------------------

import os
import glob
import json
from subprocess import Popen, PIPE
from threading import Timer
from time import sleep
from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.osc import *

#useless for a dynamic script but usefull for a static scipt
#from mididings.extra.inotify import *

# Global configuration file
with open('config.json') as json_file:
    configuration = json.load(json_file)

config(

    # Defaults
    # initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    out_ports = [
        # DAW
        ('SD90_PARTA', '20:0'),         # Edirol SD-90 PART A       (Port number 1)
        ('SD90_PARTB', '20:1'),         # Edirol SD-90 PART B       (Port number 2)
        ('SD90_MIDI_OUT_1', '20:2',),   # Edirol SD-90 MIDI OUT 1   (Port number 3)
        ('SD90_MIDI_OUT_2', '20:3',),   # Edirol SD-90 MIDI OUT 2   (Port number 4)
        # Clones
        ('HD500', '20:2',),     # MOVABLE
        # HD500 midi out to gt10b midi , if I output to gt10b, it goes thru pod anyway
        ('GT10B', '20:2',),     # MOVABLE
 ],

    in_ports = [
        ('Q49_MIDI_IN_1', '20:0',),  # Alesis Q49 in USB MODE
        ('SD90_MIDI_IN_1','20:2',),  # Edirol SD-90 MIDI IN 1
        ('SD90_MIDI_IN_2','20:3',)   # Edirol SD-90 MIDI IN 2
 ],

)

hook(

    #MemorizeScene('memorize-scene.txt'),
    #AutoRestart(), #AutoRestart works with mididings.extra.inotify

    #OSCInterface(port=56418, notify_ports=[56419,56420]),
    OSCInterface(port=56418, notify_ports=56419),
    #OSCInterface(),
)

#-----------------------------------------------------------------------------------------------------------
# Functions section 
# functions.py
__FUNCTIONS__

#-----------------------------------------------------------------------------------------------------------
# Filters Section
# filters.py
#-----------------------------------------------------------------------------------------------------------
__FILTERS__

#-----------------------------------------------------------------------------------------------------------
# Hardware Section defined in /hardware/ directory
#-----------------------------------------------------------------------------------------------------------
# Edirol SD-90 Studio Canvas
__SD90__

# HD500 configuration
__HD500__

# GT10B configuration
__GT10B__

#-----------------------------------------------------------------------------------------------------------
# Control section
# control.py
__CONTROL__
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Patches configuration
# patches.py
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# Scenes region
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=InitSoundModule, patch=Discard()),
__SCENES__
}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
_pre  = Print('input', portnames='in')
_post = Print('output',portnames='out')

# TODO repenser ce token (fit pas avec le reste)
__CONTROLLER__

run(
    control=_ctrl,
    scenes=_scenes,
    #pre=_pre,
    #post=_post,
)
