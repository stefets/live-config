#
# Patches for the run().control patch
#

# AKAI sliders, knobs and switches
nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(1, 2, 3, 7, 4, 20, 21, 22, 23, 24, 25, 26, 69, 100, 101, 102, 103) >>
    CtrlSplit({
        1: Expr1,
        2: Expr2,
        4: GT10B_Tuner,
        7: GT10B_Volume,
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
        23: Discard(),
        24: Discard(),
        25: Discard(),
        26: Discard(),
        69: Tuner,
        100: Ctrl(sd90_port_a, 1, 7, EVENT_VALUE),
        101: Program(sd90_port_a, 1, EVENT_VALUE),
        102: Ctrl(sd90_port_b, 1, 7, EVENT_VALUE),
        103: Program(sd90_port_b, 1, EVENT_VALUE),
    })
)

# Each Call(Mp3Player) create a mpg123 process
mp3_volume=CtrlFilter(7) >> CtrlValueFilter(0, 101)
mp3_jump=CtrlFilter(1) >> CtrlValueFilter(0, 121)

key_controller_config=key_config["controller"]
key_transpose=Transpose(key_controller_config["transpose"])

key_controller_channel=key_controller_config["channel"]
key_controller = [
  Filter(NOTEON) >> key_transpose, 
  mp3_volume, 
  mp3_jump, 
] >> Call(Mp3Player(key_config, "SD90"))

pk5_controller_channel=4
#pk5_controller=[PortFilter(mpk_midi), PortFilter('MPK-MIDI-2')] >> ChannelFilter(4) >> [
pk5_controller=[PortFilter(mpk_midi)] >> ChannelFilter(4) >> [
    Filter(NOTEON) >> key_transpose,
    mp3_volume, 
    mp3_jump,
] >> Call(Mp3Player(key_config, "SD90"))

hue_controller_channel = 11
hue_controller = p_hue

spotify_channel = 12
spotify_controller = [
    Filter(NOTEON) >> key_transpose,
    CtrlFilter(7) >> CtrlValueFilter(0, 101), 
    CtrlFilter(1,44),
    ] >> Call(SpotifyPlayer(spotify_config))


# MidiMix controller patch for SoundCraft UI

midimix_controller=PortFilter(midimix_midi) >> [
    Filter(NOTEON) >> Process(MidiMix()) >> [
        KeyFilter(1) >> Ctrl(0, EVENT_VALUE) >> mute_mono,
        KeyFilter(4) >> Ctrl(1, EVENT_VALUE) >> mute_mono,

        KeyFilter(7)  >> Ctrl(2, EVENT_VALUE) >> mute_stereo,
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

# Collection of controllers
controllers = ChannelFilter(key_controller_channel,nav_controller_channel, hue_controller_channel, spotify_channel)
control_patch = [
	controllers >>
	ChannelSplit({
	    key_controller_channel: key_controller,
	    nav_controller_channel: nav_controller,
        hue_controller_channel: hue_controller,
        spotify_channel : spotify_controller,
	}),
    midimix_controller,
    pk5_controller
]
