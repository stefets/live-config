
'''
    My Soundcraft UI 16 definition file for mididings
    This module use the OSC protocol to communicate with the Osc Soundcraft Bridge daemon
'''
# 0-127 to 0-1
ratio=0.7874015748 / 100

def ui_cursor(ev):
    return ev.data2 * ratio

def ui_knob(ev):
    return ui_cursor(ev)

def ui_mute(ev):
    return 1 if ev.data2==127 else 0

''' Return the controller value for SendOsc '''
def ui_event(ev, offset=0):
    return ev.ctrl+offset if ev.type == CTRL else -1

''' Wrapper over ui_event '''
def ui_left(ev):
    return ui_event(ev)

''' Wrapper over ui_event '''
def ui_right(ev):
    return ui_event(ev, 1)

def set_input(ev, offset):
    ev.ctrl = ev.ctrl + offset
    return ev

# Osc Soundcraft Bridge definition
osb_port    = 56420
mainpath    = "/master"
linepath    = "/lmix"
playpath    = "/pmix"
mixpath     = "/mix"
revpath     = "/reverb"
mutepath    = "/mute"

# Main volume
ui_master=SendOSC(osb_port, mainpath, ui_cursor)

# 
#GENERIC: Stand for ALL XLR+1/4 sockets
mixbase  = SendOSC(osb_port, mixpath,  ui_event, ui_cursor)
mutebase = SendOSC(osb_port, mutepath, ui_event, ui_mute)
revbase  = SendOSC(osb_port, revpath,  ui_event, ui_cursor)

#CUSTOM: Hardware filter via my Akai mpk249 - thanks to the 32 channel
# I can use the same control number with 2 different ports
ui_mix=PortSplit({
    "MPK-MIDI-IN-1" : mixbase,
    "MPK-MIDI-IN-2" : mutebase,
})

# Hard ruled stereo patch with +1 offset for the right channel
ui_stereo_mix=PortSplit({
    "MPK-MIDI-IN-1" : [
        SendOSC(osb_port, mixpath, ui_left,  ui_cursor),    
        SendOSC(osb_port, mixpath, ui_right, ui_cursor),
    ],
    "MPK-MIDI-IN-2" : [
        SendOSC(osb_port, mutepath, ui_left,  ui_mute),    
        SendOSC(osb_port, mutepath, ui_right, ui_mute),
    ]
})

ui_line=PortSplit({
    "MPK-MIDI-IN-1" : [
        SendOSC(osb_port, linepath, 0, ui_cursor),    
        SendOSC(osb_port, linepath, 1, ui_cursor),
    ],
    "MPK-MIDI-IN-2" : [
        SendOSC(osb_port, "/lmute", 0, ui_mute),    
        SendOSC(osb_port, "/lmute", 1, ui_mute),
    ]
})

ui_player=PortSplit({
    "MPK-MIDI-IN-1" : [
        SendOSC(osb_port, playpath, 0, ui_cursor),    
        SendOSC(osb_port, playpath, 1, ui_cursor),
    ],
    "MPK-MIDI-IN-2" : [
        SendOSC(osb_port, "/pmute", 0, ui_mute),    
        SendOSC(osb_port, "/pmute", 1, ui_mute),
    ]
})
