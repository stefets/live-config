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
from plugins.audioplayer.spotify import SpotifyPlayer

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
spotify_config=plugins['spotify']

config(

    # Defaults
    # initial_scene = 1,
    # backend = 'alsa',
    # client_name = 'mididings',

    # Ports are changed by live.sh with sed/awk
    out_ports = [

        ('SD90-PART-A', ''),
        ('SD90-PART-B', ''),
        ('SD90-MIDI-OUT-1', '',),
        ('SD90-MIDI-OUT-2', '',),

        ('GT10B-MIDI-OUT-1', '',),

        ('UM2-MIDI-OUT-1', '32:0',),
        ('UM2-MIDI-OUT-2', '32:1',),

        ('MPK-MIDI-OUT-3', '28:2',), # 5 PIN MIDI OUT

    ],

    in_ports = [

        ('SD90-MIDI-IN-1','',),
        ('SD90-MIDI-IN-2','',),

        #('GT10B-MIDI-IN-1', '',),

        ('UM2-MIDI-IN-1', '32:0',),

        #('Q49', '',),

        ('MPK-MIDI-IN-1', '28:0',), # USB A ch.1-16
        ('MPK-MIDI-IN-2', '28:1',), # USB B ch.1-16
        ('MPK-MIDI-IN-3', '28:2',), # 5 PIN MIDI IN 
        ('MPK-MIDI-IN-4', '28:3',), # Under investigation, possible internal thru

    ],

)

hook(
    #AutoRestart(), # Use when debug directly in script.py
    OSCInterface(),
)

#-----------------------------------------------------------------------------------------------------------
# Class and function body
# functions.py
# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
'''
Execute un glissando
'''
#def glissando(ev, from_note, to_note, vel, duration, direction, port):
#    note_range = range(from_note,to_note) if direction == 1 else reversed(range(from_note,to_note))
#    for note in note_range:
#        output_event(NoteOnEvent(port, ev.channel, note, vel))
#        sleep(duration)
#        output_event(NoteOffEvent(port, ev.channel, note))

def glissando_process(ev, from_note, to_note, vel, duration, direction, port, on):
    output_event(NoteOnEvent(port, ev.channel, from_note, vel)) if on else output_event(NoteOffEvent(port, ev.channel, from_note))
    if not on:
        from_note += 1
    if from_note < to_note:
        Timer(duration, lambda: glissando_process(ev, from_note, to_note, vel, duration, direction, port, not on)).start()

def glissando(ev, from_note, to_note, vel, duration, direction, port):
    glissando_process(ev, from_note, to_note, vel, duration, direction, port, True)

# -------------------------------------------------------------------------------------------

def NavigateToScene(ev):
    ''' 
    Navigate through Scenes and Sub-Scenes
    
    MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    
    With that function, you can wrap trough Scenes AND SubScenes
    
    That function assume that the first SceneNumber is 1
    '''
    if ev.ctrl == 20:
        nb_scenes = len(scenes())
        cs = current_scene()
        # Scene backward
        if ev.value == 1:
            if cs > 1:
                switch_scene(cs - 1)
            # Scene forward and wrap
        elif ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs + 1)
            else:
                switch_scene(1)
            # SubScene backward
        elif ev.value == 3:
            css = current_subscene()
            if css > 1:
                switch_subscene(css - 1)
            # SubScene forward and wrap
        elif ev.value == 4:
            css = current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css + 1)
            else:
                switch_subscene(1)


# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64) * direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value * direction)

# ---------------------------------------------------------------------------------------------------------

'''
    Convert data2 value to 0-1 range for the Soundcraft UI Mixer
'''
def data2_to_zero_one_range(ev):    
    return ev.data2 * 0.7874015748 / 100

def data2_to_mute(ev):
    return 1 if ev.data2==127 else 0

''' Set or overwrite an environment variable '''
def setenv(ev, key, value):
    os.environ[key] = value

''' Soundcraft input '''
def sc_input(ev, offset=-1):
    return ev.ctrl+offset if ev.type == CTRL else -1

def set_input(ev, offset):
    ev.ctrl = ev.ctrl + offset
    return ev

def debug(ev):
    print(ev)


#-----------------------------------------------------------------------------------------------------------
# Filters body
# filters.py
#-----------------------------------------------------------------------------------------------------------
# Channel et filtre des inputs

# Instruments d'exécution et/ou controlleur
inputs=configuration["inputs"]
akai_channel=inputs["akai"]
akai = ChannelFilter(akai_channel)

pk5_channel=inputs["pk5"]
pk5 = ChannelFilter(pk5_channel)

q49_channel=inputs["q49"]
q49 = ChannelFilter(q49_channel)

fcb_channel=inputs["fcb"]
fcb = ChannelFilter(fcb_channel)


#-----------------------------------------------------------------------------------------------------------
# Devices body
#
# DEVICE
# Boss GT-10B
# This device has 4 banks, each bank contains 100 programs 
# TODO : Create a device builder

# Midi channel defined in config.json
GT10BChannel = configuration['devices']['gt10b']

# Output port to use, specified in main.py
#GT10BPort = 'SD90-MIDI-OUT-1'  # 5 pin midi in, from SD-90 midi out 1
#GT10BPort = 'UM2-MIDI-OUT-1'  # 5 pin midi in, from  UM2 midi out 1
GT10BPort = 'GT10B-MIDI-OUT-1'  # USB MODE

# Banks
GT10B_bank_0 = (Ctrl(GT10BPort, GT10BChannel, 0, 0) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_1 = (Ctrl(GT10BPort, GT10BChannel, 0, 1) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_2 = (Ctrl(GT10BPort, GT10BChannel, 0, 2) // Ctrl(GT10BPort, GT10BChannel, 32, 0))
GT10B_bank_3 = (Ctrl(GT10BPort, GT10BChannel, 0, 3) // Ctrl(GT10BPort, GT10BChannel, 32, 0))

# Program (same for the 4 banks)
GT10B_pgrm_1 = Program(GT10BPort, channel=GT10BChannel, program=1)
GT10B_pgrm_2 = Program(GT10BPort, channel=GT10BChannel, program=2)
GT10B_pgrm_3 = Program(GT10BPort, channel=GT10BChannel, program=3)
GT10B_pgrm_4 = Program(GT10BPort, channel=GT10BChannel, program=4)
GT10B_pgrm_5 = Program(GT10BPort, channel=GT10BChannel, program=5)
GT10B_pgrm_6 = Program(GT10BPort, channel=GT10BChannel, program=6)
GT10B_pgrm_7 = Program(GT10BPort, channel=GT10BChannel, program=7)
GT10B_pgrm_8 = Program(GT10BPort, channel=GT10BChannel, program=8)
GT10B_pgrm_9 = Program(GT10BPort, channel=GT10BChannel, program=9)
GT10B_pgrm_10 = Program(GT10BPort, channel=GT10BChannel, program=10)
GT10B_pgrm_11 = Program(GT10BPort, channel=GT10BChannel, program=11)
GT10B_pgrm_12 = Program(GT10BPort, channel=GT10BChannel, program=12)
GT10B_pgrm_13 = Program(GT10BPort, channel=GT10BChannel, program=13)
GT10B_pgrm_14 = Program(GT10BPort, channel=GT10BChannel, program=14)
GT10B_pgrm_15 = Program(GT10BPort, channel=GT10BChannel, program=15)
GT10B_pgrm_16 = Program(GT10BPort, channel=GT10BChannel, program=16)
GT10B_pgrm_17 = Program(GT10BPort, channel=GT10BChannel, program=17)
GT10B_pgrm_18 = Program(GT10BPort, channel=GT10BChannel, program=18)
GT10B_pgrm_19 = Program(GT10BPort, channel=GT10BChannel, program=19)
GT10B_pgrm_20 = Program(GT10BPort, channel=GT10BChannel, program=20)
GT10B_pgrm_21 = Program(GT10BPort, channel=GT10BChannel, program=21)
GT10B_pgrm_22 = Program(GT10BPort, channel=GT10BChannel, program=22)
GT10B_pgrm_23 = Program(GT10BPort, channel=GT10BChannel, program=23)
GT10B_pgrm_24 = Program(GT10BPort, channel=GT10BChannel, program=24)
GT10B_pgrm_25 = Program(GT10BPort, channel=GT10BChannel, program=25)
GT10B_pgrm_26 = Program(GT10BPort, channel=GT10BChannel, program=26)
GT10B_pgrm_27 = Program(GT10BPort, channel=GT10BChannel, program=27)
GT10B_pgrm_28 = Program(GT10BPort, channel=GT10BChannel, program=28)
GT10B_pgrm_29 = Program(GT10BPort, channel=GT10BChannel, program=29)
GT10B_pgrm_30 = Program(GT10BPort, channel=GT10BChannel, program=30)
GT10B_pgrm_31 = Program(GT10BPort, channel=GT10BChannel, program=31)
GT10B_pgrm_32 = Program(GT10BPort, channel=GT10BChannel, program=32)
GT10B_pgrm_33 = Program(GT10BPort, channel=GT10BChannel, program=33)
GT10B_pgrm_34 = Program(GT10BPort, channel=GT10BChannel, program=34)
GT10B_pgrm_35 = Program(GT10BPort, channel=GT10BChannel, program=35)
GT10B_pgrm_36 = Program(GT10BPort, channel=GT10BChannel, program=36)
GT10B_pgrm_37 = Program(GT10BPort, channel=GT10BChannel, program=37)
GT10B_pgrm_38 = Program(GT10BPort, channel=GT10BChannel, program=38)
GT10B_pgrm_39 = Program(GT10BPort, channel=GT10BChannel, program=39)
GT10B_pgrm_40 = Program(GT10BPort, channel=GT10BChannel, program=40)
GT10B_pgrm_41 = Program(GT10BPort, channel=GT10BChannel, program=41)
GT10B_pgrm_42 = Program(GT10BPort, channel=GT10BChannel, program=42)
GT10B_pgrm_43 = Program(GT10BPort, channel=GT10BChannel, program=43)
GT10B_pgrm_44 = Program(GT10BPort, channel=GT10BChannel, program=44)
GT10B_pgrm_45 = Program(GT10BPort, channel=GT10BChannel, program=45)
GT10B_pgrm_46 = Program(GT10BPort, channel=GT10BChannel, program=46)
GT10B_pgrm_47 = Program(GT10BPort, channel=GT10BChannel, program=47)
GT10B_pgrm_48 = Program(GT10BPort, channel=GT10BChannel, program=48)
GT10B_pgrm_49 = Program(GT10BPort, channel=GT10BChannel, program=49)
GT10B_pgrm_50 = Program(GT10BPort, channel=GT10BChannel, program=50)
GT10B_pgrm_51 = Program(GT10BPort, channel=GT10BChannel, program=51)
GT10B_pgrm_52 = Program(GT10BPort, channel=GT10BChannel, program=52)
GT10B_pgrm_53 = Program(GT10BPort, channel=GT10BChannel, program=53)
GT10B_pgrm_54 = Program(GT10BPort, channel=GT10BChannel, program=54)
GT10B_pgrm_55 = Program(GT10BPort, channel=GT10BChannel, program=55)
GT10B_pgrm_56 = Program(GT10BPort, channel=GT10BChannel, program=56)
GT10B_pgrm_57 = Program(GT10BPort, channel=GT10BChannel, program=57)
GT10B_pgrm_58 = Program(GT10BPort, channel=GT10BChannel, program=58)
GT10B_pgrm_59 = Program(GT10BPort, channel=GT10BChannel, program=59)
GT10B_pgrm_60 = Program(GT10BPort, channel=GT10BChannel, program=60)
GT10B_pgrm_61 = Program(GT10BPort, channel=GT10BChannel, program=61)
GT10B_pgrm_62 = Program(GT10BPort, channel=GT10BChannel, program=62)
GT10B_pgrm_63 = Program(GT10BPort, channel=GT10BChannel, program=63)
GT10B_pgrm_64 = Program(GT10BPort, channel=GT10BChannel, program=64)
GT10B_pgrm_65 = Program(GT10BPort, channel=GT10BChannel, program=65)
GT10B_pgrm_66 = Program(GT10BPort, channel=GT10BChannel, program=66)
GT10B_pgrm_67 = Program(GT10BPort, channel=GT10BChannel, program=67)
GT10B_pgrm_68 = Program(GT10BPort, channel=GT10BChannel, program=68)
GT10B_pgrm_69 = Program(GT10BPort, channel=GT10BChannel, program=69)
GT10B_pgrm_70 = Program(GT10BPort, channel=GT10BChannel, program=70)
GT10B_pgrm_71 = Program(GT10BPort, channel=GT10BChannel, program=71)
GT10B_pgrm_72 = Program(GT10BPort, channel=GT10BChannel, program=72)
GT10B_pgrm_73 = Program(GT10BPort, channel=GT10BChannel, program=73)
GT10B_pgrm_74 = Program(GT10BPort, channel=GT10BChannel, program=74)
GT10B_pgrm_75 = Program(GT10BPort, channel=GT10BChannel, program=75)
GT10B_pgrm_76 = Program(GT10BPort, channel=GT10BChannel, program=76)
GT10B_pgrm_77 = Program(GT10BPort, channel=GT10BChannel, program=77)
GT10B_pgrm_78 = Program(GT10BPort, channel=GT10BChannel, program=78)
GT10B_pgrm_79 = Program(GT10BPort, channel=GT10BChannel, program=79)
GT10B_pgrm_80 = Program(GT10BPort, channel=GT10BChannel, program=80)
GT10B_pgrm_81 = Program(GT10BPort, channel=GT10BChannel, program=81)
GT10B_pgrm_82 = Program(GT10BPort, channel=GT10BChannel, program=82)
GT10B_pgrm_83 = Program(GT10BPort, channel=GT10BChannel, program=83)
GT10B_pgrm_84 = Program(GT10BPort, channel=GT10BChannel, program=84)
GT10B_pgrm_85 = Program(GT10BPort, channel=GT10BChannel, program=85)
GT10B_pgrm_86 = Program(GT10BPort, channel=GT10BChannel, program=86)
GT10B_pgrm_87 = Program(GT10BPort, channel=GT10BChannel, program=87)
GT10B_pgrm_88 = Program(GT10BPort, channel=GT10BChannel, program=88)
GT10B_pgrm_89 = Program(GT10BPort, channel=GT10BChannel, program=89)
GT10B_pgrm_90 = Program(GT10BPort, channel=GT10BChannel, program=90)
GT10B_pgrm_91 = Program(GT10BPort, channel=GT10BChannel, program=91)
GT10B_pgrm_92 = Program(GT10BPort, channel=GT10BChannel, program=92)
GT10B_pgrm_93 = Program(GT10BPort, channel=GT10BChannel, program=93)
GT10B_pgrm_94 = Program(GT10BPort, channel=GT10BChannel, program=94)
GT10B_pgrm_95 = Program(GT10BPort, channel=GT10BChannel, program=95)
GT10B_pgrm_96 = Program(GT10BPort, channel=GT10BChannel, program=96)
GT10B_pgrm_97 = Program(GT10BPort, channel=GT10BChannel, program=97)
GT10B_pgrm_98 = Program(GT10BPort, channel=GT10BChannel, program=98)
GT10B_pgrm_99 = Program(GT10BPort, channel=GT10BChannel, program=99)
GT10B_pgrm_100 = Program(GT10BPort, channel=GT10BChannel, program=100)

# GT10B_bank 0
#U01_A = [
#       Ctrl(GT10BPort, GT10BChannel,10, 127),
#       Ctrl(GT10BPort, GT10BChannel,10, 0),
#       Ctrl(GT10BPort, GT10BChannel,11, 127),
#       Ctrl(GT10BPort, GT10BChannel,11, 0),
#       Ctrl(GT10BPort, GT10BChannel,7, 127),
#       ]

#U01_A = (GT10B_bank_0 // GT10B_pgrm_1 // Ctrl(GT10BPort, GT10BChannel, 7,127))
U01_A = (GT10B_bank_0 // GT10B_pgrm_1)
U01_B = (GT10B_bank_0 // GT10B_pgrm_2)
U01_C = (GT10B_bank_0 // GT10B_pgrm_3)
U01_D = (GT10B_bank_0 // GT10B_pgrm_4)
U02_A = (GT10B_bank_0 // GT10B_pgrm_5)
U02_B = (GT10B_bank_0 // GT10B_pgrm_6)
U02_C = (GT10B_bank_0 // GT10B_pgrm_7)
U02_D = (GT10B_bank_0 // GT10B_pgrm_8)
U03_A = (GT10B_bank_0 // GT10B_pgrm_9)
U03_B = (GT10B_bank_0 // GT10B_pgrm_10)
U03_C = (GT10B_bank_0 // GT10B_pgrm_11)
U03_D = (GT10B_bank_0 // GT10B_pgrm_12)
U04_A = (GT10B_bank_0 // GT10B_pgrm_13)
U04_B = (GT10B_bank_0 // GT10B_pgrm_14)
U04_C = (GT10B_bank_0 // GT10B_pgrm_15)
U04_D = (GT10B_bank_0 // GT10B_pgrm_16)
U05_A = (GT10B_bank_0 // GT10B_pgrm_17)
U05_B = (GT10B_bank_0 // GT10B_pgrm_18)
U05_C = (GT10B_bank_0 // GT10B_pgrm_19)
U05_D = (GT10B_bank_0 // GT10B_pgrm_20)
U06_A = (GT10B_bank_0 // GT10B_pgrm_21)
U06_B = (GT10B_bank_0 // GT10B_pgrm_22)
U06_C = (GT10B_bank_0 // GT10B_pgrm_23)
U06_D = (GT10B_bank_0 // GT10B_pgrm_24)
U07_A = (GT10B_bank_0 // GT10B_pgrm_25)
U07_B = (GT10B_bank_0 // GT10B_pgrm_26)
U07_C = (GT10B_bank_0 // GT10B_pgrm_27)
U07_D = (GT10B_bank_0 // GT10B_pgrm_28)
U08_A = (GT10B_bank_0 // GT10B_pgrm_29)
U08_B = (GT10B_bank_0 // GT10B_pgrm_30)
U08_C = (GT10B_bank_0 // GT10B_pgrm_31)
U08_D = (GT10B_bank_0 // GT10B_pgrm_32)
U09_A = (GT10B_bank_0 // GT10B_pgrm_33)
U09_B = (GT10B_bank_0 // GT10B_pgrm_34)
U09_C = (GT10B_bank_0 // GT10B_pgrm_35)
U09_D = (GT10B_bank_0 // GT10B_pgrm_36)
U10_A = (GT10B_bank_0 // GT10B_pgrm_37)
U10_B = (GT10B_bank_0 // GT10B_pgrm_38)
U10_C = (GT10B_bank_0 // GT10B_pgrm_39)
U10_D = (GT10B_bank_0 // GT10B_pgrm_40)
U11_A = (GT10B_bank_0 // GT10B_pgrm_41)
U11_B = (GT10B_bank_0 // GT10B_pgrm_42)
U11_C = (GT10B_bank_0 // GT10B_pgrm_43)
U11_D = (GT10B_bank_0 // GT10B_pgrm_44)
U12_A = (GT10B_bank_0 // GT10B_pgrm_45)
U12_B = (GT10B_bank_0 // GT10B_pgrm_46)
U12_C = (GT10B_bank_0 // GT10B_pgrm_47)
U12_D = (GT10B_bank_0 // GT10B_pgrm_48)
U13_A = (GT10B_bank_0 // GT10B_pgrm_49)
U13_B = (GT10B_bank_0 // GT10B_pgrm_50)
U13_C = (GT10B_bank_0 // GT10B_pgrm_51)
U13_D = (GT10B_bank_0 // GT10B_pgrm_52)
U14_A = (GT10B_bank_0 // GT10B_pgrm_53)
U14_B = (GT10B_bank_0 // GT10B_pgrm_54)
U14_C = (GT10B_bank_0 // GT10B_pgrm_55)
U14_D = (GT10B_bank_0 // GT10B_pgrm_56)
U15_A = (GT10B_bank_0 // GT10B_pgrm_57)
U15_B = (GT10B_bank_0 // GT10B_pgrm_58)
U15_C = (GT10B_bank_0 // GT10B_pgrm_59)
U15_D = (GT10B_bank_0 // GT10B_pgrm_60)
U16_A = (GT10B_bank_0 // GT10B_pgrm_61)
U16_B = (GT10B_bank_0 // GT10B_pgrm_62)
U16_C = (GT10B_bank_0 // GT10B_pgrm_63)
U16_D = (GT10B_bank_0 // GT10B_pgrm_64)
U17_A = (GT10B_bank_0 // GT10B_pgrm_65)
U17_B = (GT10B_bank_0 // GT10B_pgrm_66)
U17_C = (GT10B_bank_0 // GT10B_pgrm_67)
U17_D = (GT10B_bank_0 // GT10B_pgrm_68)
U18_A = (GT10B_bank_0 // GT10B_pgrm_69)
U18_B = (GT10B_bank_0 // GT10B_pgrm_70)
U18_C = (GT10B_bank_0 // GT10B_pgrm_71)
U18_D = (GT10B_bank_0 // GT10B_pgrm_72)
U19_A = (GT10B_bank_0 // GT10B_pgrm_73)
U19_B = (GT10B_bank_0 // GT10B_pgrm_74)
U19_C = (GT10B_bank_0 // GT10B_pgrm_75)
U19_D = (GT10B_bank_0 // GT10B_pgrm_76)
U20_A = (GT10B_bank_0 // GT10B_pgrm_77)
U20_B = (GT10B_bank_0 // GT10B_pgrm_78)
U20_C = (GT10B_bank_0 // GT10B_pgrm_79)
U20_D = (GT10B_bank_0 // GT10B_pgrm_80)
U21_A = (GT10B_bank_0 // GT10B_pgrm_81)
U21_B = (GT10B_bank_0 // GT10B_pgrm_82)
U21_C = (GT10B_bank_0 // GT10B_pgrm_83)
U21_D = (GT10B_bank_0 // GT10B_pgrm_84)
U22_A = (GT10B_bank_0 // GT10B_pgrm_85)
U22_B = (GT10B_bank_0 // GT10B_pgrm_86)
U22_C = (GT10B_bank_0 // GT10B_pgrm_87)
U22_D = (GT10B_bank_0 // GT10B_pgrm_88)
U23_A = (GT10B_bank_0 // GT10B_pgrm_89)
U23_B = (GT10B_bank_0 // GT10B_pgrm_90)
U23_C = (GT10B_bank_0 // GT10B_pgrm_91)
U23_D = (GT10B_bank_0 // GT10B_pgrm_92)
U24_A = (GT10B_bank_0 // GT10B_pgrm_93)
U24_B = (GT10B_bank_0 // GT10B_pgrm_94)
U24_C = (GT10B_bank_0 // GT10B_pgrm_95)
U24_D = (GT10B_bank_0 // GT10B_pgrm_96)
U25_A = (GT10B_bank_0 // GT10B_pgrm_97)
U25_B = (GT10B_bank_0 // GT10B_pgrm_98)
U25_C = (GT10B_bank_0 // GT10B_pgrm_99)
U25_D = (GT10B_bank_0 // GT10B_pgrm_100)

# GT10B_bank 1
U26_A = (GT10B_bank_1 // GT10B_pgrm_1)
U26_B = (GT10B_bank_1 // GT10B_pgrm_2)
U26_C = (GT10B_bank_1 // GT10B_pgrm_3)
U26_D = (GT10B_bank_1 // GT10B_pgrm_4)
U27_A = (GT10B_bank_1 // GT10B_pgrm_5)
U27_B = (GT10B_bank_1 // GT10B_pgrm_6)
U27_C = (GT10B_bank_1 // GT10B_pgrm_7)
U27_D = (GT10B_bank_1 // GT10B_pgrm_8)
U28_A = (GT10B_bank_1 // GT10B_pgrm_9)
U28_B = (GT10B_bank_1 // GT10B_pgrm_10)
U28_C = (GT10B_bank_1 // GT10B_pgrm_11)
U28_D = (GT10B_bank_1 // GT10B_pgrm_12)
U29_A = (GT10B_bank_1 // GT10B_pgrm_13)
U29_B = (GT10B_bank_1 // GT10B_pgrm_14)
U29_C = (GT10B_bank_1 // GT10B_pgrm_15)
U29_D = (GT10B_bank_1 // GT10B_pgrm_16)
U30_A = (GT10B_bank_1 // GT10B_pgrm_17)
U30_B = (GT10B_bank_1 // GT10B_pgrm_18)
U30_C = (GT10B_bank_1 // GT10B_pgrm_19)
U30_D = (GT10B_bank_1 // GT10B_pgrm_20)
U31_A = (GT10B_bank_1 // GT10B_pgrm_21)
U31_B = (GT10B_bank_1 // GT10B_pgrm_22)
U31_C = (GT10B_bank_1 // GT10B_pgrm_23)
U31_D = (GT10B_bank_1 // GT10B_pgrm_24)
U32_A = (GT10B_bank_1 // GT10B_pgrm_25)
U32_B = (GT10B_bank_1 // GT10B_pgrm_26)
U32_C = (GT10B_bank_1 // GT10B_pgrm_27)
U32_D = (GT10B_bank_1 // GT10B_pgrm_28)
U33_A = (GT10B_bank_1 // GT10B_pgrm_29)
U33_B = (GT10B_bank_1 // GT10B_pgrm_30)
U33_C = (GT10B_bank_1 // GT10B_pgrm_31)
U33_D = (GT10B_bank_1 // GT10B_pgrm_32)
U34_A = (GT10B_bank_1 // GT10B_pgrm_33)
U34_B = (GT10B_bank_1 // GT10B_pgrm_34)
U34_C = (GT10B_bank_1 // GT10B_pgrm_35)
U34_D = (GT10B_bank_1 // GT10B_pgrm_36)
U35_A = (GT10B_bank_1 // GT10B_pgrm_37)
U35_B = (GT10B_bank_1 // GT10B_pgrm_38)
U35_C = (GT10B_bank_1 // GT10B_pgrm_39)
U35_D = (GT10B_bank_1 // GT10B_pgrm_40)
U36_A = (GT10B_bank_1 // GT10B_pgrm_41)
U36_B = (GT10B_bank_1 // GT10B_pgrm_42)
U36_C = (GT10B_bank_1 // GT10B_pgrm_43)
U36_D = (GT10B_bank_1 // GT10B_pgrm_44)
U37_A = (GT10B_bank_1 // GT10B_pgrm_45)
U37_B = (GT10B_bank_1 // GT10B_pgrm_46)
U37_C = (GT10B_bank_1 // GT10B_pgrm_47)
U37_D = (GT10B_bank_1 // GT10B_pgrm_48)
U38_A = (GT10B_bank_1 // GT10B_pgrm_49)
U38_B = (GT10B_bank_1 // GT10B_pgrm_50)
U38_C = (GT10B_bank_1 // GT10B_pgrm_51)
U38_D = (GT10B_bank_1 // GT10B_pgrm_52)
U39_A = (GT10B_bank_1 // GT10B_pgrm_53)
U39_B = (GT10B_bank_1 // GT10B_pgrm_54)
U39_C = (GT10B_bank_1 // GT10B_pgrm_55)
U39_D = (GT10B_bank_1 // GT10B_pgrm_56)
U40_A = (GT10B_bank_1 // GT10B_pgrm_57)
U40_B = (GT10B_bank_1 // GT10B_pgrm_58)
U40_C = (GT10B_bank_1 // GT10B_pgrm_59)
U40_D = (GT10B_bank_1 // GT10B_pgrm_60)
U41_A = (GT10B_bank_1 // GT10B_pgrm_61)
U41_B = (GT10B_bank_1 // GT10B_pgrm_62)
U41_C = (GT10B_bank_1 // GT10B_pgrm_63)
U41_D = (GT10B_bank_1 // GT10B_pgrm_64)
U42_A = (GT10B_bank_1 // GT10B_pgrm_65)
U42_B = (GT10B_bank_1 // GT10B_pgrm_66)
U42_C = (GT10B_bank_1 // GT10B_pgrm_67)
U42_D = (GT10B_bank_1 // GT10B_pgrm_68)
U43_A = (GT10B_bank_1 // GT10B_pgrm_69)
U43_B = (GT10B_bank_1 // GT10B_pgrm_70)
U43_C = (GT10B_bank_1 // GT10B_pgrm_71)
U43_D = (GT10B_bank_1 // GT10B_pgrm_72)
U44_A = (GT10B_bank_1 // GT10B_pgrm_73)
U44_B = (GT10B_bank_1 // GT10B_pgrm_74)
U44_C = (GT10B_bank_1 // GT10B_pgrm_75)
U44_D = (GT10B_bank_1 // GT10B_pgrm_76)
U45_A = (GT10B_bank_1 // GT10B_pgrm_77)
U45_B = (GT10B_bank_1 // GT10B_pgrm_78)
U45_C = (GT10B_bank_1 // GT10B_pgrm_79)
U45_D = (GT10B_bank_1 // GT10B_pgrm_80)
U46_A = (GT10B_bank_1 // GT10B_pgrm_81)
U46_B = (GT10B_bank_1 // GT10B_pgrm_82)
U46_C = (GT10B_bank_1 // GT10B_pgrm_83)
U46_D = (GT10B_bank_1 // GT10B_pgrm_84)
U47_A = (GT10B_bank_1 // GT10B_pgrm_85)
U47_B = (GT10B_bank_1 // GT10B_pgrm_86)
U47_C = (GT10B_bank_1 // GT10B_pgrm_87)
U47_D = (GT10B_bank_1 // GT10B_pgrm_88)
U48_A = (GT10B_bank_1 // GT10B_pgrm_89)
U48_B = (GT10B_bank_1 // GT10B_pgrm_90)
U48_C = (GT10B_bank_1 // GT10B_pgrm_91)
U48_D = (GT10B_bank_1 // GT10B_pgrm_92)
U49_A = (GT10B_bank_1 // GT10B_pgrm_93)
U49_B = (GT10B_bank_1 // GT10B_pgrm_94)
U49_C = (GT10B_bank_1 // GT10B_pgrm_95)
U49_D = (GT10B_bank_1 // GT10B_pgrm_96)
U50_A = (GT10B_bank_1 // GT10B_pgrm_97)
U50_B = (GT10B_bank_1 // GT10B_pgrm_98)
U50_C = (GT10B_bank_1 // GT10B_pgrm_99)
U50_D = (GT10B_bank_1 // GT10B_pgrm_100)

# GT10B_bank 2
P01_A = (GT10B_bank_2 // GT10B_pgrm_1)
P01_B = (GT10B_bank_2 // GT10B_pgrm_2)
P01_C = (GT10B_bank_2 // GT10B_pgrm_3)
P01_D = (GT10B_bank_2 // GT10B_pgrm_4)
P02_A = (GT10B_bank_2 // GT10B_pgrm_5)
P02_B = (GT10B_bank_2 // GT10B_pgrm_6)
P02_C = (GT10B_bank_2 // GT10B_pgrm_7)
P02_D = (GT10B_bank_2 // GT10B_pgrm_8)
P03_A = (GT10B_bank_2 // GT10B_pgrm_9)
P03_B = (GT10B_bank_2 // GT10B_pgrm_10)
P03_C = (GT10B_bank_2 // GT10B_pgrm_11)
P03_D = (GT10B_bank_2 // GT10B_pgrm_12)
P04_A = (GT10B_bank_2 // GT10B_pgrm_13)
P04_B = (GT10B_bank_2 // GT10B_pgrm_14)
P04_C = (GT10B_bank_2 // GT10B_pgrm_15)
P04_D = (GT10B_bank_2 // GT10B_pgrm_16)
P05_A = (GT10B_bank_2 // GT10B_pgrm_17)
P05_B = (GT10B_bank_2 // GT10B_pgrm_18)
P05_C = (GT10B_bank_2 // GT10B_pgrm_19)
P05_D = (GT10B_bank_2 // GT10B_pgrm_20)
P06_A = (GT10B_bank_2 // GT10B_pgrm_21)
P06_B = (GT10B_bank_2 // GT10B_pgrm_22)
P06_C = (GT10B_bank_2 // GT10B_pgrm_23)
P06_D = (GT10B_bank_2 // GT10B_pgrm_24)
P07_A = (GT10B_bank_2 // GT10B_pgrm_25)
P07_B = (GT10B_bank_2 // GT10B_pgrm_26)
P07_C = (GT10B_bank_2 // GT10B_pgrm_27)
P07_D = (GT10B_bank_2 // GT10B_pgrm_28)
P08_A = (GT10B_bank_2 // GT10B_pgrm_29)
P08_B = (GT10B_bank_2 // GT10B_pgrm_30)
P08_C = (GT10B_bank_2 // GT10B_pgrm_31)
P08_D = (GT10B_bank_2 // GT10B_pgrm_32)
P09_A = (GT10B_bank_2 // GT10B_pgrm_33)
P09_B = (GT10B_bank_2 // GT10B_pgrm_34)
P09_C = (GT10B_bank_2 // GT10B_pgrm_35)
P09_D = (GT10B_bank_2 // GT10B_pgrm_36)
P10_A = (GT10B_bank_2 // GT10B_pgrm_37)
P10_B = (GT10B_bank_2 // GT10B_pgrm_38)
P10_C = (GT10B_bank_2 // GT10B_pgrm_39)
P10_D = (GT10B_bank_2 // GT10B_pgrm_40)
P11_A = (GT10B_bank_2 // GT10B_pgrm_41)
P11_B = (GT10B_bank_2 // GT10B_pgrm_42)
P11_C = (GT10B_bank_2 // GT10B_pgrm_43)
P11_D = (GT10B_bank_2 // GT10B_pgrm_44)
P12_A = (GT10B_bank_2 // GT10B_pgrm_45)
P12_B = (GT10B_bank_2 // GT10B_pgrm_46)
P12_C = (GT10B_bank_2 // GT10B_pgrm_47)
P12_D = (GT10B_bank_2 // GT10B_pgrm_48)
P13_A = (GT10B_bank_2 // GT10B_pgrm_49)
P13_B = (GT10B_bank_2 // GT10B_pgrm_50)
P13_C = (GT10B_bank_2 // GT10B_pgrm_51)
P13_D = (GT10B_bank_2 // GT10B_pgrm_52)
P14_A = (GT10B_bank_2 // GT10B_pgrm_53)
P14_B = (GT10B_bank_2 // GT10B_pgrm_54)
P14_C = (GT10B_bank_2 // GT10B_pgrm_55)
P14_D = (GT10B_bank_2 // GT10B_pgrm_56)
P15_A = (GT10B_bank_2 // GT10B_pgrm_57)
P15_B = (GT10B_bank_2 // GT10B_pgrm_58)
P15_C = (GT10B_bank_2 // GT10B_pgrm_59)
P15_D = (GT10B_bank_2 // GT10B_pgrm_60)
P16_A = (GT10B_bank_2 // GT10B_pgrm_61)
P16_B = (GT10B_bank_2 // GT10B_pgrm_62)
P16_C = (GT10B_bank_2 // GT10B_pgrm_63)
P16_D = (GT10B_bank_2 // GT10B_pgrm_64)
P17_A = (GT10B_bank_2 // GT10B_pgrm_65)
P17_B = (GT10B_bank_2 // GT10B_pgrm_66)
P17_C = (GT10B_bank_2 // GT10B_pgrm_67)
P17_D = (GT10B_bank_2 // GT10B_pgrm_68)
P18_A = (GT10B_bank_2 // GT10B_pgrm_69)
P18_B = (GT10B_bank_2 // GT10B_pgrm_70)
P18_C = (GT10B_bank_2 // GT10B_pgrm_71)
P18_D = (GT10B_bank_2 // GT10B_pgrm_72)
P19_A = (GT10B_bank_2 // GT10B_pgrm_73)
P19_B = (GT10B_bank_2 // GT10B_pgrm_74)
P19_C = (GT10B_bank_2 // GT10B_pgrm_75)
P19_D = (GT10B_bank_2 // GT10B_pgrm_76)
P20_A = (GT10B_bank_2 // GT10B_pgrm_77)
P20_B = (GT10B_bank_2 // GT10B_pgrm_78)
P20_C = (GT10B_bank_2 // GT10B_pgrm_79)
P20_D = (GT10B_bank_2 // GT10B_pgrm_80)
P21_A = (GT10B_bank_2 // GT10B_pgrm_81)
P21_B = (GT10B_bank_2 // GT10B_pgrm_82)
P21_C = (GT10B_bank_2 // GT10B_pgrm_83)
P21_D = (GT10B_bank_2 // GT10B_pgrm_84)
P22_A = (GT10B_bank_2 // GT10B_pgrm_85)
P22_B = (GT10B_bank_2 // GT10B_pgrm_86)
P22_C = (GT10B_bank_2 // GT10B_pgrm_87)
P22_D = (GT10B_bank_2 // GT10B_pgrm_88)
P23_A = (GT10B_bank_2 // GT10B_pgrm_89)
P23_B = (GT10B_bank_2 // GT10B_pgrm_90)
P23_C = (GT10B_bank_2 // GT10B_pgrm_91)
P23_D = (GT10B_bank_2 // GT10B_pgrm_92)
P24_A = (GT10B_bank_2 // GT10B_pgrm_93)
P24_B = (GT10B_bank_2 // GT10B_pgrm_94)
P24_C = (GT10B_bank_2 // GT10B_pgrm_95)
P24_D = (GT10B_bank_2 // GT10B_pgrm_96)
P25_A = (GT10B_bank_2 // GT10B_pgrm_97)
P25_B = (GT10B_bank_2 // GT10B_pgrm_98)
P25_C = (GT10B_bank_2 // GT10B_pgrm_99)
P25_D = (GT10B_bank_2 // GT10B_pgrm_100)
# GT10B_bank 3
P26_A = (GT10B_bank_3 // GT10B_pgrm_1)
P26_B = (GT10B_bank_3 // GT10B_pgrm_2)
P26_C = (GT10B_bank_3 // GT10B_pgrm_3)
P26_D = (GT10B_bank_3 // GT10B_pgrm_4)
P27_A = (GT10B_bank_3 // GT10B_pgrm_5)
P27_B = (GT10B_bank_3 // GT10B_pgrm_6)
P27_C = (GT10B_bank_3 // GT10B_pgrm_7)
P27_D = (GT10B_bank_3 // GT10B_pgrm_8)
P28_A = (GT10B_bank_3 // GT10B_pgrm_9)
P28_B = (GT10B_bank_3 // GT10B_pgrm_10)
P28_C = (GT10B_bank_3 // GT10B_pgrm_11)
P28_D = (GT10B_bank_3 // GT10B_pgrm_12)
P29_A = (GT10B_bank_3 // GT10B_pgrm_13)
P29_B = (GT10B_bank_3 // GT10B_pgrm_14)
P29_C = (GT10B_bank_3 // GT10B_pgrm_15)
P29_D = (GT10B_bank_3 // GT10B_pgrm_16)
P30_A = (GT10B_bank_3 // GT10B_pgrm_17)
P30_B = (GT10B_bank_3 // GT10B_pgrm_18)
P30_C = (GT10B_bank_3 // GT10B_pgrm_19)
P30_D = (GT10B_bank_3 // GT10B_pgrm_20)
P31_A = (GT10B_bank_3 // GT10B_pgrm_21)
P31_B = (GT10B_bank_3 // GT10B_pgrm_22)
P31_C = (GT10B_bank_3 // GT10B_pgrm_23)
P31_D = (GT10B_bank_3 // GT10B_pgrm_24)
P32_A = (GT10B_bank_3 // GT10B_pgrm_25)
P32_B = (GT10B_bank_3 // GT10B_pgrm_26)
P32_C = (GT10B_bank_3 // GT10B_pgrm_27)
P32_D = (GT10B_bank_3 // GT10B_pgrm_28)
P33_A = (GT10B_bank_3 // GT10B_pgrm_29)
P33_B = (GT10B_bank_3 // GT10B_pgrm_30)
P33_C = (GT10B_bank_3 // GT10B_pgrm_31)
P33_D = (GT10B_bank_3 // GT10B_pgrm_32)
P34_A = (GT10B_bank_3 // GT10B_pgrm_33)
P34_B = (GT10B_bank_3 // GT10B_pgrm_34)
P34_C = (GT10B_bank_3 // GT10B_pgrm_35)
P34_D = (GT10B_bank_3 // GT10B_pgrm_36)
P35_A = (GT10B_bank_3 // GT10B_pgrm_37)
P35_B = (GT10B_bank_3 // GT10B_pgrm_38)
P35_C = (GT10B_bank_3 // GT10B_pgrm_39)
P35_D = (GT10B_bank_3 // GT10B_pgrm_40)
P36_A = (GT10B_bank_3 // GT10B_pgrm_41)
P36_B = (GT10B_bank_3 // GT10B_pgrm_42)
P36_C = (GT10B_bank_3 // GT10B_pgrm_43)
P36_D = (GT10B_bank_3 // GT10B_pgrm_44)
P37_A = (GT10B_bank_3 // GT10B_pgrm_45)
P37_B = (GT10B_bank_3 // GT10B_pgrm_46)
P37_C = (GT10B_bank_3 // GT10B_pgrm_47)
P37_D = (GT10B_bank_3 // GT10B_pgrm_48)
P38_A = (GT10B_bank_3 // GT10B_pgrm_49)
P38_B = (GT10B_bank_3 // GT10B_pgrm_50)
P38_C = (GT10B_bank_3 // GT10B_pgrm_51)
P38_D = (GT10B_bank_3 // GT10B_pgrm_52)
P39_A = (GT10B_bank_3 // GT10B_pgrm_53)
P39_B = (GT10B_bank_3 // GT10B_pgrm_54)
P39_C = (GT10B_bank_3 // GT10B_pgrm_55)
P39_D = (GT10B_bank_3 // GT10B_pgrm_56)
P40_A = (GT10B_bank_3 // GT10B_pgrm_57)
P40_B = (GT10B_bank_3 // GT10B_pgrm_58)
P40_C = (GT10B_bank_3 // GT10B_pgrm_59)
P40_D = (GT10B_bank_3 // GT10B_pgrm_60)
P41_A = (GT10B_bank_3 // GT10B_pgrm_61)
P41_B = (GT10B_bank_3 // GT10B_pgrm_62)
P41_C = (GT10B_bank_3 // GT10B_pgrm_63)
P41_D = (GT10B_bank_3 // GT10B_pgrm_64)
P42_A = (GT10B_bank_3 // GT10B_pgrm_65)
P42_B = (GT10B_bank_3 // GT10B_pgrm_66)
P42_C = (GT10B_bank_3 // GT10B_pgrm_67)
P42_D = (GT10B_bank_3 // GT10B_pgrm_68)
P43_A = (GT10B_bank_3 // GT10B_pgrm_69)
P43_B = (GT10B_bank_3 // GT10B_pgrm_70)
P43_C = (GT10B_bank_3 // GT10B_pgrm_71)
P43_D = (GT10B_bank_3 // GT10B_pgrm_72)
P44_A = (GT10B_bank_3 // GT10B_pgrm_73)
P44_B = (GT10B_bank_3 // GT10B_pgrm_74)
P44_C = (GT10B_bank_3 // GT10B_pgrm_75)
P44_D = (GT10B_bank_3 // GT10B_pgrm_76)
P45_A = (GT10B_bank_3 // GT10B_pgrm_77)
P45_B = (GT10B_bank_3 // GT10B_pgrm_78)
P45_C = (GT10B_bank_3 // GT10B_pgrm_79)
P45_D = (GT10B_bank_3 // GT10B_pgrm_80)
P46_A = (GT10B_bank_3 // GT10B_pgrm_81)
P46_B = (GT10B_bank_3 // GT10B_pgrm_82)
P46_C = (GT10B_bank_3 // GT10B_pgrm_83)
P46_D = (GT10B_bank_3 // GT10B_pgrm_84)
P47_A = (GT10B_bank_3 // GT10B_pgrm_85)
P47_B = (GT10B_bank_3 // GT10B_pgrm_86)
P47_C = (GT10B_bank_3 // GT10B_pgrm_87)
P47_D = (GT10B_bank_3 // GT10B_pgrm_88)
P48_A = (GT10B_bank_3 // GT10B_pgrm_89)
P48_B = (GT10B_bank_3 // GT10B_pgrm_90)
P48_C = (GT10B_bank_3 // GT10B_pgrm_91)
P48_D = (GT10B_bank_3 // GT10B_pgrm_92)
P49_A = (GT10B_bank_3 // GT10B_pgrm_93)
P49_B = (GT10B_bank_3 // GT10B_pgrm_94)
P49_C = (GT10B_bank_3 // GT10B_pgrm_95)
P49_D = (GT10B_bank_3 // GT10B_pgrm_96)
P50_A = (GT10B_bank_3 // GT10B_pgrm_97)
P50_B = (GT10B_bank_3 // GT10B_pgrm_98)
P50_C = (GT10B_bank_3 // GT10B_pgrm_99)
P50_D = (GT10B_bank_3 // GT10B_pgrm_100)

# Send CC
GT10B_Ctrl =  Ctrl(GT10BPort, GT10BChannel, EVENT_CTRL, EVENT_VALUE)

# Send CC aliases
GT10B_Tuner = GT10B_Ctrl    
GT10B_Volume = GT10B_Ctrl
GT10B_Expression = GT10B_Ctrl
#
# Line 6 POD-HD-500
#

# Channel d'écoute
hd500_channel = configuration['devices']['hd500']

# Connecté a quel port MIDI ?
hd500_port = 'UM2-MIDI-OUT-1'

# Programmes
P01A = Program(hd500_port, channel=hd500_channel, program=1)
P01B = Program(hd500_port, channel=hd500_channel, program=2)
P01C = Program(hd500_port, channel=hd500_channel, program=3)
P01D = Program(hd500_port, channel=hd500_channel, program=4)
P02A = Program(hd500_port, channel=hd500_channel, program=5)
P02B = Program(hd500_port, channel=hd500_channel, program=6)
P02C = Program(hd500_port, channel=hd500_channel, program=7)
P02D = Program(hd500_port, channel=hd500_channel, program=8)
P03A = Program(hd500_port, channel=hd500_channel, program=9)
P03B = Program(hd500_port, channel=hd500_channel, program=10)
P03C = Program(hd500_port, channel=hd500_channel, program=11)
P03D = Program(hd500_port, channel=hd500_channel, program=12)
P04A = Program(hd500_port, channel=hd500_channel, program=13)
P04B = Program(hd500_port, channel=hd500_channel, program=14)
P04C = Program(hd500_port, channel=hd500_channel, program=15)
P04D = Program(hd500_port, channel=hd500_channel, program=16)
P05A = Program(hd500_port, channel=hd500_channel, program=17)
P05B = Program(hd500_port, channel=hd500_channel, program=18)
P05C = Program(hd500_port, channel=hd500_channel, program=19)
P05D = Program(hd500_port, channel=hd500_channel, program=20)
P06A = Program(hd500_port, channel=hd500_channel, program=21)
P06B = Program(hd500_port, channel=hd500_channel, program=22)
P06C = Program(hd500_port, channel=hd500_channel, program=23)
P06D = Program(hd500_port, channel=hd500_channel, program=24)
P07A = Program(hd500_port, channel=hd500_channel, program=25)
P07B = Program(hd500_port, channel=hd500_channel, program=26)
P07C = Program(hd500_port, channel=hd500_channel, program=27)
P07D = Program(hd500_port, channel=hd500_channel, program=28)
P08A = Program(hd500_port, channel=hd500_channel, program=29)
P08B = Program(hd500_port, channel=hd500_channel, program=30)
P08C = Program(hd500_port, channel=hd500_channel, program=31)
P08D = Program(hd500_port, channel=hd500_channel, program=32)
P09A = Program(hd500_port, channel=hd500_channel, program=33)
P09B = Program(hd500_port, channel=hd500_channel, program=34)
P09C = Program(hd500_port, channel=hd500_channel, program=35)
P09D = Program(hd500_port, channel=hd500_channel, program=36)
P10A = Program(hd500_port, channel=hd500_channel, program=37)
P10B = Program(hd500_port, channel=hd500_channel, program=38)
P10C = Program(hd500_port, channel=hd500_channel, program=39)
P10D = Program(hd500_port, channel=hd500_channel, program=40)
P11A = Program(hd500_port, channel=hd500_channel, program=41)
P11B = Program(hd500_port, channel=hd500_channel, program=42)
P11C = Program(hd500_port, channel=hd500_channel, program=43)
P11D = Program(hd500_port, channel=hd500_channel, program=44)
P12A = Program(hd500_port, channel=hd500_channel, program=45)
P12B = Program(hd500_port, channel=hd500_channel, program=46)
P12C = Program(hd500_port, channel=hd500_channel, program=47)
P12D = Program(hd500_port, channel=hd500_channel, program=48)
P13A = Program(hd500_port, channel=hd500_channel, program=49)
P13B = Program(hd500_port, channel=hd500_channel, program=50)
P13C = Program(hd500_port, channel=hd500_channel, program=51)
P13D = Program(hd500_port, channel=hd500_channel, program=52)
P14A = Program(hd500_port, channel=hd500_channel, program=53)
P14B = Program(hd500_port, channel=hd500_channel, program=54)
P14C = Program(hd500_port, channel=hd500_channel, program=55)
P14D = Program(hd500_port, channel=hd500_channel, program=56)
P15A = Program(hd500_port, channel=hd500_channel, program=57)
P15B = Program(hd500_port, channel=hd500_channel, program=58)
P15C = Program(hd500_port, channel=hd500_channel, program=59)
P15D = Program(hd500_port, channel=hd500_channel, program=60)
P16A = Program(hd500_port, channel=hd500_channel, program=61)
P16B = Program(hd500_port, channel=hd500_channel, program=62)
P16C = Program(hd500_port, channel=hd500_channel, program=63)
P16D = Program(hd500_port, channel=hd500_channel, program=64)

# POD-HD-500 to control Fender Super60
# TODO Revisiter cela
#S60A = Program(hd500_port, channel=hd500_channel, program=61)
#S60B = Program(hd500_port, channel=hd500_channel, program=62)
#S60C = Program(hd500_port, channel=hd500_channel, program=63)
#S60D = Program(hd500_port, channel=hd500_channel, program=64)

# Footsiwtch
FS1 = Ctrl(hd500_port, hd500_channel, 51, 64)
FS2 = Ctrl(hd500_port, hd500_channel, 52, 64)
FS3 = Ctrl(hd500_port, hd500_channel, 53, 64)
FS4 = Ctrl(hd500_port, hd500_channel, 54, 64)
FS5 = Ctrl(hd500_port, hd500_channel, 55, 64)
FS6 = Ctrl(hd500_port, hd500_channel, 56, 64)
FS7 = Ctrl(hd500_port, hd500_channel, 57, 64)
FS8 = Ctrl(hd500_port, hd500_channel, 58, 64)
TOE = Ctrl(hd500_port, hd500_channel, 59, 64)

# Exp1 et Exp2
Expr1 = Ctrl(hd500_port, hd500_channel, 1, EVENT_VALUE)
Expr2 = Ctrl(hd500_port, hd500_channel, 2, EVENT_VALUE)

# Tuner
Tuner = Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)

TunerOn = Ctrl(hd500_port, hd500_channel, 69, 127)
TunerOff = Ctrl(hd500_port, hd500_channel, 69, 0)

#
# The MIDIDINGS syntax for the EDIROL SD-90 Studio Canvas sound module (not fully implemented)
#

factor = 128

'''
Inst part: 
80(50H) = Special 1 set
81(51H) = Special 2 set
96(60H) = Classical set
97(61H) = Contemporary set
98(62H) = Solo set
99(63H) = Enhanced set
'''
Special1=80*factor
Special2=81*factor
Classical=96*factor
Contemporary=97*factor
Solo=98*factor
Enhanced=99*factor

'''
Drum part: 
104(60H) = Classical set
105(61H) = Contemporary set
106(62H) = Solo set
107(63H) = Enhanced set
'''
ClassicalDrum=104*factor
ContemporaryDrum=105*factor
SoloDrum=106*factor
EnhancedDrum=107*factor

'''
Variation
'''
Var1=1
Var2=2
Var3=3
Var4=4
Var5=5
Var6=6
Var7=7
Var8=8
Var9=9

# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01 = (Ctrl('SD90-PART-A', 1, 100, 0) // Ctrl('SD90-PART-A', 1, 101, 0) // Ctrl('SD90-PART-A', 1, 6, 12) // Ctrl('SD90-PART-A', 1, 38, 0))
PB_A02 = (Ctrl('SD90-PART-A', 2, 100, 0) // Ctrl('SD90-PART-A', 2, 101, 0) // Ctrl('SD90-PART-A', 2, 6, 12) // Ctrl('SD90-PART-A', 2, 38, 0))
PB_A03 = (Ctrl('SD90-PART-A', 3, 100, 0) // Ctrl('SD90-PART-A', 3, 101, 0) // Ctrl('SD90-PART-A', 3, 6, 12) // Ctrl('SD90-PART-A', 3, 38, 0))
PB_A04 = (Ctrl('SD90-PART-A', 4, 100, 0) // Ctrl('SD90-PART-A', 4, 101, 0) // Ctrl('SD90-PART-A', 4, 6, 12) // Ctrl('SD90-PART-A', 4, 38, 0))
PB_A05 = (Ctrl('SD90-PART-A', 5, 100, 0) // Ctrl('SD90-PART-A', 5, 101, 0) // Ctrl('SD90-PART-A', 5, 6, 12) // Ctrl('SD90-PART-A', 5, 38, 0))
PB_A06 = (Ctrl('SD90-PART-A', 6, 100, 0) // Ctrl('SD90-PART-A', 6, 101, 0) // Ctrl('SD90-PART-A', 6, 6, 12) // Ctrl('SD90-PART-A', 6, 38, 0))
PB_A07 = (Ctrl('SD90-PART-A', 7, 100, 0) // Ctrl('SD90-PART-A', 7, 101, 0) // Ctrl('SD90-PART-A', 7, 6, 12) // Ctrl('SD90-PART-A', 7, 38, 0))
PB_A08 = (Ctrl('SD90-PART-A', 8, 100, 0) // Ctrl('SD90-PART-A', 8, 101, 0) // Ctrl('SD90-PART-A', 8, 6, 12) // Ctrl('SD90-PART-A', 8, 38, 0))
PB_A09 = (Ctrl('SD90-PART-A', 9, 100, 0) // Ctrl('SD90-PART-A', 9, 101, 0) // Ctrl('SD90-PART-A', 9, 6, 12) // Ctrl('SD90-PART-A', 9, 38, 0))
PB_A10 = (Ctrl('SD90-PART-A', 10, 100, 0) // Ctrl('SD90-PART-A', 10, 101, 0) // Ctrl('SD90-PART-A', 10, 6, 12) // Ctrl('SD90-PART-A', 10, 38, 0))
PB_A11 = (Ctrl('SD90-PART-A', 11, 100, 0) // Ctrl('SD90-PART-A', 11, 101, 0) // Ctrl('SD90-PART-A', 11, 6, 12) // Ctrl('SD90-PART-A', 11, 38, 0))
PB_A12 = (Ctrl('SD90-PART-A', 12, 100, 0) // Ctrl('SD90-PART-A', 12, 101, 0) // Ctrl('SD90-PART-A', 12, 6, 12) // Ctrl('SD90-PART-A', 12, 38, 0))
PB_A13 = (Ctrl('SD90-PART-A', 13, 100, 0) // Ctrl('SD90-PART-A', 13, 101, 0) // Ctrl('SD90-PART-A', 13, 6, 12) // Ctrl('SD90-PART-A', 13, 38, 0))
PB_A14 = (Ctrl('SD90-PART-A', 14, 100, 0) // Ctrl('SD90-PART-A', 14, 101, 0) // Ctrl('SD90-PART-A', 14, 6, 12) // Ctrl('SD90-PART-A', 14, 38, 0))
PB_A15 = (Ctrl('SD90-PART-A', 15, 100, 0) // Ctrl('SD90-PART-A', 15, 101, 0) // Ctrl('SD90-PART-A', 15, 6, 12) // Ctrl('SD90-PART-A', 15, 38, 0))
PB_A16 = (Ctrl('SD90-PART-A', 16, 100, 0) // Ctrl('SD90-PART-A', 16, 101, 0) // Ctrl('SD90-PART-A', 16, 6, 12) // Ctrl('SD90-PART-A', 16, 38, 0))

# SD-90 Part B - All Channel
PB_B01 = (Ctrl('SD90-PART-B', 1, 100, 0) // Ctrl('SD90-PART-B', 1, 101, 0) // Ctrl('SD90-PART-B', 1, 6, 12) // Ctrl('SD90-PART-B', 1, 38, 0))
PB_B02 = (Ctrl('SD90-PART-B', 2, 100, 0) // Ctrl('SD90-PART-B', 2, 101, 0) // Ctrl('SD90-PART-B', 2, 6, 12) // Ctrl('SD90-PART-B', 2, 38, 0))
PB_B03 = (Ctrl('SD90-PART-B', 3, 100, 0) // Ctrl('SD90-PART-B', 3, 101, 0) // Ctrl('SD90-PART-B', 3, 6, 12) // Ctrl('SD90-PART-B', 3, 38, 0))
PB_B04 = (Ctrl('SD90-PART-B', 4, 100, 0) // Ctrl('SD90-PART-B', 4, 101, 0) // Ctrl('SD90-PART-B', 4, 6, 12) // Ctrl('SD90-PART-B', 4, 38, 0))
PB_B05 = (Ctrl('SD90-PART-B', 5, 100, 0) // Ctrl('SD90-PART-B', 5, 101, 0) // Ctrl('SD90-PART-B', 5, 6, 12) // Ctrl('SD90-PART-B', 5, 38, 0))
PB_B06 = (Ctrl('SD90-PART-B', 6, 100, 0) // Ctrl('SD90-PART-B', 6, 101, 0) // Ctrl('SD90-PART-B', 6, 6, 12) // Ctrl('SD90-PART-B', 6, 38, 0))
PB_B07 = (Ctrl('SD90-PART-B', 7, 100, 0) // Ctrl('SD90-PART-B', 7, 101, 0) // Ctrl('SD90-PART-B', 7, 6, 12) // Ctrl('SD90-PART-B', 7, 38, 0))
PB_B08 = (Ctrl('SD90-PART-B', 8, 100, 0) // Ctrl('SD90-PART-B', 8, 101, 0) // Ctrl('SD90-PART-B', 8, 6, 12) // Ctrl('SD90-PART-B', 8, 38, 0))
PB_B09 = (Ctrl('SD90-PART-B', 9, 100, 0) // Ctrl('SD90-PART-B', 9, 101, 0) // Ctrl('SD90-PART-B', 9, 6, 12) // Ctrl('SD90-PART-B', 9, 38, 0))
PB_B10 = (Ctrl('SD90-PART-B', 10, 100, 0) // Ctrl('SD90-PART-B', 10, 101, 0) // Ctrl('SD90-PART-B', 10, 6, 12) // Ctrl('SD90-PART-B', 10, 38, 0))
PB_B11 = (Ctrl('SD90-PART-B', 11, 100, 0) // Ctrl('SD90-PART-B', 11, 101, 0) // Ctrl('SD90-PART-B', 11, 6, 12) // Ctrl('SD90-PART-B', 11, 38, 0))
PB_B12 = (Ctrl('SD90-PART-B', 12, 100, 0) // Ctrl('SD90-PART-B', 12, 101, 0) // Ctrl('SD90-PART-B', 12, 6, 12) // Ctrl('SD90-PART-B', 12, 38, 0))
PB_B13 = (Ctrl('SD90-PART-B', 13, 100, 0) // Ctrl('SD90-PART-B', 13, 101, 0) // Ctrl('SD90-PART-B', 13, 6, 12) // Ctrl('SD90-PART-B', 13, 38, 0))
PB_B14 = (Ctrl('SD90-PART-B', 14, 100, 0) // Ctrl('SD90-PART-B', 14, 101, 0) // Ctrl('SD90-PART-B', 14, 6, 12) // Ctrl('SD90-PART-B', 14, 38, 0))
PB_B15 = (Ctrl('SD90-PART-B', 15, 100, 0) // Ctrl('SD90-PART-B', 15, 101, 0) // Ctrl('SD90-PART-B', 15, 6, 12) // Ctrl('SD90-PART-B', 15, 38, 0))
PB_B16 = (Ctrl('SD90-PART-B', 16, 100, 0) // Ctrl('SD90-PART-B', 16, 101, 0) // Ctrl('SD90-PART-B', 16, 6, 12) // Ctrl('SD90-PART-B', 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------

# Classical Set
StandardSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 1))
RoomSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 9))
PowerSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 17))
ElectricSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 25))
AnalogSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 26))
JazzSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 33))
BrushSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 41))
OrchestraSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 49))
SFXSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 57))

# Contemporary Set
StandardSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 1))
RoomSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 9))
PowerSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 17))
DanceSet =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 25))
RaveSet =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 26))
JazzSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 33))
BrushSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 41))

# Solo Set
St_Standard =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 1))
St_Room =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 9))
St_Power =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 17))
RustSet =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 25))
Analog2Set =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 26))
St_Jazz =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 33))
St_Brush =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 41))

# Enhanced Set
Amb_Standard =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 1))
Amb_Room =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 9))
GatedPower =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 17))
TechnoSet =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 25))
BullySet =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 26))
Amb_Jazz =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 33))
Amb_Brush =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 41))

# WIP SD-90 Full Patch implementation 
# Special 1 instrument part
DLAPad=Output('SD90-PART-A', channel=1, program=(Special1, 1))
BrushingSaw=Output('SD90-PART-A', channel=1, program=(Special1, 2))
Xtremities=Output('SD90-PART-A', channel=1, program=(Special1, 3))
Atmostrings=Output('SD90-PART-A', channel=1, program=(Special1, 4))
NooTongs=Output('SD90-PART-A', channel=1, program=(Special1, 5))
Mistery=Output('SD90-PART-A', channel=1, program=(Special1, 6))
EastrnEurope=Output('SD90-PART-A', channel=1, program=(Special1, 7))
HarpsiAndStr=Output('SD90-PART-A', channel=1, program=(Special1, 8))
ShoutGt=Output('SD90-PART-A', channel=1, program=(Special1,9))
CleanChorus=Output('SD90-PART-A', channel=1, program=(Special1, 10))
MidBoostGt=Output('SD90-PART-A', channel=1, program=(Special1, 11))
Guitarvibe=Output('SD90-PART-A', channel=1, program=(Special1, 12))
ClusterSect=Output('SD90-PART-A', channel=1, program=(Special1, 13))
MariachiTp=Output('SD90-PART-A', channel=1, program=(Special1, 14))
NYTenor=Output('SD90-PART-A', channel=1, program=(Special1, 15))
JazzClub=Output('SD90-PART-A', channel=1, program=(Special1, 16))
MoodyAlto=Output('SD90-PART-A', channel=1, program=(Special1, 17))
FujiYama=Output('SD90-PART-A', channel=1, program=(Special1, 18))
SDPiano=Output('SD90-PART-A', channel=1, program=(Special1, 19))

# Special 2 instrument part
RichChoir=Output('SD90-PART-A', channel=1, program=(Special2, 18))
OBBorealis=Output('SD90-PART-A', channel=1, program=(Special2, 80))
VintagePhase=Output('SD90-PART-A', channel=1, program=(Special2, 82))
FifthAtmAft=Output('SD90-PART-A', channel=1, program=(Special2, 85))
Borealis=Output('SD90-PART-A', channel=1, program=(Special2, 106))
CircularPad=Output('SD90-PART-A', channel=1, program=(Special2, 107))
Oxigenizer=Output('SD90-PART-A', channel=1, program=(Special2, 108))
Quasar=Output('SD90-PART-A', channel=1, program=(Special2, 109))
HellSection=Output('SD90-PART-A', channel=1, program=(Special2, 111))


# Classical instrument part
BirdTweet=Output('SD90-PART-B', channel=4, program=(Classical, 124))
Applause=Output('SD90-PART-B', channel=8, program=(Classical, 127))

# Classical instrument part - Variation 1
Itopia=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 92))
Kalimba=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 109))
BagPipe=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 110))
Dog=Output('SD90-PART-B', channel=14, program=(Classical+Var1, 124))
Telephone2=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 125))
CarEngine=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 126))
Laughing=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 127))

# Classical instrument part - Variation 2
Screaming=Output('SD90-PART-B', channel=13, program=(Classical+Var2, 127))
DoorCreak=Output('SD90-PART-B', channel=1, program=(Classical+Var2, 125))
Thunder=Output('SD90-PART-B', channel=15, program=(Classical+Var2, 123))

# Classical instrument part - Variation 3
Wind=Output('SD90-PART-B', channel=3, program=(Classical+Var3, 123))
Explosion=Output('SD90-PART-B', channel=7, program=(Classical+Var3, 128))

# Classical instrument part - Variation 4
Stream=Output('SD90-PART-B', channel=12, program=(Classical+Var4, 123))


# Classical instrument part - Variation 5
Siren=Output('SD90-PART-B', channel=5, program=(Classical+Var5, 126))
Bubble=Output('SD90-PART-B', channel=1, program=(Classical+Var5, 123))

# Classical instrument part - Variation 6
Train=Output('SD90-PART-B', channel=6, program=(Classical+Var6, 126))

# Classical instrument part - Variation 7
Jetplane=Output('SD90-PART-B', channel=1, program=(Classical+Var7, 126))

# Classical instrument part - Variation 8
Starship=Output('SD90-PART-B', channel=1, program=(Classical+Var8, 126))

# Contemporary instrument part
Helicpoter=Output('SD90-PART-B', channel=1, program=(Contemporary, 126))
Seashore=Output('SD90-PART-B', channel=2, program=(Contemporary, 123))

# Contemporary instrument part - Variation 1
Rain=Output('SD90-PART-B', channel=1, program=(Contemporary+Var1, 123))


### End SD-90 Patch list
# -------------------------------------------------------------------
# SD Mixer config 
Reset = '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7'
MixToAfx = '\xF0\x41\x10\x00\x48\x12\x02\x10\x10\x00\x06\x58\xF7'
MasterEffect = '\xF0\x41\x10\x00\x48\x12\x02\x10\x20\x00\x78\x56\xF7'

SD90_Initialize = (SysEx(Reset) // SysEx(MixToAfx) // SysEx(MasterEffect) // InitPitchBend)
#-----------------------------------------------------------------------------------------------------------
# Patches body
# patches.py
#-----------------------------------------------------------------------------------------------------------
'''
Notes :
- Ctrl #3 est Undefined selon la documentation du protocole MIDI; donc libre d'utilisation.
- L'utilisation du Ctrl(3,value) sert a passer le value dans EVENT_VALUE pour l'unité suivante dans une série d'unité
- Soit pour assigner une valeur au pédales d'expression du POD HD 500
- Soit pour déterminer la valeur d'une transition pour le chargement d'une scène du Philips HUE
- Soit pour contrôler Cakewalk

Controller 3 : ref.: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
CC      Bin             Hex     Control function    Value       Used as
3	00000011	03	Undefined	    0-127	MSB
'''
# Lighting patches -----------------------------------------------------------------------------
HueOff=Call(HueBlackout(hue_config))
HueNormal=Call(HueScene(hue_config, "Normal"))
HueGalaxie=Call(HueScene(hue_config, "Galaxie"))
HueGalaxieMax=Call(HueScene(hue_config, "GalaxieMax"))
HueDemon=Call(HueScene(hue_config, "Demon"))
HueSoloRed=Call(HueScene(hue_config, "SoloRed"))
HueDetente=Call(HueScene(hue_config, "Détente"))
HueVeilleuse=Call(HueScene(hue_config, "Veilleuse"))
HueLecture=Call(HueScene(hue_config, "Lecture"))

# SD90 - Sequencer patches -----------------------------------------------
violon = Output('SD90-PART-A', channel=1, program=(Classical,41))

p_hue = Filter(NOTEON) >> [
    KeyFilter(notes=[101]) >> HueNormal, 
    KeyFilter(notes=[102]) >> HueDetente, 
    KeyFilter(notes=[103]) >> HueLecture, 
    KeyFilter(notes=[104]) >> HueVeilleuse, 
    KeyFilter(notes=[105]) >> HueGalaxie, 
    KeyFilter(notes=[106]) >> HueGalaxieMax, 
    KeyFilter(notes=[107]) >> HueDemon, 
    KeyFilter(notes=[108]) >> HueOff, 
    KeyFilter(notes=[109]) >> Ctrl(3, 50) >> HueLecture, 

]

akai_pad_nature = [
    ~Filter(PITCHBEND) >> KeyFilter(notes=[109]) >> LatchNotes(polyphonic=True) >> Key(0) >> Rain,
    KeyFilter(notes=[110]) >> Key(12) >> Thunder,
    KeyFilter(notes=[111]) >> Key(48) >> Dog,
    KeyFilter(notes=[112]) >> Key(24) >> BirdTweet,
    KeyFilter(notes=[113]) >> Key(72) >> Screaming,
    KeyFilter(notes=[114]) >> Key(48) >> Explosion, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[115]) >> Key(12) >> Wind, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[116]) >> LatchNotes(polyphonic=True) >> Key(36) >> Applause, 
]

#-----------------------------------------------------------------------------------------------

# My Cakewalk Generic Control Surface definition -----------------------------------------------
CakeRecord=Ctrl('MPK-MIDI-OUT-3', 1, 119,127)
CakePlay=Ctrl('MPK-MIDI-OUT-3', 1, 118, 127)
CakeStop=Ctrl('MPK-MIDI-OUT-3', 1, 119, 127)
#-----------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------
# Execution patches
#-----------------------------------------------------------------------------------------------


#explosion = Key(0) >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=(Classical+Var3,128), volume=100)
piano_base =  Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=(Classical,1))
nf_piano = Output('SD90-PART-A', channel=1, program=(Classical,2), volume=100)
piano =  Output('SD90-PART-A', channel=3, program=(Classical,1), volume=100)
piano2 = Output('SD90-PART-A', channel=2, program=(Classical,2), volume=100)

# Patch Synth
keysynth =  Velocity(fixed=80) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
marathon_intro=(akai>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Note : ChannelFilter 2 - Enable PK5 message only
marathon_chords=(pk5 >> LatchNotes(False, reset='c4') >> Velocity(fixed=80) >>
	(

		# From first to last...
		(KeyFilter('e3') >> Key('b3') >> Harmonize('b','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('c3') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('d3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //

		# From first to last 2 frets higher
		(KeyFilter('a3') >> Key('c#4') >> Harmonize('c#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('f3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('g3') >> Key('g#3') >> Harmonize('g#','major',['unison', 'third', 'fifth', 'octave'])) // 

        # Isolated note
        (KeyFilter('b3') >> Key('a6'))

	) >> Transpose(-24) >> Output('SD90-PART-A', channel=4, program=(Classical+Var1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(akai >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(akai >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output('SD90-PART-A', channel=4, program=(Classical,51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(akai >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output('SD90-PART-B', channel=11, program=(Enhanced,99), volume=80))

marathon_bridge_split= KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth2 =  Velocity(fixed=115) >> Output('SD90-PART-A', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('SD90-PART-A', channel=1, program=(Enhanced,15), volume=100)
closer_base = Velocity(fixed=100) >> Output('SD90-PART-A', channel=2, program=(Enhanced,51), volume=100)
closer_main =  KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=(Enhanced,92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=(Enhanced,92), volume=100)
tss_keyboard_main =  KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=(Enhanced,103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=(Enhanced,103), volume=100)
tss_foot_main =  KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('SD90-PART-A',channel=1,program=(Solo,53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('SD90-PART-A',channel=1,program=(Solo,53),volume=100,ctrls={91:75}))
analogkid_high = Output('SD90-PART-A', channel=2, program=(Solo,53), volume=100, ctrls={93:75, 91:100})
analogkid_main =  KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending =  Key('a1') >> Output('SD90-PART-A', channel=5, program=(Special2,68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight =  Key('d#6') >> Output('SD90-PART-A', channel=16, program=(Special1,12), volume=100)

# Band : Moi ----------------------------------------------------

# Song : Centurion 

# Init patch 
i_centurion = [
        Call(Playlist(playlist_config)), 
        P02A, Ctrl(3,127) >> Expr2
]

# Execution patch
seq_centurion = (Velocity(fixed=110) >>	
    [
		Output('SD90-PART-A', channel=1, program=(Enhanced,96), volume=110, pan=32),
		Output('SD90-PART-A', channel=2, program=(Enhanced,82), volume=110, pan=96)
	])

# Filter
p_centurion = (LatchNotes(True, reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) //
		(KeyFilter('E3') >> Key('D2')) //
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> seq_centurion)


# Band : Big Country ------------------------------------------

# Song : In a big country

# Init patch
i_big_country = [U01_A, P14A, FS1, FS3, Ctrl(3,127) >> Expr2]

# Execution patch

i_big_country_live = [P14D, FS1, FS3, FS4, Ctrl(3,85) >> Expr2]
p_big_country_live = (pk5 >> KeyFilter(notes=[60]) >> 
        [
            Filter(NOTEON) >> [CakePlay],
            Filter(NOTEOFF) >> HueGalaxieMax, 
        ])

p_big_country = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[69]) >> FS4),
             (KeyFilter(notes=[71]) >> [HueGalaxie, FS2, Ctrl(3,85) >> Expr2]),
             (KeyFilter(notes=[72]) >> [HueSoloRed, FS2, Ctrl(3,127) >> Expr2])
         ])

# Big Country fin de section ------------------------------------------

# Band : Octobre ------------------------------------------

# Init patch (Intro)
i_octobre = [P09A, FS1, FS3, FS4, Ctrl(3,127) >> Expr2]

# Execution patch
p_octobre = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[64]) >> [FS4, Ctrl(3,120) >> Expr2]),
             (KeyFilter(notes=[65]) >> [FS1, Ctrl(3,100) >> Expr2]),
             (KeyFilter(notes=[67]) >> [FS1, FS2, FS4, Ctrl(3,65) >> Expr2]),
             (KeyFilter(notes=[69]) >> [FS2, Ctrl(3,127) >> Expr2]),
             (KeyFilter(notes=[71]) >> [FS1, FS4, Ctrl(3,100 ) >> Expr2])
         ])


# Octobre fin de section ------------------------------------------

# Band : Rush ------------------------------------------

# Default init patch
i_rush = [P02A, Ctrl(3,100) >> Expr2]

# Default patch - tout en paralelle mais séparé par contexte
p_rush = (pk5 >> Filter(NOTEON) >>
    [
        [
            KeyFilter(notes=[60]) >> HueOff,
            KeyFilter(notes=[62]) >> HueGalaxie,
            KeyFilter(notes=[64]) >> HueSoloRed
        ],                
        [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, FS4, Ctrl(3,100) >> Expr2, HueGalaxie],
            KeyFilter(notes=[72]) >> [FS1, FS4, Ctrl(3,120) >> Expr2, HueSoloRed]
        ]
    ])

# Subdivisions

# Init patch
i_rush_sub=[P02A, FS3, Ctrl(3,100) >> Expr2]

# Grand Designs

# Init patch
i_rush_gd = [P02A, FS1, FS3, Ctrl(3,127) >> Expr2] 

# Execution patch
p_rush_gd = (pk5 >> 
    [
        Filter(NOTEON) >> [
                [ 
                    KeyFilter(notes=[60]) >> HueOff,
                    KeyFilter(notes=[61]) >> Ctrl(3, 1) >> HueDemon,
                    KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxie,
                    KeyFilter(notes=[64, 72]) >> Ctrl(3, 1) >> HueSoloRed,
                ],
                [
                    KeyFilter(notes=[67]) >> FS4,
                    KeyFilter(notes=[69]) >> [Ctrl(3, 100) >> Expr2, FS4],
                    KeyFilter(notes=[71]) >> [Ctrl(3, 127) >> Expr2, FS4],
                    KeyFilter(notes=[72]) >>  Ctrl(3, 127) >> Expr2
                ],
            ],
        Filter(NOTEOFF) >> [
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 1) >> HueGalaxie
                ],
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 100) >> Expr2
                ]
            ],
    ])

# Youtube SoundCraftBridge Demo
p_rush_gd_demo = (ChannelFilter(16) >> 
    [
        Filter(NOTEON) >> [
                [ 
                    KeyFilter(notes=[113]) >> Ctrl(3, 50) >> HueLecture,
                    #KeyFilter(notes=[61]) >> Ctrl(3, 1) >> HueDemon,
                    #KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxie,
                    #KeyFilter(notes=[64, 72]) >> Ctrl(3, 1) >> HueSoloRed,
                ],
                [
                    #KeyFilter(notes=[67]) >> FS4,
                    #KeyFilter(notes=[69]) >> [Ctrl(3, 100) >> Expr2, FS4],
                    #KeyFilter(notes=[71]) >> [Ctrl(3, 127) >> Expr2, FS4],
                    #KeyFilter(notes=[72]) >>  Ctrl(3, 127) >> Expr2
                ],
            ],
        Filter(NOTEOFF) >> [
                [
                    #KeyFilter(notes=[72]) >> Ctrl(3, 1) >> HueGalaxie
                ],
                [
                    #KeyFilter(notes=[72]) >> Ctrl(3, 100) >> Expr2
                ]
            ],
    ])

# The Trees

# Init patch
i_rush_trees = [P02A, FS3, Ctrl(3,100) >> Expr2] 

# Foot keyboard output
p_rush_trees_foot = Velocity(fixed=110) >> Output('SD90-PART-A', channel=1, program=(Classical,51), volume=110, ctrls={93:75, 91:75})

# Execution patch
p_rush_trees=(pk5 >>
    [
        # Controle de l'éclairage
        Filter(NOTEON) >> [
            KeyFilter('C3') >> HueGalaxie,
            KeyFilter(notes=[71]) >> HueGalaxie,
            KeyFilter(notes=[72]) >> HueSoloRed,
        ],
        # Controle du POD HD500 
        Filter(NOTEON) >> [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, Ctrl(3,100) >> Expr2],
            KeyFilter(notes=[72]) >> [FS1, Ctrl(3,120) >> Expr2],
        ],
        # Controle du séquenceur 
        # Il faut laisser passer f3 dans un filtre dummy car il sert de Latch
        [
            KeyFilter('C3') >> Key('A0'),
            KeyFilter('D3') >> Key('B0'),
            KeyFilter('E3') >> Key('D1'),
            KeyFilter('f3') >> Pass(),
        ] >> LatchNotes(False, reset='f3') >> p_rush_trees_foot
    ])

# Rush fin de section ------------------------------------------

# ---
# Daw helper
p_transport = (pk5 >> 
        [
            Filter(NOTEON) >> KeyFilter(notes=[60]) >> [CakePlay],
            Filter(NOTEON) >> KeyFilter(notes=[62]) >> [CakeRecord],
            Filter(NOTEOFF) >> HueGalaxieMax, 
        ])

# ---
# Glissando
p_glissando=(Filter(NOTEON) >> Call(glissando, 48, 84, 100, 0.01, -1, 'SD90-PART-A'))

# PORTAMENTO 
#portamento_base=Ctrl(1,1,5,50)
#portamento_off=Ctrl(1,1,65,0)	# Switch OFF
#portamento_on=Ctrl(1,1,65,127)  # Switch ON
#portamento_up=(portamento_base // portamento_on)
#portamento_off=(portamento_base // portamento_off)
#legato=Ctrl(1,1,120,0)

#-----------------------------------------------------------------------------------------------------------
# Control body
# control.py
# Controlleur 1

# AKAI sliders, knobs and switches
nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(1, 2, 3, 7, 4, 20, 21, 22, 23, 24, 25, 26, 69) >>
    CtrlSplit({
        1: Expr1,
        2: Expr2,
        4: GT10B_Tuner,
        7: GT10B_Volume,
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
        26: Program('SD90-PART-A', 1, EVENT_VALUE),
        69: Tuner,
    })
)

# Keyboard Controller : Contexte d'utilisation d'un clavier pour controller le plugins Mp3Player ou le Philips Hue
# Le CC#7 est en % et le CC#1 en secondes pour Mp3Player

key_controller=key_config["controller"]
key_transpose=Transpose(key_controller["transpose"])

key_controller_channel=key_controller["channel"]
key_controller = [
  Filter(NOTEON) >> key_transpose, 
  CtrlFilter(7) >> CtrlValueFilter(0, 101), 
  CtrlFilter(1) >> CtrlValueFilter(0, 121), 
] >> Call(Mp3Player(key_config))

hue_controller_channel = 11
hue_patch = p_hue

spotify_channel = 12
spotify_patch = [
    Filter(NOTEON) >> key_transpose,
    CtrlFilter(7) >> CtrlValueFilter(0, 101), 
    CtrlFilter(1,44),
    ] >> Call(SpotifyPlayer(spotify_config))

# My SoundCraft UI16 series controller patch
osb_port = 56420
scc=configuration["soundcraft_controller_channel"]
sc_controller= [

    CtrlFilter(1,2,3,4,5,6,7,8,9,10,11,12) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range),
    CtrlFilter(13) >> SendOSC(osb_port, '/lmix', 0, data2_to_zero_one_range),
    CtrlFilter(14) >> SendOSC(osb_port, '/lmix', 1, data2_to_zero_one_range),
    CtrlFilter(15) >> SendOSC(osb_port, '/pmix', 0, data2_to_zero_one_range),
    CtrlFilter(16) >> SendOSC(osb_port, '/pmix', 1, data2_to_zero_one_range),
    
    CtrlFilter(17,18,19,20,21,22,23,24,25,26,27,28) >> Process(set_input, offset=-16) >> SendOSC(osb_port, '/mute', sc_input, data2_to_mute),
    CtrlFilter(29) >> SendOSC(osb_port, '/lmute', 0, data2_to_zero_one_range),
    CtrlFilter(30) >> SendOSC(osb_port, '/lmute', 1, data2_to_zero_one_range),
    CtrlFilter(31) >> SendOSC(osb_port, '/pmute', 0, data2_to_zero_one_range),
    CtrlFilter(32) >> SendOSC(osb_port, '/pmute', 1, data2_to_zero_one_range),

    # MASTER
    CtrlFilter(100) >> SendOSC(osb_port, '/master', data2_to_zero_one_range),

    # Reverb channel 1 to 12
    CtrlFilter(33,34,35,36,37,38,39,40,41,42,43,44) >> Process(set_input, offset=-32) >> SendOSC(osb_port, '/reverb', sc_input, data2_to_zero_one_range),

]

# Collection de controllers par channel
controllers = ChannelFilter(key_controller_channel,nav_controller_channel, hue_controller_channel, spotify_channel, scc)
_control = (
	controllers >>
	ChannelSplit({
		key_controller_channel: key_controller,
		nav_controller_channel: nav_controller,
        hue_controller_channel: hue_patch,
        spotify_channel : spotify_patch,
        scc : sc_controller
	})
)

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Scenes body
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Initialize", init_patch=SD90_Initialize, patch=Discard()),
    2: SceneGroup("Rush",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Subdivisions", init_patch=i_rush_sub, patch=p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("Divers", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("PowerWindows", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("GraceUnderPressure", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush_gd, patch=p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
        ]),
    3: SceneGroup("BassCover",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Default", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("Queen", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("T4F", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("Toto", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
        ]),
    4: SceneGroup("HBR",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("YYZ", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("Limelight", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("FlyByNight", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("RedBarchetta", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("Freewill", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("SpritOfRadio", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("TomSawyer", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("CloserToTheHeart", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
        ]),
    5: SceneGroup("BigCountry",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("In a big country", init_patch=i_big_country, patch=p_big_country),
            Scene("In a big country LIVE", init_patch=i_big_country_live, patch=p_big_country // p_big_country_live),
        ]),
    6: SceneGroup("GrandDesignsStudio",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("PowerWindows", init_patch=Call(Playlist(playlist_config)), patch=p_rush_gd_demo),
            Scene("Futur", init_patch=Discard(), patch=p_transport),
        ]),
    7: SceneGroup("Demonstrations",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("BrushingSaw", LatchNotes(False, reset='f3') >> Transpose(-24) >> BrushingSaw),
            Scene("Xtremities", Xtremities),
            Scene("BagPipe", BagPipe),
            Scene("Borealis", Borealis),
            Scene("FifthAtmAft", FifthAtmAft),
            Scene("RichChoir", RichChoir),
            Scene("CircularPad", CircularPad),
            Scene("Oxigenizer", Oxigenizer),
            Scene("Quasar", Quasar),
            Scene("HellSection", HellSection),
            Scene("Demon", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Jokes", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Tabarnac", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("TLMEP", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
        ]),
    8: SceneGroup("Compositions",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Palindrome", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Centurion", init_patch=i_centurion, patch=p_centurion),
        ]),
    9: SceneGroup("MP3Player",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Majestyx", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("MajestyxBasse", init_patch=Call(Playlist(playlist_config))//U03_A, patch=Discard()),
            Scene("Delirium", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Hits", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Middleage", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("NinaHagen", init_patch=Call(Playlist(playlist_config)), patch=Discard()),            
            Scene("SteveMorse", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Timeline", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("TV", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
        ]),
    10: SceneGroup("Spotify", 
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Rush", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch=Discard(),  init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE Bridge",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Demon", init_patch=HueDemon, patch=Discard()),
            Scene("SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Off", init_patch=HueOff, patch=Discard()),
        ]),
    12: SceneGroup("Octobre",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Maudite Machine", init_patch=i_octobre, patch=p_transport // p_octobre),
        ]),}
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
# Run region
#-----------------------------------------------------------------------------------------------------------
# PROD
pre  = ~ChannelFilter(8, 9, 11) // ~Filter(SYSRT_CLOCK)
post = Pass()

# DEBUG
#pre  = Print('input', portnames='in')
#post = Print('output',portnames='out')

run(
    control=_control,
    scenes=_scenes,
    pre=pre,
    #post=post,
)
