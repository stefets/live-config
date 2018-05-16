    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    3: Scene("FreeWill", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    4: Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, ChannelFilter(2) >> Transpose(-24) >> closer_base]),
    5: SceneGroup("The Trees", [
            Scene("Bridge",  play >> System(play_file("trees_full.mp3"))),
            Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    6: SceneGroup("Time Stand Still", [
			Scene("TSS-Intro", play >> System(play_file("tss.mp3"))),
			Scene("TSS-Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
	   ]),
    7: SceneGroup("2112", [
		    Scene("2112-MP3 via D4", Process(RemoveDuplicates()) >> d4play >> System(play_file("2112.mp3"))),
		    Scene("2112-MP3 via FCB1010", play >> System(play_file("2112.mp3"))),
            Scene("Explosion", explosion),
       ]),
    8: Scene("Analog Kid", Channel(1) >> analogkid_main),
    9: Scene("Hemispheres", play >> System(play_file("hemispheres.mp3"))),
    10: Scene("Circumstances", play >> System(play_file("circumstances.mp3"))),
    11: SceneGroup("Natural Science", [
            Scene("Intro", play >> System(play_file("ns_intro.mp3"))),
            Scene("Outro", play >> System(play_file("ns_outro.mp3"))),
       ]),
    12:Scene("YYZ",  Process(RemoveDuplicates()) >> yyz),
    13:Scene("TimeStandSteel.D4",  
			[ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main,
			ChannelFilter(3) >> Process(RemoveDuplicates(0.01)) >> 
			[
				(
				tss_d4_melo_tom_A // 
				tss_d4_castanet // 
				tss_d4_melo_tom_B // 
				tss_d4_808_tom
				)
	 		]]),
    14:Scene("Closer A", Process(RemoveDuplicates(0.01)) >> closer_patch_celesta_d4),
    15:Scene("Closer B", Process(RemoveDuplicates(0.01)) >> closer_patch_d4),
    16:Scene("YYZ", Process(RemoveDuplicates()) >> yyz),
    17:Scene("Mission",  mission),
