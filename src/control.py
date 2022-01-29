# Controlleur 1

nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(1, 2, 7, 4, 20, 21, 22, 23, 24, 25, 26, 69) >>
    CtrlSplit({
        1: Expr1,
        2: Expr2,
        69: Ctrl('SD90-MIDI-OUT-1', nav_controller_channel, EVENT_CTRL, EVENT_VALUE),
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
        7: GT10B_Volume,
        4: GT10B_Tuner,
        26: Program('SD90-PART-A', 1, EVENT_VALUE),
    })
)

# Keyboard Controller : Contexte d'utilisation d'un clavier pour controller le plugins Mp3Player ou le Philips Hue
# Le CC#7 est en % et le CC#1 en secondes pour Mp3Player

key_controller=key_config["controller"]
key_transpose=Transpose(key_controller["transpose"])

key_controller_channel=key_controller["channel"]
key_controller = [
    [
        Filter(NOTEON) >> key_transpose, 
        CtrlFilter(7) >> CtrlValueFilter(0, 101), 
        CtrlFilter(1) >> CtrlValueFilter(0, 121), 
    ] >> Call(Mp3Player(key_config)),
    Filter(NOTEON) >> key_transpose >> [KeyFilter(notes=[0]) >> HueOff, KeyFilter(notes=[48]) >> HueNormal],
]

hue_controller_channel = 11
hue_controller = akai_pad

spotify_channel = 12
spotify_patch = [
    Filter(NOTEON) >> key_transpose,
    CtrlFilter(7) >> CtrlValueFilter(0, 101), 
    ] >> Call(SpotifyPlayer(spotify_config))

# Collection de controllers par channel
controllers = ChannelFilter(key_controller_channel,nav_controller_channel, hue_controller_channel, spotify_channel)
_control = (
	controllers >>
	ChannelSplit({
		key_controller_channel: key_controller,
		nav_controller_channel: nav_controller,
        hue_controller_channel: hue_controller,
        spotify_channel : spotify_patch
	})
)

