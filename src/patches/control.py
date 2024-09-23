
#
# Patches for the run().control patch
#

# Transport filter Filter for MPG123 and Spotipy and VLC
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

key_mp3_control = transport_filter >> MPG123_SD90_A
pk5_mp3_control = transport_filter >> MPG123_SD90_B
q49_mp3_control = transport_filter >> MPG123_U192k
mpk_vlc_control = trigger_filter >> VLC_BASE
q49_vlc_control = trigger_filter >> VLC_BASE

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

# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : pk5_mp3_control,
       15 : Pass(),     # FCB1010 to MPK249-Midi IN and MPK OUT to POD HD500 IN
    }),
    mpk_port_a : ChannelSplit({
         1 : mpk_soundcraft_control,
         8 : key_mp3_control,
        11 : (Channel(16) >> CtrlMap(11, 7) >> GT10B_Volume),  # Akai MPK249 Expression pedal
        12 : mpk_vlc_control,
        13 : p_hue,
        #14 : spotify_control,
        15 : hd500_control,
        16 : gt10b_control
    }),
    mpk_port_b : ChannelSplit({
         4 : pk5_mp3_control,
        11 : HD500_Expr1,             # Akai MPK249 Expression pedal
    }),
    q49_midi : ChannelSplit({
         1 : q49_mp3_control,
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})
