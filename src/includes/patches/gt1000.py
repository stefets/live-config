
#
# The Boss GT-1000 definition file for mididings
# This device has 4 banks, each bank contains 50 programs 
#

gt1k_port = "mpk249_midi"

# Internal Midi channel configured in the gt1k USB options
gt1k_listen_channel = 9

gt1k = CtrlSplit({
    55 : [Print("OK"),Ctrl(gt1k_port, gt1k_listen_channel, 1, EVENT_VALUE)],
})



