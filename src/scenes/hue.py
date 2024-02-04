
_scenes = {
    1: Scene("Initialize", init_patch=SD90_Initialize, patch=interlude),
        2:SceneGroup("Demonstrations", [
	    Scene("Dimmer",
                init_patch=Call(Playlist()), 
                patch=[ Filter(NOTEON|NOTEOFF) >> KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxieMax,
                        Filter(CTRL) >> CtrlSplit({
                            7: Pass(),
                            1: Pass(),
                        })
                      ]
                ),
            Scene("Off", init_patch=Call(Playlist()),
                patch=[
                    Pass(),
                ]),
        ]),
        3: SceneGroup("Éclairage HUE",
        [
            Scene("Init", init_patch=Discard(), patch=Discard()),
            Scene("Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Demon", init_patch=HueDemon, patch=Discard()),
            Scene("SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Off", init_patch=HueStudioOff, patch=Discard()),
        ]),

}