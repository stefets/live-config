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
    switch_scene(ev.ctrl)

# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

# Controller pour le changement de scene
_control = Filter(CTRL) >> CtrlFilter([20,21,22]) >> Process(NavigateToScene)

_intro = Output('Q49', channel=1, program=22, volume=100)

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth =  Velocity(fixed=80) >> Output('PK5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})

# Patche pour Closer to the earth
closer_high = Output('Q49', 1, 15, 100)
closer_base = Output('Q49', 2, 51, 110)
closer_main = KeySplit('c3', closer_base, closer_high)

_scenes = {
    2:  Scene("Intro", _intro),
    1:  Scene("MP3", Filter(CTRL) >> CtrlSplit({ 23: System("mpg123 /mnt/flash/root/online.mp3")})),
    20: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> keysynth),
    21: Scene("FreeWill", Transpose(12) >> LatchNotes(False,reset='E4') >> keysynth),
    22: Scene("CloserToTheHeart", closer_main)
}

run(
    control=_control,
    pre=_pre, 
#    post=_post,
    scenes=_scenes, 
)

