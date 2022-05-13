    2: SceneGroup("Rush",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Subdivisions", init_patch=i_rush_sub, patch=p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("Divers", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("PowerWindows", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("GraceUnderPressure", init_patch=Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush_gd, patch=p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
        ]),
    3: SceneGroup("BassCover",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Default", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("Queen", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("T4F", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("Toto", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
        ]),
    4: SceneGroup("HBR",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("YYZ", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("Limelight", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("FlyByNight", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("TheTrees", init_patch=i_rush_trees//Call(Playlist(playlist_config)), patch=p_rush_trees),
            Scene("RedBarchetta", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("Freewill", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("SpritOfRadio", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("TomSawyer", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
            Scene("CloserToTheHeart", init_patch=i_rush//Call(Playlist(playlist_config)), patch=p_rush),
        ]),
    5: SceneGroup("BigCountry",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("In a big country", init_patch=i_big_country, patch=p_big_country),
            Scene("In a big country LIVE", init_patch=i_big_country_live, patch=p_big_country // p_big_country_live),
        ]),
    6: SceneGroup("GrandDesignsStudio",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Recorder", init_patch=Discard(), patch=p_recorder),
        ]),
    7: SceneGroup("Demonstrations",
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
            Scene("Demon", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Jokes", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Tabarnac", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("TLMEP", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
        ]),
    8: SceneGroup("Compositions",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Palindrome", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Centurion", init_patch=i_centurion, patch=p_centurion),
        ]),
    9: SceneGroup("MP3Player",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Majestyx", init_patch=Call(Playlist(playlist_config))//U01_A, patch=Discard()),
            Scene("MajestyxBasse", init_patch=Call(Playlist(playlist_config))//U03_A, patch=Discard()),
            Scene("Delirium", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Hits", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Middleage", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("NinaHagen", init_patch=Call(Playlist(playlist_config)), patch=Discard()),            
            Scene("SteveMorse", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("Timeline", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
            Scene("TV", init_patch=Call(Playlist(playlist_config)), patch=Discard()),
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
    11: SceneGroup("HUE Bridge",
        [
            Scene("Select", init_patch=Discard(), patch=Discard()),
            Scene("Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Demon", init_patch=HueDemon, patch=Discard()),
            Scene("SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Off", init_patch=HueOff, patch=Discard()),
        ]),

