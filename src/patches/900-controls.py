#
# Patches for the run().control patch
#

# Generic
generic_controller = (
    CtrlFilter(16, 1, 2, 4, 7, 20, 69, 100, 101, 102, 103) >>
    CtrlSplit({
          1: HD500_Expr1,
          2: HD500_Expr2,
          4: GT10B_Tuner,
          7: GT10B_Volume,
         20: Call(NavigateToScene),
         69: HD500_Tuner,
        100: Ctrl(sd90_port_a, 1, 7, EVENT_VALUE),
        101: Program(sd90_port_a, 1, EVENT_VALUE),
        102: Ctrl(sd90_port_b, 1, 7, EVENT_VALUE),
        103: Program(sd90_port_b, 1, EVENT_VALUE),
    })
)

# 
mp3_jump    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
mp3_volume  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
mp3_trigger = Filter(NOTEON) >> Transpose(-36)
mp3_transport = [mp3_jump, mp3_volume, mp3_trigger]

mpk_mp3_controller = mp3_transport >> Call(Mp3Player(key_config, "SD90"))
pk5_mp3_controller = mp3_transport >> Call(Mp3Player(key_config, "SD90"))

# Spotify
spotify_controller = [
  Filter(NOTEON) >> mp3_trigger,
  CtrlFilter(7) >> CtrlValueFilter(0, 101), 
  CtrlFilter(1,44),
] >> Call(SpotifyPlayer(spotify_config))


# SoundCraft UI
soundcraft_controller=[
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

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_controller,
    mpk_midi : ChannelSplit({
	    4 : pk5_mp3_controller,
	}),
    mpk_port_a : ChannelSplit({
	     8 : mpk_mp3_controller,
	     9 : generic_controller,
        11 : p_hue,
        12 : spotify_controller,
	}),
    mpk_port_b : ChannelSplit({
	     4 : pk5_mp3_controller,
	}),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
    q49_midi    : Pass(),
})
