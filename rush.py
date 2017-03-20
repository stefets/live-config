from mididings import *
from mididings.extra import *

config(

    client_name = 'Master',

    out_ports = [ 
        ('q49', '20:0','.*SD-90 Part A'),
        ('pk5', '20:0','.*SD-90 Part A') ],

    in_ports = [ ('MidiDings IN 1', '20:2','.*SD-90 MIDI 1') ],

)

_pre = Print('input', portnames='in')
_post = Print('output', portnames='out')

_control = Filter(NOTEON) >> (KeyFilter('C1') % (SceneSwitch(offset=1), SceneSwitch(offset=-1)))

patch = Output('q49', channel=1, program=22, volume=100)

# RUSH
barchetta = Velocity(fixed=80) >> Output('pk5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})
freewill = Transpose(12) >> Velocity(fixed=80) >> Output('pk5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})
#barchetta = LatchNotes(False,reset='C3') >> Velocity(fixed=80) >> Output('pk5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})
#freewill = Transpose(12) >> LatchNotes(False,reset='E4') >> Velocity(fixed=80) >> Output('pk5', channel=1, program=82, volume=100, ctrls={93:75, 91:75})

#closer_high = Transpose(0) >> Output('q49', 1, 15, 100)
#closer_base = Transpose(0) >> Output('q49', 2, 51, 110)
#closer_main = KeySplit('c3', closer_base, closer_high)

_scenes = {
    1: Scene("PatchName", patch),
    2: barchetta,
    3: freewill
}

run(
    control=_control,
    pre=_pre, 
#    post=_post,
    scenes=_scenes, 
)

