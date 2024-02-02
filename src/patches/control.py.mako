
#
# Patches for the run().control patch
#

# Transport filter Filter for mp3 and spotify
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

key_mp3_control = transport_filter >> Call(Mp3Player("${audio_device}"))
pk5_mp3_control = transport_filter >> Call(Mp3Player("${audio_device}"))
mpk_vlc_control = Filter(NOTEON) >> VLC

# Spotify
spotify_control = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())

mpk_soundcraft_control=Filter(CTRL|NOTE) >> [
        Filter(CTRL) >> Pass(),
        Filter(NOTE) >> NoteOn(EVENT_NOTE, 127) >> Port(midimix_midi),
    ] >> soundcraft_control

pk5_soundcraft_control=Filter(NOTEON) >> KeyFilter(72) >> NoteOn(9, 127) >> Port(midimix_midi) >> soundcraft_control

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : pk5_mp3_control,
        #3 : pk5_soundcraft_control,
    }),
    mpk_port_a : ChannelSplit({
         1 : mpk_soundcraft_control,
         8 : key_mp3_control,
        11 : (Channel(16) >> CtrlMap(11, 7) >> GT10B_Volume),  # Akai MPK249 Expression pedal
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
         1 : Pass(),
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})
