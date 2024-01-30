    1: Scene("Initialize", init_patch=SD90_Initialize, patch=Discard()),
    2: SceneGroup("RUSH",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Generic", init_patch=Call(Playlist()), patch=Discard()//p_rush),
            Scene("Subdivisions", init_patch=i_rush_sub//Call(Playlist()), patch=Discard()//p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist()), patch=Discard()//p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush_gd, patch=Discard()//p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
            Scene("YYZ", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("Limelight", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("FlyByNight", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("RedBarchetta", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("Freewill", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("SpritOfRadio", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("TomSawyer", init_patch=i_rush//Call(Playlist()), patch=p_rush),
            Scene("CloserToTheHeart", init_patch=i_rush//Call(Playlist()), patch=p_rush),
        ]),
    3: SceneGroup("BassCover",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Default", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Queen", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("T4F", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Toto", init_patch=Call(Playlist())//U01_A, patch=Discard()),
        ]),
    4: SceneGroup("Recording",
        [
            Scene("Bass", init_patch=Discard(), patch=p_transport),
        ]),
    5: SceneGroup("BigCountry",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("InBigCountry", init_patch=i_big_country, patch=p_big_country),
            Scene("HighlandScenery", init_patch=U01_B // P14B, patch=p_highland_scenery),
            Scene("Inwards", init_patch=U01_B // P14B, patch=p_pk5ctrl_generic>>p_base),
            Scene("AnglePark", init_patch=U01_B // P14B, patch=p_pk5ctrl_generic>>p_base),
            Scene("Wonderland", init_patch=p_wonderland_init, patch=p_wonderland),
        ]),
    6: SceneGroup("GrandDesignsStudio",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("PowerWindows", init_patch=Call(Playlist()), patch=p_rush_gd_demo),
            Scene("Futur", init_patch=Discard(), patch=p_transport),
        ]),
    7: SceneGroup("Keyboard",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
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
        ]),
    8: SceneGroup("Libre",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
        ]),
    9: SceneGroup("MP3Player",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("TV", init_patch=Call(Playlist()), patch=Discard()),
            Scene("GraceUnderPressure", init_patch=Call(Playlist()), patch=Discard()),
            Scene("Hits", init_patch=Call(Playlist()), patch=Discard()),
            Scene("Majestyx", init_patch=Call(Playlist())//U01_A, patch=Discard()),
            Scene("Middleage", init_patch=Call(Playlist()), patch=Discard()),
            Scene("NinaHagen", init_patch=Call(Playlist()), patch=Discard()),            
            Scene("PowerWindows", init_patch=Call(Playlist()), patch=Discard()),
            Scene("SteveMorse", init_patch=Call(Playlist()), patch=Discard()),
        ]),
    10: SceneGroup("Spotify", 
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Rush", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "0L1cHmn20fW7KL2DrJlFCL")),
            Scene("BigCountry", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "15d8HFEqWAkcwYpPsI6vgW")),
            Scene("PatMetheny",patch=Discard(),  init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "6WkqCksGxIiCkuKWHMqiMA")),
            Scene("Medieval", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST", "3zkrx4OGDerC4vYoKWZ7d7")),
            Scene("LilyBurns", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","2rKQYsL2f5iONT7tlAsOuc")),
            Scene("MichelCusson", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","4kqcWUHZTtfX8rZeILjhdo")),
            Scene("Vola", patch=Discard(), init_patch=Call(setenv, "SPOTIFY_PLAYLIST","02v48VLu8jtnkeYlfl1Xrt")),
        ]),
    11: SceneGroup("HUE",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Studio.Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Studio.Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Studio.Demon", init_patch=HueDemon, patch=Discard()),
            Scene("Studio.SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Studio.Detente", init_patch=HueDetente, patch=Discard()),
            Scene("Studio.Veilleuse", init_patch=HueVeilleuse, patch=Discard()),
            Scene("Studio.Lecture", init_patch=HueLecture, patch=Discard()),
            Scene("Studio.FullBlanc", init_patch=HueSsFullBlanc, patch=Discard()),
            Scene("Cuisine.Minimal", init_patch=HueCuisine, patch=Discard()),
            Scene("Chambre.Minimal", init_patch=HueChambreMaitre, patch=Discard()),
            Scene("AllOff", init_patch=HueAllOff, patch=Discard()),
        ]),
    12: SceneGroup("Libre",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
        ]),
    13: SceneGroup("SD90-BANK",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Special1", init_patch=SP1, patch=Discard()),
            Scene("Special2", init_patch=SP2, patch=Discard()),
            Scene("Classical", init_patch=CLASIC, patch=Discard()),
            Scene("Contemporary", init_patch=CONTEM, patch=Discard()),
            Scene("Solo", init_patch=SOLO, patch=Discard()),
            Scene("Enhanced", init_patch=ENHANC, patch=Discard()),
        ]),
    14: SceneGroup("MUSE",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Assassin", init_patch=AfxOff // P01A, patch=p_muse),
            Scene("Hysteria", init_patch=AfxOff  // P01A, patch=p_muse),
            Scene("Cydonia",  init_patch=AfxOff// P01A, patch=p_muse),
            Scene("Starlight", init_patch=AfxOff // P01A, patch=p_muse),
            Scene("Stockholm", init_patch=AfxOff // P01A, patch=[p_muse_stockholm, p_muse]),
        ]),
