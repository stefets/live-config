
#
# The Boss GT-1000 definition file for mididings
# This device has 4 banks, each bank contains 50 programs 
#

# Internal Midi channel configured in the gt1k USB options
gt1k_channel = 9

gt1kBankSelector = CtrlValueFilter(0, 4) >> [
      Ctrl(gt1000_midi_1, gt1k_channel, EVENT_CTRL, EVENT_VALUE), 
      Ctrl(gt1000_midi_1, gt1k_channel, 32, 0),
]
gt1kBank1 = Ctrl(0, 0) >> gt1kBankSelector
gt1kBank2 = Ctrl(0, 1) >> gt1kBankSelector
gt1kBank3 = Ctrl(0, 2) >> gt1kBankSelector
gt1kBank4 = Ctrl(0, 3) >> gt1kBankSelector

gt1kProgramSelector = Program(gt1000_midi_1, channel = gt1k_channel, program = EVENT_VALUE)

# Send CC
#gt1k_Ctrl =  Ctrl(gt1k_midi_1, gt1k_channel, EVENT_CTRL, EVENT_VALUE)

# Send CC aliases
#gt1k_Tuner = Ctrl(gt1k_midi_1, gt1k_channel, EVENT_CTRL, EVENT_VALUE)
#gt1k_Volume = gt1k_Ctrl
#gt1k_Expression = gt1k_Ctrl

# Mididings control patch
#gt1k_control = (Filter(CTRL) >> 
#    CtrlSplit({
#          4: gt1k_Tuner,
#          7: gt1k_Volume,
#         20: gt1kProgramSelector
#    }))