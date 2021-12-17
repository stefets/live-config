        2:SceneGroup("Demonstrations", [
	    Scene("OneSliderMix",
                init_patch=Call(Playlist(playlist_config)), 
                patch=[ Filter(NOTEON|NOTEOFF) >> KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxieMax,
                        Filter(CTRL) >> CtrlSplit({
                            7: SendOSC(56420, '/mix', 0, osc2midi_value_converter),
                            1: SendOSC(56420, '/mix', 1, osc2midi_value_converter),
                        })
                      ]
                ),
	    Scene("MultiSlidersMix", init_patch=Call(Playlist(playlist_config)),
                patch=Filter(CTRL) >> CtrlFilter(1,7) >> 
                    [ 
                        SendOSC(56420, '/mix', 0,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 1,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 2,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 3,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 6,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 7,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 8,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 9,  osc2midi_value_converter),
                        SendOSC(56420, '/mix', 10, osc2midi_value_converter),
                    ]),
            Scene("ToggleMute", init_patch=Call(Playlist(playlist_config)),
                patch=[
                    Filter(NOTEON)  >> SendOSC(56420, '/mute', 0, 1),
                    Filter(NOTEON)  >> SendOSC(56420, '/mute', 1, 1),
                    Filter(NOTEOFF) >> SendOSC(56420, '/mute', 0, 0),
                    Filter(NOTEOFF) >> SendOSC(56420, '/mute', 1, 0),
                ]),
        ])
