
#
# The Line 6 POD-HD-500 definition patches for mididings
#

# Listen channel
hd500_channel = 15

# Connecté a quel port MIDI ?
hd500_port = mpk_midi

# Programs
HD500ProgramSelector = Program(hd500_port, channel = hd500_channel, program = EVENT_VALUE)

# Abstract patch (must be chained before by a Ctrl(c,v))
# Example: 
#       Ctrl(69, 127) >> CtrlPod will set the tuner on.
# mean  Ctrl(hd500_port, hd500_channel, 69, 127)
CtrlPodBase = Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)

# Footswitch
FS1 = Ctrl(51, 64) >> CtrlPodBase
FS2 = Ctrl(52, 64) >> CtrlPodBase
FS3 = Ctrl(53, 64) >> CtrlPodBase
FS4 = Ctrl(54, 64) >> CtrlPodBase
FS5 = Ctrl(55, 64) >> CtrlPodBase
FS6 = Ctrl(56, 64) >> CtrlPodBase
FS7 = Ctrl(57, 64) >> CtrlPodBase
FS8 = Ctrl(58, 64) >> CtrlPodBase
TOE = Ctrl(59, 64) >> CtrlPodBase

# Exp1 et Exp2
HD500_Expr1 = Ctrl(1, EVENT_VALUE) >> CtrlPodBase
HD500_Expr2 = Ctrl(2, EVENT_VALUE) >> CtrlPodBase

# HD500_Tuner (shortcut)
HD500_Tuner = CtrlPodBase

HD500_TunerOn  = Ctrl(69, 127) >> CtrlPodBase
HD500_TunerOff = Ctrl(69, 0) >> CtrlPodBase

# Looper
HD500_Looper = CtrlFilter(60, 61, 62, 63, 65, 67, 68, 99) >> CtrlPodBase

# Tap
# Expected EVENT_VALUE between 64 and 127
HD500_Tap = Ctrl(64, EVENT_VALUE) >> CtrlPodBase

# Mididings HD500 control patch
hd500_control = (Filter(CTRL) >>
    CtrlSplit({
          1: HD500_Expr1,
          2: HD500_Expr2,
         69: HD500_Tuner,
         20: HD500ProgramSelector
    }))