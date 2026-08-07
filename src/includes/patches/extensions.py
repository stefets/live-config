
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

# VLC player - Singleton
VLC_BASE = Filter(NOTEON) >> Call(VlcPlayer())

# Playlist
VLC_PL   = NoteOn(EVENT_DATA1, 0) >> VLC_BASE

# Commands
VLC_STOP  = NoteOn(37, 0) >> VLC_BASE
VLC_PLAY  = NoteOn(39, 0) >> VLC_BASE
VLC_PAUSE = NoteOn(44, 0) >> VLC_BASE
VLC_REPEAT_ON     = NoteOn(43, 0)  >> VLC_BASE
VLC_REPEAT_OFF    = NoteOn(45, 0)  >> VLC_BASE
VLC_TOGGLE_LOOP   = NoteOn(127, 0) >> VLC_BASE
VLC_TOGGLE_REPEAT = NoteOn(126, 0) >> VLC_BASE

# AUDIO_DEVICE multiple instances allow me to play sounds in parallal (dmix)
AUDIO_DEVICE_U192k  = Call(MpvClient("U192k"))
AUDIO_DEVICE_SD90_A = Call(MpvClient("SD90"))
AUDIO_DEVICE_SD90_B = Call(MpvClient("SD90"))
# Playlist according to current scene, a singleton is enough
AUDIO_DEVICE_PLAYLIST = Call(Playlist())
