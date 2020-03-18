#-----------------------------------------------------------------------------------------------------------
# CONTROL SECTION
#-----------------------------------------------------------------------------------------------------------
q49_channel=1
pk5_channel=2
fcb_channel=9
pod_channel=9
gt10b_channel=16


# This control have the same behavior than the NavigateToScene python function above
# EXCEPT that there is NO wrap parameter for SceneSwitch
# The NavigateToScene CAN wrap through Scenes
#_control=(ChannelFilter(9) >> Filter(CTRL) >>
#	(
#		(CtrlFilter(20) >> CtrlValueFilter(1) >> SceneSwitch(offset=-1)) //
#		(CtrlFilter(20) >> CtrlValueFilter(2) >> SceneSwitch(offset=1))  //
#		(CtrlFilter(20) >> CtrlValueFilter(3) >> SubSceneSwitch(offset=1, wrap=True))
#	))


# Reset all
reset=(
	System(AllAudioOff) // Pass() //
	ResetSD90 // Pass()
)


# FCB1010 UNO as controller
#fcb1010=(ChannelFilter(9) >> Filter(CTRL) >> 
#	(
#		(CtrlFilter(20) >> Process(NavigateToScene)) // 
#		(CtrlFilter(22) >> reset)
#	))

# FCB1010 UNO as controller (same as above different syntaxes)
fcb1010=(Filter(CTRL) >> CtrlSplit({
    20: Process(NavigateToScene),
    22: reset,
}))

# KEYBOARD CONTROLLER - Alesis Q49 
# Transpose -36 to work from note 0 49
keyboard=(Filter(NOTEON|CTRL) >> Transpose(-36) >> Process(MPG123()))

# PK5 as Controller - WIP
_pk5_controller = Pass()

# Shortcut (Play switch)
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)
#-----------------------------------------------------------------------------------------------------------

# TODO (*** not sure until real need ***)
# Multiple controllers , different logic for each of them WIP
#main_controller=ChannelSplit({
    #1: _keyboard_controller,
    #9: _fcb1010_controller,
    #2:_pk5_controller
#})
