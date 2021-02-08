    2: SceneGroup("Rush",
        [
        Scene("Default", init_patch=P02A, patch=Discard()),
        Scene("Analog Kid Keyboard", analogkid_main),
        #Scene("Analog Kid Keyboard", [ChannelFilter(2) >> analogkid_main, ChannelFilter(1) >> analogkid_ending ]),
        Scene("Time Stand Still Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
        Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
        Scene("FreeWill Keyboard", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
       ]),
    3: SceneGroup("Closer",
        [
            Scene("Default", init_patch=Discard(), patch=closer_main),
        ]),
    4:SceneGroup ("Marathon", [
        Scene("Marathon-Intro/Chords", Port(1) >> (
          [
            ChannelSplit({
                keyboard_channel : marathon_intro,
                pk5_channel : marathon_chords,
            }),
            (ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(1,2) >> Port(1) >> Fork([Channel(3),Channel(4)]) >>
            [
             (CtrlFilter(2)>>Process(OnPitchbend,direction=-1)) //
                (CtrlFilter(1)>>CtrlMap(1,7))
            ])
          ])),
        Scene("Marathon-Bridge/Solo/Ending", 
            ChannelSplit({
                1 : (marathon_bridge // marathon_bridge_split),
                2 : marathon_chords,
            })),
   ]),
