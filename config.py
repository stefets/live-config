#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mididings import *
from mididings.extra import *
from mididings.engine import *
from mididings.event import *

config(

    client_name = 'Master',

    out_ports = [ 
        ('Q49', '20:0','.*SD-90 Part A'),
        ('PK5', '20:0','.*SD-90 Part A'), ],

    in_ports = [ 
        ('SD90 - MIDI IN 1', '20:2','.*SD-90 MIDI 1'),
        ('SD90 - MIDI IN 2', '20:3','.*SD-90 MIDI 2') ],

    initial_scene = 8,
)


def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev

def SendSysex(ev):
    return SysExEvent(ev.port, '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')

# Scene navigation
def NavigateToScene(ev):
    nb_scenes = len(scenes())    
    if ev.ctrl == 20:
        cs=current_scene()
        if ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs+1)
        elif ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
        elif ev.value == 3:
            #TODO - wrap subscene
            css=current_subscene()
            switch_subscene(css+1)
        elif ev.value == 3:
            restart()    

# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

# Controller pour le changement de scene
_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(20) >> Process(NavigateToScene)

# Play Switch (ToTry)
#play = Filter(CTRL) >> CtrlFilter(21)

# FX
explosion = Velocity(fixed=80) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)

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
tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=75)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=75)
tss_foot_main = KeySplit('d#3', tss_foot_left, tss_foot_right)

# Patch pour Analog Kid
analogkid=Transpose(-24) >> Harmonize('c', 'major', ['unison', 'third', 'fifth']) >> Output('Q49', channel=1, program=((99*128),49), volume=100)

# Patch debug
#debug = (ChannelFilter(1) >> Output('PK5', channel=1, program=((99*128), 1), volume=100)) // (ChannelFilter(2) >> Output('Q49', channel=3, program=((99*128), 10), volume=101))

init=Filter(NOTE) >> Process(SendSysex)

# Liste des scenes
_scenes = {
    1: Scene("Initialize",  init),
    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> keysynth),
    3: Scene("FreeWill", Transpose(12) >> LatchNotes(False,reset='E4') >> keysynth),
    4: Scene("CloserToTheHeart", closer_main),
    5: SceneGroup("The Trees", [
           Scene("Bridge",  Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/rush/trees_full.mp3")),
           Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    6: SceneGroup("Time Stand Still", [
           Scene("Q49@ch1 & PK5@ch2", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
       ]),
    7: SceneGroup("2112", [
           Scene("Intro", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/rush/2112.mp3")),
           Scene("Explosion", explosion),
       ]),
    8: Scene("AnalogKid", analogkid),
    9: SceneGroup("Bass cover", [
           Scene("Toto - Rossana", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/toto_rossana_no_bass.mp3")),
           Scene("Toto - Africa", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/toto_africa_no_bass.mp3")),
           Scene("Yes - Owner of a lonely heart", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/yes_owner_lonely_heart.mp3")),
           Scene("Queen - I want to break free", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_want_break_free.mp3")),
           Scene("Queen - Under Pressure", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_under_pressure.mp3")),
           Scene("Queen - Crazy little thing called love", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_crazy_little_thing_called_love.mp3")),
           Scene("Queen - Another one bites the dust", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/queen_another_on_bites_dust.mp3")),
           Scene("ZZ Top - Sharp dressed man", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/zz_top_sharp_dressed_man.mp3")),
           Scene("Tears for fears - Head over heels", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/t4f_head_over_heels.mp3")),
           Scene("Tears for fears - Everybody wants to rule the world", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/t4f_everybody.mp3")),
           Scene("Police - Walking on the moon", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/police_walking_moon.mp3")),
           Scene("Police - Message in a bottle", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/police_message_bottle.mp3")),
           Scene("Led Zeppelin - Rock and roll", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/led_zeppelin_rock_and_roll.mp3")),
           Scene("Bon Jovi - Livin on a prayer", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 -q /mnt/flash/solo/audio/bon_jovi_prayer.mp3")),
       ])
}

# ---------------------------
run(
    control=_control,
    pre=_pre, 
    post=_post,
    scenes=_scenes, 
)
# ---------------------------
