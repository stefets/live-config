
#
# Patches for the run().control patch
#

# TO REWORK
wip_controller = (Filter(CTRL) >>
    CtrlSplit({
         20: Call(NavigateToScene),
        100: Ctrl(sd90_port_a, 1, 7, EVENT_VALUE),
        101: Program(sd90_port_a, 1, EVENT_VALUE),
        102: Ctrl(sd90_port_b, 1, 7, EVENT_VALUE),
        103: Program(sd90_port_b, 1, EVENT_VALUE),
    })
)

gt10b_control = (Filter(CTRL) >>
    CtrlSplit({
          4: GT10B_Tuner,
          7: GT10B_Volume,
    }))

hd500_control = (Filter(CTRL) >>
    CtrlSplit({
          1: HD500_Expr1,
          2: HD500_Expr2,
         69: HD500_Tuner,
    }))

# Transport filter Filter for mp3 and spotify
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

key_mp3_control = transport_filter >> Call(Mp3Player("${audio_device}"))
pk5_mp3_control = transport_filter >> Call(Mp3Player("${audio_device}"))
mpk_vlc_control = Filter(NOTEON) >> Call(VlcPlayer())

# Spotify
spotify_control = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())


# SoundCraft UI
soundcraft_control=[
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

# FlaskDings API control patch
flaskdings_uri = os.environ["FLASKDINGS"]
flaskdings_control = trigger_filter >> [
    KeyFilter(0) >> Call(HttpGet(flaskdings_uri + "prev_scene")),
    KeyFilter(2) >> Call(HttpGet(flaskdings_uri + "next_scene")),
]

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : pk5_mp3_control,
    }),
    mpk_port_a : ChannelSplit({
         8 : key_mp3_control,
        # Akai MPK249 Expression pedal
        11 : (Channel(16) >> CtrlMap(11, 7) >> GT10B_Volume),
        12 : mpk_vlc_control,
        13 : p_hue,
        14 : spotify_control,
        15 : hd500_control,
        16 : gt10b_control
    }),
    mpk_port_b : ChannelSplit({
         4 : pk5_mp3_control,
        11 : HD500_Expr1,             # Akai MPK249 Expression pedal
    }),
    q49_midi : ChannelSplit({
         1 : flaskdings_control,
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})
