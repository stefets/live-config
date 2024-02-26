
_scenes = {
    1: Scene("Initialize", init_patch = SD90_Initialize, patch = Discard()),
    2: SceneGroup("RUSH", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
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
        ]),
    3: SceneGroup("BassCover", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Default", init_patch = MPG123_PLAYLIST//U01_A, patch = Discard()),
            Scene("Queen", init_patch = MPG123_PLAYLIST//U01_A, patch = Discard()),
            Scene("T4F", init_patch = MPG123_PLAYLIST//U01_A, patch = Discard()),
            Scene("Toto", init_patch = MPG123_PLAYLIST//U01_A, patch = Discard()),
        ]),
    4: SceneGroup("Recording", [
            Scene("Bass", init_patch = Discard(), patch = p_transport),
        ]),
    5: SceneGroup("BigCountry", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("InBigCountry", init_patch = i_big_country, patch = p_big_country),
            Scene("HighlandScenery", init_patch = U01_B // P14B, patch = p_highland_scenery),
            Scene("Inwards", init_patch = U01_B // P14B, patch = p_pk5ctrl_generic>>p_base),
            Scene("AnglePark", init_patch = U01_B // P14B, patch = p_pk5ctrl_generic>>p_base),
            Scene("Wonderland", init_patch = p_wonderland_init, patch = p_wonderland),
        ]),
    6: SceneGroup("GrandDesignsStudio", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = p_rush_gd_demo),
            Scene("Futur", init_patch = Discard(), patch = p_transport),
        ]),
    7: SceneGroup("Keyboard", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
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
    8: SceneGroup("Majestyx", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Setlist", init_patch = MPG123_PLAYLIST//U01_A, patch = Discard()),
        ]),
    9: SceneGroup("MP3Player", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Hits", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("Middleage", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("TV", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("NinaHagen", init_patch = MPG123_PLAYLIST, patch = Discard()),            
            Scene("PowerWindows", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("GraceUnderPressure", init_patch = MPG123_PLAYLIST, patch = Discard()),
            Scene("SteveMorse", init_patch = MPG123_PLAYLIST, patch = Discard()),
        ]),
    10: SceneGroup("Spotify", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Rush", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch = Discard(),  init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch = Discard(), init_patch = Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
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
        ]),
    12: SceneGroup("Libre", [
        ]),
    13: SceneGroup("SD90-BANK", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Special1", init_patch = SP1, patch = Discard()),
            Scene("Special2", init_patch = SP2, patch = Discard()),
            Scene("Classical", init_patch = CLASIC, patch = Discard()),
            Scene("Contemporary", init_patch = CONTEM, patch = Discard()),
            Scene("Solo", init_patch = SOLO, patch = Discard()),
            Scene("Enhanced", init_patch = ENHANC, patch = Discard()),
        ]),
    14: SceneGroup("MUSE", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Assassin", init_patch = AfxOff // P01A, patch = p_muse),
            Scene("Hysteria", init_patch = AfxOff  // P01A, patch = p_muse),
            Scene("Cydonia",  init_patch = AfxOff// P01A, patch = p_muse),
            Scene("Starlight", init_patch = AfxOff // P01A, patch = p_muse),
            Scene("Stockholm", init_patch = AfxOff // P01A, patch = [p_muse_stockholm, p_muse]),
        ]),
    15: SceneGroup("MajestyxLive", [
            Scene("STOP", init_patch = VLC_STOP, patch = Discard()),
            Scene("INTERLUDE", init_patch = NoteOn(0, 0) >> VLC_PL, patch = Pass()),
            Scene("01-Rockin Paradise", init_patch = Ctrl(1, 0) >> VLC_PL, patch = Pass()),
            Scene("02-BlueCollarMan", init_patch = NoteOn(2, 0) >> VLC_BASE, patch = Pass()),
            Scene("03-Lorelei", init_patch = NoteOn(3, 0) >> VLC_BASE, patch = Pass()),
            Scene("04-Too Much Time", init_patch = NoteOn(4, 0) >> VLC_BASE, patch = Pass()),
            Scene("05-Snowblind", init_patch = NoteOn(5, 0) >> VLC_BASE, patch = Pass()),
            Scene("06-Come Sail Away", init_patch = NoteOn(6, 0) >> VLC_BASE, patch = Pass()),
            Scene("07-Queen Of Spades", init_patch = NoteOn(7, 0) >> VLC_BASE, patch = Pass()),
            Scene("08-Light Up", init_patch = NoteOn(8, 0) >> VLC_BASE, patch = Pass()),
            Scene("09-The Best of Time", init_patch = NoteOn(9, 0) >> VLC_BASE, patch = Pass()),
            Scene("10-Lady", init_patch = NoteOn(10, 0) >> VLC_BASE, patch = Pass()),
            Scene("11-Fooling Yourself", init_patch = NoteOn(11, 0) >> VLC_BASE, patch = Pass()),
            Scene("12-Roboto", init_patch = NoteOn(12, 0) >> VLC_BASE, patch = Pass()),
            Scene("13-Show Me The Way", init_patch = NoteOn(13, 0) >> VLC_BASE, patch = Pass()),
            Scene("14-Lights", init_patch = NoteOn(14, 0) >> VLC_BASE, patch = Pass()),
            Scene("15-Pieces Of Eight", init_patch = NoteOn(15, 0) >> VLC_BASE, patch = Pass()),
            Scene("16-I’m Ok", init_patch = NoteOn(16, 0) >> VLC_BASE, patch = Pass()),
            Scene("17-Miss America", init_patch = NoteOn(17, 0) >> VLC_BASE, patch = Pass()),
            Scene("18-Babe", init_patch = NoteOn(18, 0) >> VLC_BASE, patch = Pass()),
            Scene("19-Renegade", init_patch = NoteOn(19, 0) >> VLC_BASE, patch = Pass()),
            Scene("20-Crystal Ball", init_patch = NoteOn(20, 0) >> VLC_BASE, patch = Pass()),
            Scene("21-Grand Illusion", init_patch = NoteOn(21, 0) >> VLC_BASE, patch = Pass()),
            Scene("22-BoatOnThRiver", init_patch = NoteOn(22, 0) >> VLC_BASE, patch = Pass()),
            Scene("23-SuiteMadameBlue", init_patch = NoteOn(23, 0) >> VLC_BASE, patch = Pass()),
            Scene("Repeat-ON", init_patch =  VLC_REPEAT_ON, patch = Pass()),
            Scene("Repeat-OFF", init_patch = VLC_REPEAT_OFF, patch = Pass ()),
        ]),    
    16:  SceneGroup("Sampler", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("Track1", init_patch = Discard(), patch = Discard()),
        ]),
    17:  SceneGroup("POC", [
            Scene("Select", init_patch = Discard(), patch = Discard()),
            Scene("INTERLUDE", patch = pk5 >> Filter(NOTEON) >> NoteOn(0, 0) >> VLC_BASE, init_patch = Pass()),

        ]),
}
