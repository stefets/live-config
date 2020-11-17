    2: SceneGroup("Rush cover", [
        Scene("Analog Kid Keyboard", analogkid_main),
        #Scene("Analog Kid Keyboard", [ChannelFilter(2) >> analogkid_main, ChannelFilter(1) >> analogkid_ending ]),
        Scene("TimeStandSteel", play >> System(play_file("time_stand_steel.mp3"))),
        Scene("Time Stand Still Keyboard", [ChannelFilter(1) >> tss_keyboard_main, ChannelFilter(2) >> LatchNotes(False, reset='c4') >> tss_foot_main]),
        Scene("KidGloves", play >> System(play_file("kid_gloves.mp3"))),
        Scene("KidGloves Keyboard", Transpose(0) >> LatchNotes(False,reset='F3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
        Scene("Freewill", play >> System(play_file("freewill.mp3"))),
        Scene("FreeWill Keyboard", Transpose(0) >> LatchNotes(False,reset='E3')  >> Harmonize('c', 'major', ['unison', 'octave']) >> keysynth),
        Scene("Territories", play >> System(play_file("territories.mid"))),
        Scene("Mission", play >> System(play_file("mission.mid"))),
       ]),
   3:SceneGroup ("Marathon", [
        Scene("Marathon-Intro/Chords", Port(1) >> (
          [
            ChannelSplit({
                q49_channel : marathon_intro,
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
