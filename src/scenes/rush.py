
_scenes = {
    1: Scene("Initialize", init_patch=SD90_Initialize, patch=interlude),
    2: Scene("RedBarchetta", init_patch=i_rush, patch=LatchNotes(False,reset='C3') >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    3: Scene("FreeWill", init_patch=i_rush, patch=Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
    4: Scene("CloserToTheHeart", [ChannelFilter(1) >> closer_main, pk5 >> Transpose(-24) >> closer_base]),
    5: SceneGroup("Time Stand Still", [
			Scene("TSS-Keyboard", [ChannelFilter(1) >> tss_keyboard_main, pk5 >> LatchNotes(False, reset='c4') >> tss_foot_main]),
	   ]),
    6: Scene("Analog Kid", init_patch=i_rush, patch=analogkid_main),
    7: SceneGroup("rush",
        [
        Scene("Analog Kid Keyboard", analogkid_main),
        #Scene("Analog Kid Keyboard", [ChannelFilter(2) >> analogkid_main, ChannelFilter(1) >> analogkid_ending ]),
        Scene("Time Stand Still Keyboard",
        [
            ChannelFilter(1) >> tss_keyboard_main,
            ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main
        ]),
        Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3') >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
        Scene("FreeWill Keyboards", Transpose(0) >> LatchNotes(False,reset='E3') >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
       ]),
    8:SceneGroup(
        "Marathon", 
        [
            Scene("Intro/Chords", Port(1) >> (
            [
                ChannelSplit({
                    akai_channel : marathon_intro,
                    pk5_channel : marathon_chords,
                }),
                ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(1,2) >> Port(1) >> 
                    Fork([Channel(3),Channel(4)]) >>
                    Fork([(CtrlFilter(2) >> Process(OnPitchbend,direction=-1))],
                         [(CtrlFilter(1) >> CtrlMap(1,7))])
            ])),
            Scene("Bridge/Solo/Ending", 
                ChannelSplit(
                    {
                        akai_channel : (marathon_bridge // marathon_bridge_split),
                        pk5_channel : marathon_chords,
                    })),

        ]),
}    
