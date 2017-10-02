#-----------------------------------------------------------------------------------------------------------
# SCENES SECTION
#-----------------------------------------------------------------------------------------------------------
_scenes = {
    1: Scene("Reset",  reset),
    2: Scene("RedBarchetta", LatchNotes(False,reset='C3') >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    3: Scene("FreeWill", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    4: Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, ChannelFilter(2) >> Transpose(-24) >> closer_base]),
    5: SceneGroup("The Trees", [
            Scene("Bridge",  play >> System("mpg123 -q /mnt/flash/live/trees_full.mp3")),
            Scene("Synth", Transpose(-29) >> LatchNotes(False,reset='G0') >> lowsynth),
       ]),
    6: SceneGroup("Time Stand Still", [
			Scene("TSS-Intro", play >> System("mpg123 -q /mnt/flash/live/tss.mp3")),
			Scene("TSS-Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
	   ]),
    7: SceneGroup("2112", [
            Scene("Intro", play >> System("mpg123 -q /mnt/flash/live/2112.mp3")),
            Scene("Explosion", explosion),
       ]),
    8: Scene("Analog Kid", [ChannelFilter(2) >> analogkid, ChannelFilter(1) >> analogkid_ending ]),
    9: Scene("Hemispheres", play >> System("mpg123 -q /mnt/flash/live/hemispheres.mp3")),
    10: Scene("Circumstances", play >> System("mpg123 -q /mnt/flash/live/circumstances.mp3")),
    11: SceneGroup("Natural Science", [
            Scene("Intro", play >> System("mpg123 -q /mnt/flash/live/ns_intro.mp3")),
            Scene("Outro", play >> System("mpg123 -q /mnt/flash/live/ns_outro.mp3")),
       ]),
}
