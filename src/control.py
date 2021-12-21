# Controlleur 1 : changement de scene

#from devices.hd500 import TunerOn


nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(1, 20, 21, 22) >>
    CtrlSplit({
         1: CtrlMap(1,7) >> Ctrl(GT10BPort, GT10BChannel, EVENT_CTRL, EVENT_VALUE),
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
    })
)

# Keyboard Controller : Contexte d'utilisation d'un clavier pour controller le plugins Mp3Player ou le Philips Hue
# Le CC#7 est en % et le CC#1 en secondes pour Mp3Player

key_controller=key_config["controller"]
key_transpose=Transpose(key_controller["transpose"])

hd500_tuner=Filter(NOTEON) >> key_transpose >> [    
        KeyFilter(notes=[1]) >> TunerOn,
        KeyFilter(notes=[3]) >> TunerOff,
    ]

key_controller_channel=key_controller["channel"]
key_controller = [
    [
        Filter(NOTEON) >> key_transpose, 
        CtrlFilter(7) >> CtrlValueFilter(0, 101), 
        CtrlFilter(1) >> CtrlValueFilter(0, 121), 
    ] >> Call(Mp3Player(key_config)),
    Filter(NOTEON) >> key_transpose >> [KeyFilter(notes=[0]) >> HueOff, KeyFilter(notes=[48]) >> HueNormal],
    CtrlFilter(91) >> Expr1
]


# Collection de controllers
controllers = ChannelFilter(key_controller_channel,nav_controller_channel)
_control = (
	controllers >>
	ChannelSplit({
		key_controller_channel: key_controller,
		nav_controller_channel: nav_controller,
	})
)

