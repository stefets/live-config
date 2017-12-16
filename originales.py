    2: SceneGroup("Compositions", [    
            Scene("Centurion - no guitar, no synth", play >> System(player + "centurion.mp3")),
            Scene("Centurion - Synth", centurion_patch),
            Scene("Cool Boy - no guitar, no synth", play >> System(player + "cool_boy.mp3")),
            #Scene("Cool Boy - Synth", analogkid),
            #Scene("Centurion - Patch et Video", centurion_patch, [centurion_video]),
            Scene("Shadow - no bass", play >> System(player + "shadow.mp3")),
            Scene("Voleur - no guitar", play >> System(player + "voleur.mp3")),
       ]),   
