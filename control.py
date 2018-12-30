#-----------------------------------------------------------------------------------------------------------
# 											CONTROL SECTION
#-----------------------------------------------------------------------------------------------------------

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
clean=(
		System(AllAudioOff) // 
		Pass() // 
		SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7') //
		Pass()
)

# FCB1010 UNO as controller
fcb1010=(ChannelFilter(9) >> Filter(CTRL) >> 
	(
		(CtrlFilter(20) >> Process(NavigateToScene)) // 
		(CtrlFilter(22) >> clean)
	))

# KEYBOARD CONTROLLER - WIP
keyboard = Pass()

# TLMEP
# TODO Keyboard controller a la maniere de Tout le monde en parle

# Shortcut (Play switch)
play = ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(21)
d4play = ChannelFilter(3) >> KeyFilter(45) >> Filter(NOTEON) >> NoteOff(45)
#-----------------------------------------------------------------------------------------------------------
