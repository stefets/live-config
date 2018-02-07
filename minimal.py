    #2: Scene(name="Test",  init_patch=q49, patch=(Output('PODHD500', channel=9, program=64)))
    #2: Scene(name="Test",  patch=q49, init_patch=(Output('PODHD500', channel=9, program=64)))
    2: Scene("Test", mission),
    3: Scene(name="Test", patch=analogkid_main, init_patch=pod_init),
    4: Scene(name="Test", patch=analogkid_main, init_patch=pod_init),
    #2: Scene(name="Test", patch=[analog_pod, analogkid_main], init_patch=pod_init),
	#2: SceneGroup("Group1", [ 
		#Scene("Test",Pass(),Call(show_time)),
		#]) 
