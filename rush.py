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
        if ev.value == 0:
            if cs < nb_scenes:
                switch_scene(cs+1)
        elif ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
        elif ev.value == 2:
            css=current_subscene()
            switch_subscene(css+1)
    
# Pre/Post
_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

# Controller pour le changement de scene
_control = Filter(CTRL) >> CtrlFilter(20) >> Process(NavigateToScene)

_intro = Output('Q49', channel=1, program=22, volume=100)

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth =  Velocity(fixed=80) >> Output('PK5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})

# Patche pour Closer to the earth
closer_high = Output('Q49', 1, 15, 100)
closer_base = Output('Q49', 2, 51, 110)
closer_main = KeySplit('c3', closer_base, closer_high)

_scenes = {
    1: Scene("Intro", _intro),
    2: Scene("MP3", Filter(CTRL) >> CtrlFilter(21) >> System("mpg123 /mnt/flash/root/online.mp3")),
    3: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> keysynth),
    4: Scene("FreeWill", Transpose(12) >> LatchNotes(False,reset='E4') >> keysynth),
    5: Scene("CloserToTheHeart", closer_main),
    6: SceneGroup("2112", [
           Scene("Intro",  Filter(CTRL) >> CtrlSplit({ 21: System("mpg123 /mnt/flash/rush/2112.mp3")})),
           Scene("Explosion",  Filter(CTRL) >> CtrlSplit({ 21: System("mpg123 /mnt/flash/alert.mp3")})),
       ]),
}

run(
    control=_control,
#    pre=_pre, 
#    post=_post,
    scenes=_scenes, 
)

