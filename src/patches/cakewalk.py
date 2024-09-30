
#
# Cakewalk Generic Control Surface definition -----------------------------------------------
#

# Setup controllers
cw_rew  = 115
cw_fwd  = 116
cw_stop = 117
cw_play = 118
cw_rec  = 119

# Allowed controllers
ctrls = [cw_rec, cw_stop, cw_play, cw_rec, cw_fwd]

# Trigger value
cw_trigger_value = 127

# Output port
cw_port = sd90_midi_2

# ---------------

# Execution patches
CakewalkController = CtrlFilter(ctrls) >> Ctrl(cw_port, EVENT_CHANNEL, EVENT_CTRL, cw_trigger_value) 

# Direct DAW patch
CakeStop   = Ctrl(cw_stop, EVENT_VALUE) >> CakewalkController
CakePlay   = Ctrl(cw_play, EVENT_VALUE) >> CakewalkController
CakeRecord = Ctrl(cw_rec,  EVENT_VALUE) >> CakewalkController

# WIP
CakeRewind = Ctrl(cw_rew, EVENT_VALUE) >> CakewalkController
CakeForward= Ctrl(cw_fwd, EVENT_VALUE) >> CakewalkController
