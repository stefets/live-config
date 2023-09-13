
#
# The Line 6 POD-HD-500 definition patches for mididings
#

# Channel d'écoute
hd500_channel = 15

# Connecté a quel port MIDI ?
hd500_port = mpk_midi

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

# Abstract patch (must be chained before by a Ctrl(c,v))
# Example: 
#       Ctrl(69, 127) >> CtrlPod will set the tuner on.
# mean  Ctrl(hd500_port, hd500_channel, 69, 127)
CtrlPod = Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)

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
HD500_Expr1 = Ctrl(hd500_port, hd500_channel, 1, EVENT_VALUE)
HD500_Expr2 = Ctrl(hd500_port, hd500_channel, 2, EVENT_VALUE)

# HD500_Tuner (shortcut)
HD500_Tuner = CtrlPod

HD500_TunerOn  = Ctrl(hd500_port, hd500_channel, 69, 127)
HD500_TunerOff = Ctrl(hd500_port, hd500_channel, 69, 0)

# Looper
HD500_Looper = CtrlFilter(60, 61, 62, 63, 65, 67, 68, 99) >> CtrlPod

# Tap
# Expected EVENT_VALUE between 64 and 127
HD500_Tap = Ctrl(hd500_port, hd500_channel, 64, EVENT_VALUE)
