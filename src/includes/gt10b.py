
#
# The Boss GT-10B definition file for mididings
# This device has 4 banks, each bank contains 100 programs 
#

# Internal Midi channel configured in the GT10B USB options
GT10BChannel = 16

GT10BankSelector = CtrlValueFilter(0, 3) >> [
      Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE), 
      Ctrl(gt10b_midi, GT10BChannel, 32, 0),
]
GT10Bank0 = Ctrl(0, 0) >> GT10BankSelector
GT10Bank1 = Ctrl(0, 1) >> GT10BankSelector
GT10Bank2 = Ctrl(0, 2) >> GT10BankSelector
GT10Bank3 = Ctrl(0, 3) >> GT10BankSelector

GT10BProgramSelector = Program(gt10b_midi, channel = GT10BChannel, program = EVENT_VALUE)

# Send CC
GT10B_Ctrl =  Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)

# Send CC aliases
GT10B_Tuner = Ctrl(gt10b_midi, GT10BChannel, EVENT_CTRL, EVENT_VALUE)    
GT10B_Volume = GT10B_Ctrl
GT10B_Expression = GT10B_Ctrl

# Mididings control patch
gt10b_control = (Filter(CTRL) >> 
    CtrlSplit({
          4: GT10B_Tuner,
          7: GT10B_Volume,
         20: GT10BProgramSelector
    }))