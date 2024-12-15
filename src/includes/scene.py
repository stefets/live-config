
global_init = [
    SD90_Initialize,
    HueNormal,
]
_scenes = {
    1: Scene("Initialize", init_patch = global_init, patch = Discard()),
    2: SceneGroup("Rush", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Generic", init_patch = MPG123_PLAYLIST, patch = Discard()//p_rush),
            Scene("Subdivisions", init_patch = i_rush_sub//MPG123_PLAYLIST, patch = Discard()//p_rush),
            Scene("TheTrees", init_patch = i_rush_trees//MPG123_PLAYLIST, patch = Discard()//p_rush_trees),
            Scene("Grand Designs", init_patch = i_rush_gd, patch = Discard()//p_rush_gd),
            Scene("Marathon", init_patch = i_rush, patch = Discard()),
            Scene("YYZ", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("Limelight", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("FlyByNight", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("RedBarchetta", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("Freewill", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("SpritOfRadio", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("TomSawyer", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("CloserToTheHeart", init_patch = i_rush//MPG123_PLAYLIST, patch = p_rush),
            Scene("RedBarchetta", init_patch=i_rush, patch=LatchNotes(False,reset='C3') >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
            Scene("FreeWill", init_patch=i_rush, patch=Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
            Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, pk5 >> Transpose(-24) >> closer_base]),
            Scene("Time Stand Still", [ChannelFilter(1) >> tss_keyboard_main, pk5 >> LatchNotes(False, reset='c4') >> tss_foot_main]),
            Scene("Analog Kid", init_patch=i_rush, patch=analogkid_main),
            Scene("Analog Kid Keyboard", analogkid_main),
            Scene("Time Stand Still Keyboard",
            [
                ChannelFilter(1) >> tss_keyboard_main,
                ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main
            ]),
            Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3') >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
            Scene("FreeWill Keyboards", Transpose(0) >> LatchNotes(False,reset='E3') >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
            # Scene("Marathon/Intro/Chords", Port(1) >> (
            #     [
            #         ChannelSplit({
            #             akai_channel : marathon_intro,
            #             pk5_channel : marathon_chords,
            #         }),
            #         ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(1,2) >> Port(1) >> 
            #             Fork([Channel(3),Channel(4)]) >>
            #             Fork([(CtrlFilter(2) >> Process(OnPitchbend,direction=-1))],
            #                 [(CtrlFilter(1) >> CtrlMap(1,7))])
            #     ])),
            # Scene("Marathon/Bridge/Solo/Ending", 
            #     ChannelSplit(
            #         {
            #             akai_channel : (marathon_bridge // marathon_bridge_split),
            #             pk5_channel : marathon_chords,
            #         })),
        ]),
    3: SceneGroup("BassCover", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Default", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Queen", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("T4F", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Toto", init_patch = MPG123_PLAYLIST, patch = Discard()),
        ]),
    4: SceneGroup("Recording", [
            Scene("Bass", init_patch = Discard(), patch = p_transport),
        ]),
    5: SceneGroup("BigCountry", [
            Scene("BassCover", init_patch = MPG123_PLAYLIST//Discard(), patch = Discard()),
            Scene("InBigCountry", init_patch = i_big_country, patch = p_big_country),
            Scene("HighlandScenery", init_patch = Discard(), patch = p_highland_scenery),
            Scene("Inwards", init_patch = Discard(), patch = p_pk5ctrl_generic>>p_base),
            Scene("AnglePark", init_patch = Discard(), patch = p_pk5ctrl_generic>>p_base),
            Scene("Wonderland", init_patch = p_wonderland_init, patch = p_wonderland),
            Scene("RecWonderland", init_patch = Call(HD500PC("14D")), patch = p_wonderland_rec),
        ]),
    6: SceneGroup("GrandDesignsStudio", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = p_rush_gd_demo),
            Scene("Futur", init_patch = Discard(), patch = p_transport),
        ]),
    7: SceneGroup("Keyboard", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Init SD90", init_patch = SD90_Initialize, patch = Discard()),
            Scene("BrushingSaw", LatchNotes(False, reset='f3') >> Transpose(-24) >> BrushingSaw),
            Scene("Xtremities", Xtremities),
            Scene("BagPipe", BagPipe),
            Scene("Borealis", Borealis),
            Scene("FifthAtmAft", FifthAtmAft),
            Scene("RichChoir", RichChoir),
            Scene("CircularPad", CircularPad),
            Scene("Oxigenizer", Oxigenizer),
            Scene("Quasar", Quasar),
            Scene("HellSection", HellSection),
            Scene("Itopia", Itopia),
            Scene("Kalimba", Kalimba),
            Scene("Dog", Dog),
            Scene("Siren", Siren),
            Scene("Explosion", Explosion),
            Scene("Thunder", Thunder),
            Scene("DoorCreak", DoorCreak),
            Scene("Laughing", Laughing),
            Scene("Applause", Applause),
            Scene("Telephone2", Telephone2),
            Scene("Rain", Rain),
            Scene("Drums", Amb_Room),
            Scene("NatureSound", akai_pad_nature),
        ]),
    8: SceneGroup("Cakewalk", [ 
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Play", init_patch = CakePlay, patch = Discard()),
            Scene("Stop", init_patch = CakeStop, patch = Discard()),
            Scene("Record", init_patch = CakeRecord, patch = Discard()),
            Scene("Rewind", init_patch = CakeRewind, patch = Discard()),
            Scene("Forward", init_patch = CakeForward, patch = Discard()),
            Scene("Drum", init_patch = SP1, patch = Output(sd90_midi_2, channel=10, program=(ClassicalDrum, 1))),
        ]),
    9: SceneGroup("MP3Player", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Hits", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Middleage", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("TV", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("NinaHagen", init_patch = MPG123_PLAYLIST, patch = Discard()),            
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("GraceUnderPressure", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("SteveMorse", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Colocs", init_patch = MPG123_PLAYLIST, patch = Discard()),
        ]),
    10: SceneGroup("Spotify", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Rush", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch = Discard(),  init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Studio.Normal", init_patch = HueNormal, patch = Discard()),
            Scene("Studio.Galaxie", init_patch = HueGalaxie, patch = Discard()),
            Scene("Studio.Demon", init_patch = HueDemon, patch = Discard()),
            Scene("Studio.SoloRed", init_patch = HueSoloRed, patch = Discard()),
            Scene("Studio.Detente", init_patch = HueDetente, patch = Discard()),
            Scene("Studio.Veilleuse", init_patch = HueVeilleuse, patch = Discard()),
            Scene("Studio.Lecture", init_patch = HueLecture, patch = Discard()),
            Scene("Studio.FullBlanc", init_patch = HueSsFullBlanc, patch = Discard()),
            Scene("Cuisine.Minimal", init_patch = HueCuisine, patch = Discard()),
            Scene("Chambre.Minimal", init_patch = HueChambreMaitre, patch = Discard()),
            Scene("AllOff", init_patch = HueAllOff, patch = Discard()),
                Scene("OneSliderMix",
            init_patch=Call(Playlist()), 
            patch=[ Filter(NOTEON|NOTEOFF) >> KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxieMax,
                    Filter(CTRL) >> CtrlSplit({
                        7: SendOSC(56420, '/mix', 0, cursor_value_converter),
                        1: SendOSC(56420, '/mix', 1, cursor_value_converter),
                    })
                    ]
            ),
            Scene("MultiSlidersMix", init_patch=Call(Playlist()),
                    patch=Filter(CTRL) >> CtrlFilter(1,7) >> 
                        [ 
                            SendOSC(56420, '/mix', 0,  cursor_value_converter),
                            SendOSC(56420, '/mix', 1,  cursor_value_converter),
                            SendOSC(56420, '/mix', 2,  cursor_value_converter),
                            SendOSC(56420, '/mix', 3,  cursor_value_converter),
                            SendOSC(56420, '/mix', 6,  cursor_value_converter),
                            SendOSC(56420, '/mix', 7,  cursor_value_converter),
                            SendOSC(56420, '/mix', 8,  cursor_value_converter),
                            SendOSC(56420, '/mix', 9,  cursor_value_converter),
                            SendOSC(56420, '/mix', 10, cursor_value_converter),
                        ]),
                Scene("ToggleMute", init_patch=Call(Playlist()),
                    patch=[
                        Filter(NOTEON)  >> SendOSC(56420, '/mute', 0, 1),
                        Filter(NOTEON)  >> SendOSC(56420, '/mute', 1, 1),
                        Filter(NOTEOFF) >> SendOSC(56420, '/mute', 0, 0),
                        Filter(NOTEOFF) >> SendOSC(56420, '/mute', 1, 0),
                    ]),
                ]),
                
    12: SceneGroup("SoundcraftUI", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Record", init_patch = ui_rectoggle, patch = Discard()),
        
        ]),
    13: SceneGroup("SD90", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Init SD90", init_patch = SD90_Initialize, patch = Discard()),
            Scene("Special1", init_patch = SP1, patch = Discard()),
            Scene("Special2", init_patch = SP2, patch = Discard()),
            Scene("Classical", init_patch = CLASIC, patch = Discard()),
            Scene("Contemporary", init_patch = CONTEM, patch = Discard()),
            Scene("Solo", init_patch = SOLO, patch = Discard()),
            Scene("Enhanced", init_patch = ENHANC, patch = Discard()),
        ]),
    14: SceneGroup("MUSE", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Assassin", init_patch = Discard(), patch = p_muse),
            Scene("Hysteria", init_patch = Discard(), patch = p_muse),
            Scene("Cydonia",  init_patch = Discard(), patch = p_muse),
            Scene("Starlight", init_patch = Discard(), patch = p_muse),
            Scene("Stockholm", init_patch = Discard(), patch = [p_muse_stockholm, p_muse]),
        ]),
    15:  SceneGroup("Sampler", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Track1", init_patch = Discard(), patch = Discard()),
        ]),
    16:  SceneGroup("POC", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("INTERLUDE", patch = pk5 >> Filter(NOTEON) >> NoteOn(0, 0) >> VLC_PL, init_patch = Pass()),

        ]),
    17:  SceneGroup("VLC", [
            Scene("Select a Subscene", init_patch = Discard(), patch = Discard()),
            Scene("Stop", init_patch = VLC_STOP, patch = Discard()),
            Scene("Play", init_patch = VLC_PLAY, patch = Discard()),
            Scene("Pause", init_patch = VLC_PAUSE, patch = Discard()),
            Scene("Repeat-ON", init_patch =  VLC_REPEAT_ON, patch = Pass()),
            Scene("Repeat-OFF", init_patch = VLC_REPEAT_OFF, patch = Pass ()),
            Scene("Toggle-Loop", init_patch = VLC_TOGGLE_LOOP, patch = Pass ()),
            Scene("Toggle-Repeat", init_patch = VLC_TOGGLE_REPEAT, patch = Pass ()),
            Scene("Playlist item 1", init_patch = NoteOn(0, 0) >> VLC_PL, patch = Discard()),
            Scene("Playlist item 2", init_patch = Ctrl(1, 0) >> VLC_PL, patch = Discard()),
        ]),        
    18:  SceneGroup("GT10B", [
            Scene("Select a Bank", init_patch = Discard(), patch = Discard()),
            Scene("U01_A", init_patch = [GT10Bank0, Program(1) >> GT10BProgramSelector], patch = Discard()),
            Scene("U01_B", init_patch = [GT10Bank0, Program(2) >> GT10BProgramSelector], patch = Discard()),
    ]),
    19:  SceneGroup("HD500", [
            Scene("Select option", init_patch = Discard(), patch = Discard()),
            Scene("TunerOn", init_patch = [HD500_TunerOn], patch = Discard()),
            Scene("TunerOff", init_patch = [HD500_TunerOff], patch = Discard()),
            Scene("FS1", init_patch = [FS1], patch = Discard()),
            Scene("FS2", init_patch = [FS2], patch = Discard()),
    ]),    
    20:  SceneGroup("ID20:Free", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
    ]),    
    21:  SceneGroup("ID21:Free", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
    ]),    
    22:  SceneGroup("ID22:Free", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
    ]),    
}
