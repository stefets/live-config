
'''
    The Soundcraft UI 16 patches for mididings
    Those patches use the OSC protocol to communicate with the Osc Soundcraft Bridge daemon
    The CC number correspond to the SoundCraft input channel
    The CC value correspond to the SoundCraft cursor value 
    https://github.com/stefets/osc-soundcraft-bridge
'''

#
# Helper functions used by the Soundcraft UI patches
#

# 0-127 to 0-1
ratio=0.7874015748 / 100

def cursor_value_converter(ev):
    return ev.data2 * ratio

def ui_knob(ev):
    return cursor_value_converter(ev)

def mute_value_converter(ev):
    return 1 if ev.data2==127 else 0

''' Return the controller value for SendOsc '''
def event_value_converter(ev, offset=0):
    return ev.ctrl+offset if ev.type == CTRL else -1

''' Wrapper over ui_event '''
def ui_left(ev):
    return event_value_converter(ev)

''' Wrapper over ui_event '''
def ui_right(ev):
    return event_value_converter(ev, 1)


# Osc Soundcraft Bridge definition
osb_port = 56420
master_path = "/master"
mix_path = "/mix"
reverb_path = "/reverb"
chorus_path = "/chorus"
delay_path = "/delay"
room_path = "/room"
mute_path = "/mute"
mute_reverb_path = "/reverb/mute"
mute_delay_path = "/delay/mute"
mute_chorus_path = "/chorus/mute"
mute_room_path = "/room/mute"
bass_path = "/bass"
mid_path = "/mid"
treble_path = "/treble"


# Main volume
ui_master=SendOSC(osb_port, master_path, cursor_value_converter)

# Mono patches / stands for all XLR+1/4 sockets
# Stereo patches must target left channel, right channel will change in the same time
mix_mono = SendOSC(osb_port, mix_path,  event_value_converter, cursor_value_converter, "i")
mix_stereo = [
        SendOSC(osb_port, mix_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, mix_path, ui_right, cursor_value_converter, "i"),
    ]

reverb_mono = SendOSC(osb_port, reverb_path,  event_value_converter, cursor_value_converter, "i")
reverb_stereo = [
        SendOSC(osb_port, reverb_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, reverb_path, ui_right, cursor_value_converter, "i"),
    ]

chorus_mono = SendOSC(osb_port, chorus_path,  event_value_converter, cursor_value_converter, "i")
chorus_stereo = [
        SendOSC(osb_port, chorus_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, chorus_path, ui_right, cursor_value_converter, "i"),
    ]

delay_mono = SendOSC(osb_port, delay_path,  event_value_converter, cursor_value_converter, "i")
delay_stereo = [
        SendOSC(osb_port, delay_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, delay_path, ui_right, cursor_value_converter, "i"),
    ]

room_mono = SendOSC(osb_port, room_path,  event_value_converter, cursor_value_converter, "i")
room_stereo = [
        SendOSC(osb_port, room_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, room_path, ui_right, cursor_value_converter, "i"),
    ]


mute_mono = SendOSC(osb_port, mute_path, event_value_converter, mute_value_converter, "i")
mute_stereo = [
        SendOSC(osb_port, mute_path, ui_left,  mute_value_converter, "i"),    
        SendOSC(osb_port, mute_path, ui_right, mute_value_converter, "i"),
    ]

mute_reverb_mono = SendOSC(osb_port, mute_reverb_path, event_value_converter, mute_value_converter, "i")
mute_delay_mono = SendOSC(osb_port, mute_delay_path, event_value_converter, mute_value_converter, "i")
mute_chorus_mono = SendOSC(osb_port, mute_chorus_path, event_value_converter, mute_value_converter, "i")
mute_room_mono = SendOSC(osb_port, mute_room_path, event_value_converter, mute_value_converter, "i")

mute_delay_stereo = [
    SendOSC(osb_port, mute_delay_path, ui_left, mute_value_converter, "i"),
    SendOSC(osb_port, mute_delay_path, ui_right, mute_value_converter, "i"),
]

# Equalizer
bass_mono = SendOSC(osb_port, bass_path, event_value_converter, cursor_value_converter, "i")
bass_stereo = [
        SendOSC(osb_port, bass_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, bass_path, ui_right, cursor_value_converter, "i"),
    ]

mid_mono = SendOSC(osb_port, mid_path, event_value_converter, cursor_value_converter, "i")
mid_stereo = [
        SendOSC(osb_port, mid_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, mid_path, ui_right, cursor_value_converter, "i"),
    ]

treble_mono = SendOSC(osb_port, treble_path, event_value_converter, cursor_value_converter, "i")
treble_stereo = [
        SendOSC(osb_port, treble_path, ui_left,  cursor_value_converter, "i"),    
        SendOSC(osb_port, treble_path, ui_right, cursor_value_converter, "i"),
    ]


# Static stereo inputs
# Line patches
ui_line_mute=[
        SendOSC(osb_port, mute_path, 0, mute_value_converter, "l"),    
        SendOSC(osb_port, mute_path, 1, mute_value_converter, "l"),
    ]
    
ui_line_mix=[
        SendOSC(osb_port, mix_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, mix_path, 1, cursor_value_converter, "l"),
    ]

line_bass = [
        SendOSC(osb_port, bass_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, bass_path, 1, cursor_value_converter, "l"),
    ]
line_mid = [
        SendOSC(osb_port, mid_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, mid_path, 1, cursor_value_converter, "l"),
    ]
line_treble = [
        SendOSC(osb_port, treble_path, 0, cursor_value_converter, "l"),    
        SendOSC(osb_port, treble_path, 1, cursor_value_converter, "l"),
    ]

# Player patches
ui_player_mute=[
        SendOSC(osb_port, mute_path, 0, mute_value_converter, "p"),    
        SendOSC(osb_port, mute_path, 1, mute_value_converter, "p"),
    ]
    
ui_player_mix=[
        SendOSC(osb_port, mix_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, mix_path, 1, cursor_value_converter, "p"),
    ]

player_bass = [
        SendOSC(osb_port, bass_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, bass_path, 1, cursor_value_converter, "p"),
    ]
player_mid = [
        SendOSC(osb_port, mid_path, 0, cursor_value_converter, "p"),    
        SendOSC(osb_port, mid_path, 1, cursor_value_converter, "p"),
    ]
player_treble = [
        SendOSC(osb_port, treble_path, 0, cursor_value_converter, "p"),
        SendOSC(osb_port, treble_path, 1, cursor_value_converter, "p"),
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

# Mididings SoundCraft UI control patch
soundcraft_control=[Filter(NOTEON) >> 
                    
        Process(MidiMix()) >> [
        
        KeyFilter(1) >> Ctrl(0, EVENT_VALUE) >> mute_mono,
        KeyFilter(2) >> Pass(),
        KeyFilter(3) >> Pass(),

        KeyFilter(4) >> Ctrl(1, EVENT_VALUE) >> mute_mono,
        KeyFilter(5) >> Pass(),
        KeyFilter(6) >> Pass(),


        KeyFilter(7)  >> Ctrl(2, EVENT_VALUE) >> mute_stereo,
        KeyFilter(9)  >> Ctrl(2, EVENT_VALUE) >> mute_delay_stereo,
        KeyFilter(10) >> Ctrl(4, EVENT_VALUE) >> mute_stereo,
        KeyFilter(13) >> Ctrl(6, EVENT_VALUE) >> mute_stereo,

        KeyFilter(16) >> ui_line_mute,
        KeyFilter(19) >> ui_player_mute,
        
        KeyFilter(22) >> Discard(),

        Process(MidiMixLed())

    ],
    Filter(CTRL) >> [
        CtrlFilter(0,1) >> ui_standard_fx,
       
        CtrlFilter(2,3,4) >> CtrlSplit({
            2 : Pass(),
            3 : Ctrl(4, EVENT_VALUE),
            4 : Ctrl(6, EVENT_VALUE),
        }) >> ui_standard_stereo_eq,

        CtrlFilter(5) >> ui_line_mix_eq,
        CtrlFilter(6) >> ui_player_mix_eq,
        CtrlFilter(7) >> Discard(),
        CtrlFilter(100) >> ui_master,
    ],
]