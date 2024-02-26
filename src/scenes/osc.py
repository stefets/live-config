
_scenes = {
    1: Scene("Initialize", init_patch=SD90_Initialize, patch=interlude),
    2:SceneGroup("Demonstrations", [
    Scene("OneSliderMix",
            init_patch=Call(Playlist()), 
            patch=[ Filter(NOTEON|NOTEOFF) >> KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxieMax,
                    Filter(CTRL) >> CtrlSplit({
                        7: SendOSC(56420, '/mix', 0, data2_to_zero_one_range),
                        1: SendOSC(56420, '/mix', 1, data2_to_zero_one_range),
                    })
                    ]
            ),
    Scene("MultiSlidersMix", init_patch=Call(Playlist()),
            patch=Filter(CTRL) >> CtrlFilter(1,7) >> 
                [ 
                    SendOSC(56420, '/mix', 0,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 1,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 2,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 3,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 6,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 7,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 8,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 9,  data2_to_zero_one_range),
                    SendOSC(56420, '/mix', 10, data2_to_zero_one_range),
                ]),
        Scene("ToggleMute", init_patch=Call(Playlist()),
            patch=[
                Filter(NOTEON)  >> SendOSC(56420, '/mute', 0, 1),
                Filter(NOTEON)  >> SendOSC(56420, '/mute', 1, 1),
                Filter(NOTEOFF) >> SendOSC(56420, '/mute', 0, 0),
                Filter(NOTEOFF) >> SendOSC(56420, '/mute', 1, 0),
            ]),
    ])
}    
