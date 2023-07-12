
#
# PK5A patches as a controller
# Implement Roland PK5A Drums Mode default factory set and default user set
#

# Factory Set (Read Only)
pk5_dm_fs_mapping = [
    KeyFilter(notes=[36])
    >> [
        ChannelFilter(1) >> Discard(),
        ChannelFilter(2) >> Discard(),
        ChannelFilter(3) >> Discard(),
        ChannelFilter(4) >> Discard(),
        ChannelFilter(5) >> Discard(),
        ChannelFilter(6) >> Discard(),
        ChannelFilter(7) >> Discard(),
        ChannelFilter(8) >> Discard(),
        ChannelFilter(9) >> Discard(),
        ChannelFilter(10) >> Discard(),
        ChannelFilter(11) >> Discard(),
        ChannelFilter(12) >> Discard(),
        ChannelFilter(13) >> Discard(),
        ChannelFilter(14) >> Discard(),
        ChannelFilter(15) >> Discard(),
        ChannelFilter(16) >> Discard(),
    ],
    KeyFilter(notes=[37]) >> Discard(),
    KeyFilter(notes=[38]) >> Discard(),
    KeyFilter(notes=[39]) >> Discard(),
    KeyFilter(notes=[40]) >> Discard(),
    KeyFilter(notes=[41]) >> Discard(),
    KeyFilter(notes=[42]) >> Discard(),
    KeyFilter(notes=[45]) >> Discard(),
    KeyFilter(notes=[44]) >> Discard(),
    KeyFilter(notes=[48]) >> Discard(),
    KeyFilter(notes=[46]) >> Discard(),
    KeyFilter(notes=[49]) >> Discard(),
    KeyFilter(notes=[51]) >> Discard(),
]

# User Set - Writable
# Factory default
pk5_dm_us_mapping = [
    KeyFilter(notes=[64]) >> Discard(),
    KeyFilter(notes=[63]) >> Discard(),
    KeyFilter(notes=[62]) >> Discard(),
    KeyFilter(notes=[61]) >> Discard(),
    KeyFilter(notes=[60]) >> Discard(),
    KeyFilter(notes=[66]) >> Discard(),
    KeyFilter(notes=[65]) >> Discard(),
    KeyFilter(notes=[54]) >> Discard(),
    KeyFilter(notes=[69]) >> Discard(),
    KeyFilter(notes=[68]) >> Discard(),
    KeyFilter(notes=[67]) >> Discard(),
    KeyFilter(notes=[71]) >> Discard(),
    KeyFilter(notes=[73]) >> Discard(),
]

# Control patches

pk5_port = mpk_midi  # PK5 midi out to mkp249 midi in

# PK5 Mode Drums
pk5_dm = PortFilter(pk5_port)

# Factory set
pk5_dm_fs = pk5_dm >> pk5_dm_fs_mapping

# User set
pk5_dm_us = pk5_dm >> pk5_dm_us_mapping
