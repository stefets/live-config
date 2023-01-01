# Controlleur 1

# AKAI sliders, knobs and switches
nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(1, 2, 3, 7, 4, 20, 21, 22, 23, 24, 25, 26, 69) >>
    CtrlSplit({
        1: Expr1,
        2: Expr2,
        4: GT10B_Tuner,
        7: GT10B_Volume,
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
        26: Program('SD90-PART-A', 1, EVENT_VALUE),
        69: Tuner,
    })
)

# Keyboard Controller : Contexte d'utilisation d'un clavier pour controller le plugins Mp3Player ou le Philips Hue
# Le CC#7 est en % et le CC#1 en secondes pour Mp3Player

key_controller_config=key_config["controller"]
key_transpose=Transpose(key_controller_config["transpose"])

key_controller_channel=key_controller_config["channel"]
key_controller = [
  Filter(NOTEON) >> key_transpose, 
  CtrlFilter(7) >> CtrlValueFilter(0, 101), 
  CtrlFilter(1) >> CtrlValueFilter(0, 121), 
] >> Call(Mp3Player(key_config))

hue_controller_channel = 11
hue_controller = p_hue

spotify_channel = 12
spotify_controller = [
    Filter(NOTEON) >> key_transpose,
    CtrlFilter(7) >> CtrlValueFilter(0, 101), 
    CtrlFilter(1,44),
    ] >> Call(SpotifyPlayer(spotify_config))


# MidiMix controller patch for SoundCraft UI
midimix_controller=PortFilter('MIDIMIX') >> [
    Filter(NOTEON) >> Process(MidiMix()) >> [
        KeyFilter(1) >> Ctrl(0, EVENT_VALUE) >> mutebase,
        KeyFilter(4) >> Ctrl(1, EVENT_VALUE) >> mutebase,

        KeyFilter(7)  >> Ctrl(2, EVENT_VALUE) >> mutebase_stereo,
        KeyFilter(10) >> Ctrl(4, EVENT_VALUE) >> mutebase_stereo,
        KeyFilter(13) >> Ctrl(6, EVENT_VALUE) >> mutebase_stereo,

        KeyFilter(16) >> ui_line_mute,
        KeyFilter(19) >> ui_player_mute,

        Process(MidiMixLed())
    ],
    Filter(CTRL) >> [
        CtrlFilter(19) >> Ctrl(0, EVENT_VALUE) >> mixbase,
        CtrlFilter(23) >> Ctrl(1, EVENT_VALUE) >> mixbase,

        CtrlFilter(27) >> Ctrl(2, EVENT_VALUE) >> mixbase_stereo,
        CtrlFilter(31) >> Ctrl(4, EVENT_VALUE) >> mixbase_stereo,
        CtrlFilter(49) >> Ctrl(6, EVENT_VALUE) >> mixbase_stereo,

        CtrlFilter(53) >> ui_line_mix,
        CtrlFilter(57) >> ui_player_mix,
        CtrlFilter(62) >> ui_master,
    ],
]


# Collection of controllers by context
controllers = ChannelFilter(key_controller_channel,nav_controller_channel, hue_controller_channel, spotify_channel)
_control = ([
	controllers >>
	ChannelSplit({
		key_controller_channel: key_controller,
		nav_controller_channel: nav_controller,
        hue_controller_channel: hue_controller,
        spotify_channel : spotify_controller,
	}),
    midimix_controller
])

