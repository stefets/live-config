    2: SceneGroup("Rush",
        [
            Scene("Subdivisions", init_patch=i_rush, patch=p_rush),
            Scene("The Trees", init_patch=i_rush_trees, patch=p_rush_trees),
            Scene("Grand Designs", init_patch=i_rush, patch=p_rush_gd),
            Scene("Marathon", init_patch=i_rush, patch=Discard()),
        ]),
    3: SceneGroup("Styx",
        [
            Scene("Training", init_patch=U01_A, patch=Discard()),
            Scene("Majestyx-live", init_patch=U01_C, patch=Discard()),
        ]),
    4: SceneGroup("Big Country",
        [
            Scene("In a big country", init_patch=i_big_country, patch=p_big_country),
        ]),
    5: SceneGroup("power-windows",
        [
            Scene("Default", init_patch=Discard(), patch=p_rush_gd),
        ]),
    99: SceneGroup("Éclairage HUE",
        [
            Scene("Init", init_patch=Discard(), patch=Discard()),
            Scene("Normal", init_patch=HueNormal, patch=Discard()),
            Scene("Galaxie", init_patch=HueGalaxie, patch=Discard()),
            Scene("Demon", init_patch=HueDemon, patch=Discard()),
            Scene("SoloRed", init_patch=HueSoloRed, patch=Discard()),
            Scene("Off", init_patch=HueOff, patch=Discard()),
        ]),


