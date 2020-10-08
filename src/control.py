# -----------------------------------------------------------------------------------------------------------
# CONTROL SECTION
# -----------------------------------------------------------------------------------------------------------

# This control have the same behavior than the NavigateToScene python function above
# EXCEPT that there is NO wrap parameter for SceneSwitch
# The NavigateToScene CAN wrap through Scenes
# _ control=(ChannelFilter(9) >> Filter(CTRL) >>
#	(
#		(CtrlFilter(20) >> CtrlValueFilter(1) >> SceneSwitch(offset=-1)) //
#		(CtrlFilter(20) >> CtrlValueFilter(2) >> SceneSwitch(offset=1))  //
#		(CtrlFilter(20) >> CtrlValueFilter(3) >> SubSceneSwitch(offset=1, wrap=True))
#	))


# Reset all
reset = (
        System(AllAudioOff) // Pass() //
        ResetSD90 // Pass()
)

# FCB1010 UNO as controller (same as above different syntaxes)
fcb1010 = (Filter(CTRL) >> CtrlSplit({
    20: Call(NavigateToScene),
    22: reset,
}))

# MIDI KEYBOARD CONTROLLER TO CONTROL MPG123 
keyboard = (
                   (CtrlFilter(1, 7) >> CtrlValueFilter(0, 101)) //
                   (Filter(NOTEON) >> Transpose(-36))
           ) >> Call(MPG123())

# Shortcut (Play switch)
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)
# -----------------------------------------------------------------------------------------------------------
