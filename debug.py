    2: SceneGroup("DebugScene", [    
			#Scene("Modulation2Volume", 
			#	[
			#		[ChannelFilter(1) >> tss_keyboard_main // ChannelFilter(1) >> Filter(CTRL) >> CtrlFilter(1) >> CtrlMap(1,7) >> Channel(2)] ,
			#		ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main,
			#	]),
    	#Scene("Analog Kid", Channel(1) >> analogkid),
    	Scene("Pad D4", Process(RemoveDuplicates()) >> d4),
    	#Scene("Pad D4", d4),
       ]),   
	   
	   
#~CtrlFilter(1) >> 
