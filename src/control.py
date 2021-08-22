# Wipe all
# TODO - Move _wipe ailleur
_wipe = (
    System(AllAudioOff) // Pass() //
    ResetSD90 // Pass()
)

# FCB1010 with UNO Chip
footswitch_controller = (
    CtrlFilter(20, 21, 22) >>
    CtrlSplit({
        20: Call(NavigateToScene),
        21: Discard(),
        22: _wipe,
    })
)

# Control MPG123 process via a midi keyboard
keyboard_controller = (
	(CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
	(Filter(NOTEON) >> Transpose(-36))
) >> Call(Mp3Player(mp3player_config, mp3player_config["player"], mp3player_config["audiodevice"], False))

# Controllers collection
_control = (
	ChannelFilter(8,9) >>
	ChannelSplit({
		8: keyboard_controller,
		9: footswitch_controller,
	})
)
