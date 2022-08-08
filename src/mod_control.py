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

    CtrlFilter(1,2,9,10,11,12) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range),
    
    CtrlFilter(3,4) >> 
        [
          Ctrl(3,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range),
          Ctrl(4,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range)
        ],
    
    CtrlFilter(5,6) >> 
        [
          Ctrl(5,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range),
          Ctrl(6,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range)
        ],
    
    CtrlFilter(7,8) >> 
        [
          Ctrl(7,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range),
          Ctrl(8,EVENT_VALUE) >> SendOSC(osb_port, '/mix', sc_input, data2_to_zero_one_range)
        ],
    
    CtrlFilter(21,22,29,30,31,32) >> SendOSC(osb_port,  '/mute', sc_mute, data2_to_mute),

        CtrlFilter(23,24) >> 
        [
          Ctrl(23,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range),
          Ctrl(24,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range)
        ],
    
    CtrlFilter(25,26) >> 
        [
          Ctrl(25,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range),
          Ctrl(26,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range)
        ],
    
    CtrlFilter(27,28) >> 
        [
          Ctrl(27,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range),
          Ctrl(28,EVENT_VALUE) >> SendOSC(osb_port, '/mute', sc_mute, data2_to_zero_one_range)
        ],


    # Line IN    
    CtrlFilter(13,14) >> 
        [
          Ctrl(13,EVENT_VALUE) >> SendOSC(osb_port, '/lmix', 0, data2_to_zero_one_range),
          Ctrl(14,EVENT_VALUE) >> SendOSC(osb_port, '/lmix', 1, data2_to_zero_one_range)
        ],
    CtrlFilter(33,34) >> 
        [
          Ctrl(33,EVENT_VALUE) >> SendOSC(osb_port, '/lmute', 0, data2_to_zero_one_range),
          Ctrl(34,EVENT_VALUE) >> SendOSC(osb_port, '/lmute', 1, data2_to_zero_one_range)
        ],

    # Player IN
    CtrlFilter(15,16) >> 
        [
          Ctrl(15,EVENT_VALUE) >> SendOSC(osb_port, '/pmix', 0, data2_to_zero_one_range),
          Ctrl(16,EVENT_VALUE) >> SendOSC(osb_port, '/pmix', 1, data2_to_zero_one_range)
        ],
    CtrlFilter(35,36) >> 
        [
          Ctrl(35,EVENT_VALUE) >> SendOSC(osb_port, '/pmute', 0, data2_to_zero_one_range),
          Ctrl(36,EVENT_VALUE) >> SendOSC(osb_port, '/pmute', 1, data2_to_zero_one_range)
        ],

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

