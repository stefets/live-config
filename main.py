#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import subprocess
from threading import Timer
from time import sleep
from mididings import *
from mididings.extra import *
from mididings import engine
from mididings.engine import *
from mididings.event import *
from mididings.extra.osc import *
#now useless in dynamic mode :-/ :-(
#from mididings.extra.inotify import AutoRestart

config(

	# Default
    initial_scene = 2,
    #backend = 'alsa',
    #client_name = 'mididings',

    out_ports = [ 
        ('SD90_PARTA', '20:0'),				# Edirol SD-90 PART A 		(Port number 1)
        ('SD90_PARTB', '20:1'),				# Edirol SD-90 PART B 		(Port number 2)
        ('SD90_MIDI_OUT_1', '20:2',), 		# Edirol SD-90 MIDI OUT 1 	(Port number 3)
        ('SD90_MIDI_OUT_2', '20:3',), 		# Edirol SD-90 MIDI OUT 1 	(Port number 4)
		# Clones
        ('HD500', '20:2',), 				# MOVABLE
	],			

    in_ports = [ 
        ('Q49_MIDI_IN_1', '24:0',), 	# Alesis Q49 in USB MODE
        ('SD90_MIDI_IN_1','20:2',),		# Edirol SD-90 MIDI IN 1
        ('SD90_MIDI_IN_2','20:3',) 		# Edirol SD-90 MIDI IN 2
	],

)

hook(
    #MemorizeScene('scene.txt'),
    #AutoRestart(),
	#OSCInterface(port=56418),
	OSCInterface(),
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
# Control section
# control.py
__CONTROL__
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Sound module configuration 
#-----------------------------------------------------------------------------------------------------------
__SOUNDMODULE__

#-----------------------------------------------------------------------------------------------------------
# HD500 configuration
#-----------------------------------------------------------------------------------------------------------
__HD500__

#-----------------------------------------------------------------------------------------------------------
# Patches configuration
#-----------------------------------------------------------------------------------------------------------
__PATCHES__

#-----------------------------------------------------------------------------------------------------------
# Scenes configuration
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=InitSoundModule, patch=piano_base),
__SCENES__
}
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
# Run configuration
#-----------------------------------------------------------------------------------------------------------
_pre  = Print('input', portnames='in')
_post = Print('output',portnames='out')
run(
    control=fcb1010,
    scenes=_scenes, 
    pre=_pre, 
    #post=_post,
)

#-----------------------------------------------------------------------------------------------------------
# Many thanks to the programmer Dominic Sacre for that masterpiece
# http://das.nasophon.de/mididings/
# https://github.com/dsacre
# --------------------------------------------
# Stephane Gagnon
# pacificweb.ca
#-----------------------------------------------------------------------------------------------------------
