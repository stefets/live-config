    2: SceneGroup("solo-mode",
        [
            Scene("Rush", init_patch=i_rush, patch=p_rush),
            Scene("Rush Grand Designs", init_patch=i_rush, patch=p_rush_gd),
            Scene("Big Country", init_patch=i_big_country, patch=p_big_country),
        ]),
    3: SceneGroup("styx",
        [
            Scene("Default", init_patch=U01_A, patch=Discard()),
        ]),
    4: SceneGroup("tabarnac",
        [
            Scene("Default", patch=Discard()),
        ]),
    5: SceneGroup("palindrome",
        [
            Scene("Centurion - guitar/synth cover", patch=centurion_patch),
        ]),
    6: SceneGroup("rush_cover",
        [
            Scene("Default", patch=Discard()),
        ]),
    7: SceneGroup("bass_cover",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    8: SceneGroup("demo",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    9: SceneGroup("demon",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    10: SceneGroup("fun",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    11: SceneGroup("hits",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    12: SceneGroup("middleage",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    13: SceneGroup("tv",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    14: SceneGroup("delirium",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
    15: SceneGroup("power-windows",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),

