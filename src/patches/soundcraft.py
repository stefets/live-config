
'''
    The Soundcraft UI 16 patches for mididings
    Those patches use the OSC protocol to communicate with the Osc Soundcraft Bridge daemon
    The CC number correspond to the SoundCraft input channel
    The CC value correspond to the SoundCraft cursor value 
    https://github.com/stefets/osc-soundcraft-bridge
'''

# Osc Soundcraft Bridge definition
osb_port = 56420
master_path = "/master"
mix_path = "/mix"
reverb_path = "/reverb"
chorus_path = "/chorus"
delay_path = "/delay"
room_path = "/room"
mute_path = "/mute"
bass_path = "/bass"
mid_path = "/mid"
treble_path = "/treble"


# Main volume
ui_master=SendOSC(osb_port, master_path, ui_cursor)

# Mono patches / stands for all XLR+1/4 sockets
# Stereo patches must target left channel, right channel will change in the same time
mix_mono = SendOSC(osb_port, mix_path,  ui_event, ui_cursor, "i")
mix_stereo = [
        SendOSC(osb_port, mix_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, mix_path, ui_right, ui_cursor, "i"),
    ]

reverb_mono = SendOSC(osb_port, reverb_path,  ui_event, ui_cursor, "i")
reverb_stereo = [
        SendOSC(osb_port, reverb_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, reverb_path, ui_right, ui_cursor, "i"),
    ]

chorus_mono = SendOSC(osb_port, chorus_path,  ui_event, ui_cursor, "i")
chorus_stereo = [
        SendOSC(osb_port, chorus_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, chorus_path, ui_right, ui_cursor, "i"),
    ]

delay_mono = SendOSC(osb_port, delay_path,  ui_event, ui_cursor, "i")
delay_stereo = [
        SendOSC(osb_port, delay_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, delay_path, ui_right, ui_cursor, "i"),
    ]

room_mono = SendOSC(osb_port, room_path,  ui_event, ui_cursor, "i")
room_stereo = [
        SendOSC(osb_port, room_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, room_path, ui_right, ui_cursor, "i"),
    ]


mute_mono = SendOSC(osb_port, mute_path, ui_event, ui_mute, "i")
mute_stereo = [
        SendOSC(osb_port, mute_path, ui_left,  ui_mute, "i"),    
        SendOSC(osb_port, mute_path, ui_right, ui_mute, "i"),
    ]

# Equalizer
bass_mono = SendOSC(osb_port, bass_path, ui_event, ui_cursor, "i")
bass_stereo = [
        SendOSC(osb_port, bass_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, bass_path, ui_right, ui_cursor, "i"),
    ]

mid_mono = SendOSC(osb_port, mid_path, ui_event, ui_cursor, "i")
mid_stereo = [
        SendOSC(osb_port, mid_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, mid_path, ui_right, ui_cursor, "i"),
    ]

treble_mono = SendOSC(osb_port, treble_path, ui_event, ui_cursor, "i")
treble_stereo = [
        SendOSC(osb_port, treble_path, ui_left,  ui_cursor, "i"),    
        SendOSC(osb_port, treble_path, ui_right, ui_cursor, "i"),
    ]


# Static stereo inputs
# Line patches
ui_line_mute=[
        SendOSC(osb_port, mute_path, 0, ui_mute, "l"),    
        SendOSC(osb_port, mute_path, 1, ui_mute, "l"),
    ]
    
ui_line_mix=[
        SendOSC(osb_port, mix_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, mix_path, 1, ui_cursor, "l"),
    ]

line_bass = [
        SendOSC(osb_port, bass_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, bass_path, 1, ui_cursor, "l"),
    ]
line_mid = [
        SendOSC(osb_port, mid_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, mid_path, 1, ui_cursor, "l"),
    ]
line_treble = [
        SendOSC(osb_port, treble_path, 0, ui_cursor, "l"),    
        SendOSC(osb_port, treble_path, 1, ui_cursor, "l"),
    ]

# Player patches
ui_player_mute=[
        SendOSC(osb_port, mute_path, 0, ui_mute, "p"),    
        SendOSC(osb_port, mute_path, 1, ui_mute, "p"),
    ]
    
ui_player_mix=[
        SendOSC(osb_port, mix_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, mix_path, 1, ui_cursor, "p"),
    ]

player_bass = [
        SendOSC(osb_port, bass_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, bass_path, 1, ui_cursor, "p"),
    ]
player_mid = [
        SendOSC(osb_port, mid_path, 0, ui_cursor, "p"),    
        SendOSC(osb_port, mid_path, 1, ui_cursor, "p"),
    ]
player_treble = [
        SendOSC(osb_port, treble_path, 0, ui_cursor, "p"),
        SendOSC(osb_port, treble_path, 1, ui_cursor, "p"),
    ]

# -----------------------------------------------------
# Group patch by channel
ui_standard_fx = ChannelSplit({
            1:mix_mono,
            2:reverb_mono,
            3:delay_mono,
            4:chorus_mono,
        })

ui_standard_stereo_fx = ChannelSplit({
            1:mix_stereo,
            2:reverb_stereo,
            3:delay_stereo,
            4:chorus_stereo,
        })     

# 
ui_standard_stereo_eq = ChannelSplit({
            1:mix_stereo,
            2:bass_stereo,
            3:mid_stereo,
            4:treble_stereo,
        })

ui_line_mix_eq = ChannelSplit({
            1:ui_line_mix,
            2:line_bass,
            3:line_mid,
            4:line_treble,
        })

ui_player_mix_eq = ChannelSplit({
            1:ui_player_mix,
            2:player_bass,
            3:player_mid,
            4:player_treble,
        })