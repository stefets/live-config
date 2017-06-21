#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess
from threading import Timer
from time import sleep
from mididings import *
from mididings.extra import *
from mididings.engine import *
from mididings.event import *
from mididings.extra.inotify import AutoRestart

config(

    backend = 'alsa',

    client_name = 'Master',

    out_ports = [ 
        ('Q49', '20:0','.*SD-90 Part A'),
        ('PK5', '20:0','.*SD-90 Part A'), ],

    in_ports = [ 
        ('SD90 - MIDI IN 1', '20:2','.*SD-90 MIDI 1'),
        ('SD90 - MIDI IN 2', '20:3','.*SD-90 MIDI 2') ],

    initial_scene = 1,
)

hook(
    #MemorizeScene('scene.txt'),
    AutoRestart(),
)

#--------------------------------------------------------------------
# Test
def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev
#--------------------------------------------------------------------

# Glissando
def gliss_function(note, note_max, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    note += 1
    if note < note_max:
        Timer(.01, lambda: gliss_function(note, note_max, port, chan, vel)).start()

def gliss_exec(e):
    gliss_function(120, 168, e.port, e.channel, 100)

# Arpeggiator
def arpeggiator_function(current, max,note, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    current += 1
    if current < max:
        Timer(.15, lambda: arpeggiator_function(current, max, note,  port, chan, vel)).start()

def arpeggiator_exec(e):
    arpeggiator_function(0,16, 50,  e.port, e.channel, 100)


# For SD-90 only
def SendSysex(ev):
    return SysExEvent(ev.port, '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')
#--------------------------------------------------------------------

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
            css=current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css+1)
            else:
                switch_subscene(1)
    elif ev.ctrl == 22:
        subprocess.Popen(['/bin/bash', './kill.sh'])

#--------------------------------------------------------------------

# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')
#--------------------------------------------------------------------

# Controller pour le changement de scene (fcb1010 actual)
_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(20,22) >> Process(NavigateToScene)

# For debug
#_control = ChannelFilter(1) >> Filter(CTRL) >> CtrlFilter(1) >> CtrlValueFilter(0) >> Call(gliss_exec)
#_control = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter([20,22]) >> Process(Glissando)
_control = Filter(NOTE) >> Filter(NOTEON) >> Call(arpeggiator_exec)
#--------------------------------------------------------------------

# Exclude channel 9 (fcb1010 control scene change via channel 9)
cf=~ChannelFilter(9)
#--------------------------------------------------------------------

# Shortcut (fcb1010)
play = Filter(CTRL) >> CtrlFilter(21)
#--------------------------------------------------------------------

# FX Section
explosion = cf >> Key(0) >> Velocity(fixed=100) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth = cf >> Velocity(fixed=80) >> Output('PK5', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('PK5', channel=1, program=51, volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('Q49', 1, program=((99*128),15), volume=100)
closer_base = Velocity(fixed=100) >> Output('PK5', 2, program=((99*128),51), volume=100)
closer_main = cf >> KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('Q49', channel=3, program=((99*128),92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('Q49', channel=3, program=((99*128),92), volume=100)
tss_keyboard_main = cf >> KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_main = cf >> KeySplit('d#3', tss_foot_left, tss_foot_right)
#--------------------------------------------------------------------

# Patch Analog Kid
analogkid = cf >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'third', 'fifth', 'octave']) >> Velocity(fixed=50) >> Output('PK5', channel=1, program=((99*128),50), volume=75)
analogkid_ending = cf >> Key('a1') >> Output('PK5', channel=5, program=((81*128),68), volume=100)
#--------------------------------------------------------------------

# Patch Limelight
limelight = cf >> Key('d#6') >> Output('PK5', channel=16, program=((80*128),12), volume=100)

# Patch debug
#debug = (ChannelFilter(1) >> Output('PK5', channel=1, program=((99*128), 1), volume=100)) // (ChannelFilter(2) >> Output('Q49', channel=3, program=((99*128), 10), volume=101))
#piano=Harmonize('c', 'major', ['unison','octave']) >> Output('Q49', channel=1, program=((99*128),1), volume=100)
piano= cf >> Transpose(0) >> Output('Q49', channel=1, program=((99*128),37), volume=100)
#--------------------------------------------------------------------

# Liste des scenes
init=Filter(CTRL) >> CtrlFilter(22) >> Process(SendSysex)
_scenes = {
    1: Scene("Initialize",  piano),
    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    3: Scene("FreeWill", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    4: Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, ChannelFilter(2) >> Transpose(-24) >> closer_base]),
    5: SceneGroup("The Trees", [
            Scene("Bridge",  play >> System("mpg123 -q /mnt/flash/live/trees_full.mp3")),
            Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    6: SceneGroup("Time Stand Still", [
			Scene("TSS-Intro", play >> System("mpg123 -q /mnt/flash/live/tss.mp3")),
			Scene("TSS-Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
	   ]),
    7: SceneGroup("2112", [
            Scene("Intro", play >> System("mpg123 -q /mnt/flash/live/2112.mp3")),
            Scene("Explosion", explosion),
       ]),
    8: Scene("Analog Kid", [ChannelFilter(2) >> analogkid, ChannelFilter(1) >> analogkid_ending ]),
    9: Scene("EntreNous", play >> System("mpg123 -q /mnt/flash/live/entrenous.mp3")),
    10: Scene("Circumstances bridge", play >> System("mpg123 -q /mnt/flash/live/circumstances.mp3")),
    11: Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    12: SceneGroup("Bass cover", [
            Scene("Toto - Rossana", play >> System("mpg123 -q /mnt/flash/solo/audio/toto_rossana_no_bass.mp3")),
            Scene("Toto - Africa", play >> System("mpg123 -q /mnt/flash/solo/audio/toto_africa_no_bass.mp3")),
            Scene("Yes - Owner of a lonely heart", play >> System("mpg123 -q /mnt/flash/solo/audio/yes_owner_lonely_heart.mp3")),
            Scene("Queen - I want to break free", play >> System("mpg123 -q /mnt/flash/solo/audio/queen_want_break_free.mp3")),
            Scene("Queen - Under Pressure", play >> System("mpg123 -q /mnt/flash/solo/audio/queen_under_pressure.mp3")),
            Scene("Queen - Crazy little thing called love", play >> System("mpg123 -q /mnt/flash/solo/audio/queen_crazy_little_thing_called_love.mp3")),
            Scene("Queen - Another one bites the dust", play >> System("mpg123 -q /mnt/flash/solo/audio/queen_another_on_bites_dust.mp3")),
            Scene("ZZ Top - Sharp dressed man", play >> System("mpg123 -q /mnt/flash/solo/audio/zz_top_sharp_dressed_man.mp3")),
            Scene("Tears for fears - Head over heels", play >> System("mpg123 -q /mnt/flash/solo/audio/t4f_head_over_heels.mp3")),
            Scene("Tears for fears - Everybody wants to rule the world", play >> System("mpg123 -q /mnt/flash/solo/audio/t4f_everybody.mp3")),
            Scene("Police - Walking on the moon", play >> System("mpg123 -q /mnt/flash/solo/audio/police_walking_moon.mp3")),
            Scene("Police - Message in a bottle", play >> System("mpg123 -q /mnt/flash/solo/audio/police_message_bottle.mp3")),
            Scene("Led Zeppelin - Rock and roll", play >> System("mpg123 -q /mnt/flash/solo/audio/led_zeppelin_rock_and_roll.mp3")),
            Scene("Bon Jovi - Livin on a prayer", play >> System("mpg123 -q /mnt/flash/solo/audio/bon_jovi_prayer.mp3")),
            Scene("Pat Metheny - Letter from home", play >> System("mpg123 -q /mnt/flash/solo/audio/letter_from_home.mp3")),
            Scene("Muse - Uprising", play >> System("mpg123 -q /mnt/flash/solo/audio/uprising.mp3")),
            Scene("Compo - Shadow", play >> System("mpg123 -q /mnt/flash/solo/audio/shadow.mp3")),
       ]),
    13: SceneGroup("Rush guitar cover", [    
            Scene("Rush - Limelight", play >> System("mpg123 -q /mnt/flash/solo/audio/limelight.mp3")),
            Scene("Rush - RedBarchetta ", play >> System("mpg123 -q /mnt/flash/solo/audio/barchetta.mp3")),
            Scene("Rush - FlyByNight ", play >> System("mpg123 -q /mnt/flash/solo/audio/fly_by_night.mp3")),
            Scene("Rush - Spirit of Radio ", play >> System("mpg123 -q /mnt/flash/solo/audio/spirit_of_radio.mp3")),
       ]),
    14: SceneGroup("AnalogKid", [
            Scene("Rush - AnalogKid", play >> System("mpg123 -q /mnt/flash/solo/audio/analogkid.mp3")),
			Scene("Analog Kid Keyboard", [ChannelFilter(2) >> analogkid, ChannelFilter(1) >> analogkid_ending ]),
       ]),	 
    15: SceneGroup("TimeStandSteel", [
            Scene("Rush - TimeStandSteel", play >> System("mpg123 -q /mnt/flash/solo/audio/time_stand_steel.mp3")),
			Scene("Time Stand Still Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
       ]),	 
    16: SceneGroup("KidGloves", [
            Scene("Rush - KidGloves ", play >> System("mpg123 -q /mnt/flash/solo/audio/kid_gloves.mp3")),
			Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
       ]),   
    17: SceneGroup("Freewill", [
            Scene("Rush - Freewill ", play >> System("mpg123 -q /mnt/flash/solo/audio/freewill.mp3")),
			Scene("FreeWill Keyboard", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
       ]),   
}

# ---------------------------
run(
    control=_control,
    pre=_pre, 
    #post=_post,
    scenes=_scenes, 
)
# ---------------------------
