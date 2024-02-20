
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

# VLC player - Singleton
VLC_BASE = Filter(NOTEON) >> Call(VlcPlayer())
# Playlist
VLC_PL   = NoteOn(EVENT_DATA1, 0) >> VLC_BASE
# Commands
VLC_STOP = NoteOn(46, 0)    >> VLC_BASE
VLC_REPEAT_ON  = NoteOn(47, 0) >> VLC_BASE
VLC_REPEAT_OFF = NoteOn(48, 0) >> VLC_BASE

# MPG123 multiple instances allow me to play sounds in parallal (dmix)
#MPG123_GT10B  = Call(Mp3Player("GT10B"))
#MPG123_U192k  = Call(Mp3Player("U192k"))
MPG123_SD90_A = Call(Mp3Player("SD90"))
MPG123_SD90_B = Call(Mp3Player("SD90"))
# Playlist according to current scene, a singleton is enough
MPG123_PLAYLIST = Call(Playlist())
