    2:SceneGroup(
        "solo-mode", 
        [
            Scene("Marathon-Intro/Chords", Port(1) >> (
            [
                ChannelSplit({
                    cme_channel : marathon_intro,
                    pk5_channel : marathon_chords,
                }),
                ChannelFilter(9) >> Filter(CTRL) >> CtrlFilter(1,2) >> Port(1) >> 
                    Fork([Channel(3),Channel(4)]) >>
                    Fork([(CtrlFilter(2) >> Process(OnPitchbend,direction=-1))],
                         [(CtrlFilter(1) >> CtrlMap(1,7))])
            ])),
            Scene("Marathon-Bridge/Solo/Ending", 
                ChannelSplit(
                    {
                        cme_channel : (marathon_bridge // marathon_bridge_split),
                        pk5_channel : marathon_chords,
                    })),

        ]),
