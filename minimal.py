    3: Scene("test", patch=marathon_chords),
    #2: Scene("test", patch=(gt10b_volume // piano), init_patch=U01_A),
    2: Scene("test", patch=piano, init_patch=U26_D)
    #2: Scene("OSC", System('sendosc 192.168.2.25 55555 /stefets i 123'))
    #2: Scene("Hemispheres", PlayButton >> System(play_file("spectral_mornings.mid"))),
    #2: Scene("Hemispheres", play >> System(play_file("hemispheres.mp3")),
	#2: SceneGroup("Group1", [ 
		#Scene("Test",Pass(),Call(show_time)),
		#]) 
