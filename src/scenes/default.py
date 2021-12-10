    2: SceneGroup("Rush",
        [
            Scene("Subdivisions", init_patch=i_rush, patch=p_rush),
            Scene("The Trees", init_patch=i_rush_trees, patch=p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush_gd, patch=p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
        ]),
    3: SceneGroup("BassCover",
        [
            Scene("Default", init_patch=HueGalaxie, patch=U01_A),
            Scene("Futur", init_patch=Discard(), patch=Discard()),
        ]),
    4: SceneGroup("Big Country",
        [
            Scene("In a big country", init_patch=i_big_country, patch=p_big_country),
        ]),
    5: SceneGroup("Majestyx",
        [
            Scene("Training", init_patch=U01_A, patch=Discard()),
            Scene("Majestyx-live", init_patch=U03_A, patch=Discard()),
        ]),
    6: SceneGroup("GrandDesignsStudio",
        [
            Scene("Default", init_patch=Discard(), patch=p_rush_gd),
        ]),
    7: SceneGroup("Demonstrations",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
            Scene("BrushingSaw", LatchNotes(False, reset='f3') >> Transpose(-24) >> BrushingSaw),
            Scene("Explosion", patch=explosion),
        ]),
    6: SceneGroup("Compositions",
        [
            Scene("Centurion", init_patch=i_centurion, patch=p_centurion),
        ]),
    9: SceneGroup("Futur",
        [
            Scene("Futur", init_patch=Discard(), patch=Discard()),
        ]),
    10: SceneGroup("Éclairage HUE",
        [
            Scene("Init", init_patch=Discard(), patch=Discard()),
            Scene("Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Demon", init_patch=HueDemon, patch=Discard()),
            Scene("SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Off", init_patch=HueOff, patch=Discard()),
        ]),


