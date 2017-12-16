    2: SceneGroup("DebugScene", [    
		#Scene("Modulation2Volume", 
		#	[
		#		[ChannelFilter(1) >> tss_keyboard_main // ChannelFilter(1) >> Filter(CTRL) >> CtrlFilter(1) >> CtrlMap(1,7) >> Channel(2)] ,
		#		ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main,
		#	]),
    	#Scene("Analog Kid", analogkid_main),
    	#Scene("Pad D4", Process(RemoveDuplicates()) >> d4),
    	#Scene("Pad D4", centurion_patch),
    	#Scene("Pad D4", Process(RemoveDuplicates()) >> closer_patch_d4),
        #Scene("Pad D4",  Process(RemoveDuplicates()) >> yyz),
    	Scene("TimeStandSteel.D4",  Process(RemoveDuplicates(0.01)) >> 
			[
				(
				tss_d4_melo_tom_A // 
				tss_d4_castanet // 
				tss_d4_melo_tom_B // 
				tss_d4_808_tom
				)
	 		]),
    	#Scene("Pad D4",  Process(RemoveDuplicates(0.01)) >> tss_d4_808_tom_patch),
    	#Scene("Pad D4",  Process(RemoveDuplicates(0.01)) >> tss_d4_808_tom_patch),
    	#Scene("Pad D4",  Process(RemoveDuplicates(0.01)) >> tss_d4_melo_tom_patch),
    	#Scene("Pad D4",  Process(RemoveDuplicates(0.5)) >> closer_patch_celesta_d4),
		#Scene("2112", Process(RemoveDuplicates()) >> d4play >> System("mpg123 -q /mnt/flash/live/2112.mp3")),
       ]),   
	   
	   
#~CtrlFilter(1) >> 
