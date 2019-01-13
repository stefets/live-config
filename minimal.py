    2: Scene("POD", patch=piano, init_patch=U01_A),
    3: Scene("POD", patch=piano, init_patch=U26_D)
    #2: Scene("OSC", System('sendosc 192.168.2.25 55555 /stefets i 123'))
    #2: Scene("Piano",marathon_init // marathon_chords),
    #2: Scene("Hemispheres", PlayButton >> System(play_file("spectral_mornings.mid"))),
    #2: Scene(name="Test",  init_patch=q49, patch=(Output('PODHD500', channel=9, program=64)))
    #2: Scene(name="Test",  patch=q49, init_patch=(Output('PODHD500', channel=9, program=64)))
    #2: Scene("Hemispheres", play >> System(play_file("hemispheres.mp3")),
    #5: Scene("Test", mission),
    #6: Scene(name="Test", patch=analogkid_main, init_patch=pod_init),
    #7: Scene(name="Test", patch=analogkid_main, init_patch=pod_init),
    #2: Scene(name="Test", patch=[analog_pod, analogkid_main], init_patch=pod_init),
	#2: SceneGroup("Group1", [ 
		#Scene("Test",Pass(),Call(show_time)),
		#]) 
