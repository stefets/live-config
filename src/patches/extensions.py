
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

# VLC player - a singleton is enough
VLC = Call(VlcPlayer())

# MPG123 multiple instances allow me to play sounds in parallal (dmix)
#MPG123_GT10B  = Call(Mp3Player("GT10B"))
MPG123_SD90_A = Call(Mp3Player("SD90"))
MPG123_SD90_B = Call(Mp3Player("SD90"))
MPG123_U192k  = Call(Mp3Player("U192k"))
# Playlist according to current scene, a singleton is enough
MPG123_PLAYLIST = Call(Playlist())
