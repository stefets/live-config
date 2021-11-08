# Controlleur 1 : changement de scene
nav_controller_channel=configuration["nav_controller_channel"]
nav_controller = (
    CtrlFilter(20, 21, 22) >>
    CtrlSplit({
        20: Call(NavigateToScene),
        21: Discard(),
        22: Discard(),
    })
)

# MP3 Controller : Contexte d'utilisation d'un clavier pour controller le plugins Mp3Player
# Converti le volume ainsi que la modulation en pourcentage
mp3_config=configuration["mp3player"]
mp3_controller=mp3_config["controller"]

mp3_controller_channel=mp3_controller["channel"]
mp3_controller = (
	(CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
	(Filter(NOTEON) >> Transpose(mp3_controller["transpose"]))
    ) >> Call(Mp3Player(mp3_config))


# Collection de controllers
controllers = ChannelFilter(mp3_controller_channel,nav_controller_channel)
_control = (
	controllers >>
	ChannelSplit({
		mp3_controller_channel: mp3_controller,
		nav_controller_channel: nav_controller,
	})
)

