#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mididings import *
from mididings.extra import *
from mididings.engine import *

config(

    client_name = 'Master',

    out_ports = [ 
        ('Q49', '20:0','.*SD-90 Part A'),
        ('PK5', '20:0','.*SD-90 Part A') ],

    in_ports = [ 
        ('MidiDings IN 1', '20:2','.*SD-90 MIDI 1'),
        ('MidiDings IN 2', '20:3','.*SD-90 MIDI 2') ],
)

# Scene navigation
def NavigateToScene(ev):
    nb_scenes = len(scenes())    
    if ev.ctrl == 20:
        cs=current_scene()
        if ev.value == 1:
            if cs < nb_scenes:
                switch_scene(cs+1)
        elif ev.value == 0:
            if cs > 1:
                switch_scene(cs-1)
        elif ev.value == 2:
            #TODO - wrap subscene
            css=current_subscene()
            switch_subscene(css+1)
    
# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

# Controller pour le changement de scene
_control = Filter(CTRL) >> CtrlFilter(20) >> Process(NavigateToScene)

# Play Switch (ToTry)
#play = Filter(CTRL) >> CtrlFilter(21)

# FX
explosion = Velocity(fixed=100) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth = Velocity(fixed=80) >> Output('PK5', channel=1, program=((99*128),82), volume=100, ctrls={93:75, 91:75})

# Patch Syhth. generique pour lowbase
lowsynth = Velocity(fixed=100) >> Output('PK5', channel=1, program=51, volume=100, ctrls={93:75, 91:75})

# Patch pour Closer to the hearth
closer_high = Output('Q49', 1, 15, 100)
closer_base = Output('Q49', 2, 51, 110)
closer_main = KeySplit('c3', closer_base, closer_high)

# Patch pour Time Stand Still
tss_high = Velocity(fixed=90) >> Output('Q49', channel=1, program=((99*128),92), volume=100)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('Q49', channel=1, program=((99*128),92), volume=100)
tss_keyboard_main = KeySplit('c2', tss_base, tss_high)
tss_foot_left = Transpose(-24) >> Velocity(fixed=100) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-36) >> Velocity(fixed=100) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_main = KeySplit('d#3', tss_foot_left, tss_foot_right)

# Patch debug
debug = Output('PK5', channel=1, program=((99*128), 1), volume=100)

# Liste des scenes
_scenes = {
    6: Scene("Debug", debug),
    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> keysynth),
    3: Scene("FreeWill", Transpose(12) >> LatchNotes(False,reset='E4') >> keysynth),
    4: Scene("CloserToTheHeart", closer_main),
    5: SceneGroup("The Trees", [
           Scene("Bridge",  Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/rush/trees_full.mp3")),
           Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    1: SceneGroup("Time Stand Still", [
           Scene("Q49@ch1 & PK5@ch2", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
       ]),
    7: SceneGroup("2112", [
           Scene("Intro", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/rush/2112.mp3")),
           Scene("Explosion", explosion),
       ])
}

# ---------------------------
run(
    control=_control,
    pre=_pre, 
    #post=_post,
    scenes=_scenes, 
)
# ---------------------------
