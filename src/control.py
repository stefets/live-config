# Controlleur 1 : changement de scene

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
# Limite le Control #1 et #7 en %
key_controller=key_config["controller"]
key_transpose=Transpose(key_controller["transpose"])

key_controller_channel=key_controller["channel"]
key_controller = [
    [
        CtrlFilter(7) >> CtrlValueFilter(0, 101), 
        CtrlFilter(1) >> CtrlValueFilter(0, 121), 
        Filter(NOTEON) >> key_transpose
    ] >> Call(Mp3Player(key_config)),
    Filter(NOTEON) >> key_transpose >> KeyFilter(notes=[0]) >> HueOff,
    Filter(NOTEON) >> key_transpose >> KeyFilter(notes=[48]) >> HueNormal,
    CtrlFilter(91) >> CtrlMap(91,1) >> Ctrl(hd500_port, hd500_channel, EVENT_CTRL, EVENT_VALUE)
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

