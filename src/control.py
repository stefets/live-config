# Wipe all
# TODO - Move _wipe ailleur
_wipe = (
    System(AllAudioOff) // Pass() //
    ResetSD90 // Pass()
)

# FCB1010 & UNO Chip
_fcb1010 = (
    CtrlFilter(20,22) >>
    CtrlSplit({
        20: Call(NavigateToScene),
        22: _wipe,
    })
)

# Control MPG123 process
# See MPG123 class to understand how it works
_mpg123 = (
	(CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
	(Filter(NOTEON) >> Transpose(-36))
) >> Call(MPG123())

_control = (
	ChannelFilter(8,9) >>
	ChannelSplit({
		8: _mpg123,
		9: _fcb1010,
	})
)
