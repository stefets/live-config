    2: SceneGroup("Compositions", [    
            Scene("Centurion - no guitar, no synth", play >> System(play_file("centurion.mp3"))),
            Scene("Centurion - Synth", centurion_patch),
            Scene("Cool Boy - no guitar, no synth", play >> System(play_file("cool_boy.mp3"))),
            #Scene("Cool Boy - Synth", analogkid),
            #Scene("Centurion - Patch et Video", centurion_patch, [centurion_video]),
            Scene("Shadow - no bass", play >> System(play_file("shadow.mp3"))),
            Scene("Voleur - no guitar", play >> System(play_file("voleur.mp3"))),
       ]),   
