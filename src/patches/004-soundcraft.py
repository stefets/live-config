'''
    The Soundcraft UI 16 patches for mididings
    Those patches use the OSC protocol to communicate with the Osc Soundcraft Bridge daemon
    https://github.com/stefets/osc-soundcraft-bridge
'''

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

# Input patches / stands for all XLR+1/4 sockets
#

mixbase  = SendOSC(osb_port, mixpath,  ui_event, ui_cursor)
mutebase = SendOSC(osb_port, mutepath, ui_event, ui_mute)
revbase  = SendOSC(osb_port, revpath,  ui_event, ui_cursor)

mixbase_stereo = [
        SendOSC(osb_port, mixpath, ui_left,  ui_cursor),    
        SendOSC(osb_port, mixpath, ui_right, ui_cursor),
    ]

mutebase_stereo = [
        SendOSC(osb_port, mutepath, ui_left,  ui_mute),    
        SendOSC(osb_port, mutepath, ui_right, ui_mute),
    ]

# Line patches
ui_line_mute=[
        SendOSC(osb_port, "/lmute", 0, ui_mute),    
        SendOSC(osb_port, "/lmute", 1, ui_mute),
    ]
    
ui_line_mix=[
        SendOSC(osb_port, linepath, 0, ui_cursor),    
        SendOSC(osb_port, linepath, 1, ui_cursor),
    ]

# Player patches
ui_player_mute=[
        SendOSC(osb_port, "/pmute", 0, ui_mute),    
        SendOSC(osb_port, "/pmute", 1, ui_mute),
    ]
    
ui_player_mix=[
        SendOSC(osb_port, playpath, 0, ui_cursor),    
        SendOSC(osb_port, playpath, 1, ui_cursor),
    ]

# -----------------------------------------------------
