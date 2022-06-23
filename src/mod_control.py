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
hue_patch = p_hue

spotify_channel = 12
spotify_patch = [
    Filter(NOTEON) >> key_transpose,
    CtrlFilter(7) >> CtrlValueFilter(0, 101), 
    CtrlFilter(1,44),
    ] >> Call(SpotifyPlayer(spotify_config))

# My SoundCraft UI16 series controller logic
osb_port = 56420
scc=configuration["soundcraft_controller_channel"]
sc_controller= [
    CtrlFilter(1,2,3,4,5,6,7,8,9,10,11,12) >> SendOSC(osb_port,  '/mix', sc_input, data2_to_zero_one_range),
    #CtrlFilter(13,14) >> SendOSC(osb_port,  '/lmix', sc_base, data2_to_zero_one_range),
    #CtrlFilter(15,16) >> SendOSC(osb_port,  '/pmix', sc_base, data2_to_zero_one_range),
    CtrlFilter(21,22,23,24,25,26,27,28,29,30,31,32) >> SendOSC(osb_port,  '/mute', sc_mute, data2_to_mute),
    #CtrlFilter(33,34) >> SendOSC(osb_port,  '/lmute', sc_mute, data2_to_mute),
    CtrlFilter(35,36) >> SendOSC(osb_port,  '/pmute', sc_mute, data2_to_mute),
]

# Collection de controllers par channel
controllers = ChannelFilter(key_controller_channel,nav_controller_channel, hue_controller_channel, spotify_channel, scc)
_control = (
	controllers >>
	ChannelSplit({
		key_controller_channel: key_controller,
		nav_controller_channel: nav_controller,
        hue_controller_channel: hue_patch,
        spotify_channel : spotify_patch,
        scc : sc_controller
	})
)

