
#
# Patches for the run().control patch
#

# Transport filter
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

mpv_controller_1 = transport_filter >> AUDIO_DEVICE_SD90_A
mpv_controller_2 = transport_filter >> AUDIO_DEVICE_SD90_B
mpv_controller_3= transport_filter >> AUDIO_DEVICE_U192k
vlc_controller_1 = trigger_filter >> VLC_BASE

sd90_controller = Port(sd90_port_a) >> [ 
    CtrlFilter(0) >> WaveLevel,
    CtrlFilter(1) >> InstLevel,
    CtrlFilter(2) >> MicGtLevel,
    CtrlFilter(3) >> DigiLevel,
    CtrlFilter(4) >> MasterLevel,
    CtrlFilter(5) >> RecLevel,
 ]

# Spotify
spotify_controller = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())

soundcraft_controller=Filter(CTRL|NOTE) >> [
        Filter(CTRL) >> Pass(),
        Filter(NOTE) >> NoteOn(EVENT_NOTE, 127) >> Port(midimix_midi),
    ] >> soundcraft_control


# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : mpv_controller_2,
    }),
    mpk_port_a : ChannelSplit({
         1 : CakewalkController,
         8 : mpv_controller_1,
         4 : mpv_controller_2,
        12 : vlc_controller_1,
        13 : p_hue,
        14: sd90_controller,
    }),
    mpk_port_b : ChannelSplit({
         1 : Program(sd90_port_a, EVENT_CHANNEL, EVENT_VALUE),
         2 : Channel(1) >> Port(mixxx_midi_0),
         8 : mpv_controller_1,
         4 : mpv_controller_2,
    }),

    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
    
    # Direct routing of the Numark to the virtual port used by Mixxx
    numark_midi_pmv3_0 : Port(mixxx_midi_0),
    numark_midi_pmv2_0 : Port(mixxx_midi_0),
    um2_midi_1 : ChannelSplit({
        15 : gt1k,
    }),

})
