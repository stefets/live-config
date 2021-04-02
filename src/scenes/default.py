    2: SceneGroup("solo-mode",
        [
            Scene("Rush", init_patch=P02A, patch=Discard()),
            Scene("BigCountry", init_patch=i_big_country, patch=p_big_country),
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
            Scene("Default", init_patch=P02A, patch=Discard()),
        ]),
    7: SceneGroup("bass_cover",
        [
            Scene("Default", init_patch=Discard(), patch=Discard()),
        ]),
