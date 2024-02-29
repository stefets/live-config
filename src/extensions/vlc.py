"""
    This extension allow controls of VLC player API with mididings
"""


import json
import mididings.constants as _constants

from range_key_dict import RangeKeyDict
from python_vlc_http import HttpVLC, RequestFailed


class VlcPlayer():
    def __init__(self):
        self.vlc = None
        self.configuration = None
        if not self.create():
            return

        # Configure playlist
        self.playlist = []
        pl_name = self.configuration["playlist"]
        playlists = self.vlc.fetch_playlist(pl_name)
        if playlists:
            self.playlist = playlists[0]["children"]
        else:
            print(f"error: Playlist {pl_name} not found")
            self.enabled = False
            return

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        # Allow note 0 to 127
        self.note_range_mapping = RangeKeyDict(
            {
                (0, 36): self.handle_playlist_event,
                (36, 128): self.handle_command_event,
            }
        )
        
        # Single NoteOn mapping
        self.note_mapping = {
            # White keys
            36: self.unassigned,
            38: self.unassigned,
            40: self.unassigned,
            41: self.unassigned,
            43: self.set_repeat_on,
            45: self.set_repeat_off,
            47: self.unassigned,
            # Black keys
            37: self.stop,
            39: self.play,
            42: self.prev_entry,
            44: self.pause,
            46: self.next_entry,
            # WIP
            126: self.toggle_repeat,
            127: self.toggle_loop,
        }

        # Control change mapping
        self.ctrl_range_mapping = RangeKeyDict(
            {
                (0, 2): self.unassigned,
                (7, 8): self.set_volume,
            }
        )
        self.current_entry = 0

    
    def create(self):
        try:
            with open('./extensions/vlc.json') as vlcConfig:
                self.configuration = json.load(vlcConfig)     
            self.vlc = HttpVLC(self.configuration["host"], self.configuration["username"], self.configuration["password"])
        except FileNotFoundError:
            print('error: VLC configuration file not found.')            
        except RequestFailed:
            print("warning: VLC server not available.")
        self.enabled = self.vlc is not None and self.configuration is not None
        
        return self.enabled


    # Invoke
    def __call__(self, ev):
        if self.enabled:
            self.ctrl_range_mapping[ev.data1](
                ev
            ) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)
    

    # Note mapping
    def handle_command_event(self, ev):
        self.note_mapping[ev.data1](ev)


    # Range note mapping for the playlist
    def handle_playlist_event(self, ev):
        if ev.data1 > len(self.playlist) - 1:
            return
        self.current_entry = ev.data1
        candidate = self.playlist[ev.data1]
        try:
            self.vlc.play_playlist_item(candidate["id"])
        except Exception as e:
            print(f"error: {repr(e)}")

    
    def unassigned(self, ev):
        pass

    
    def play(self, ev):
        self.vlc.play() 

    
    def pause(self, ev):
        self.vlc.pause()


    def next_entry(self, ev):
        self.vlc.next_track()


    def prev_entry(self, ev):
        self.vlc.previous_track()


    def on_replay(self, ev):
        pass

    
    def set_volume(self, ev):
        pass

    
    def toggle_loop(self, ev):
        self.vlc.toggle_loop()

    
    def toggle_repeat(self, ev):
        self.vlc.toggle_repeat()

    
    def set_repeat_on(self, ev):
        if not self.vlc.is_on_repeat():
            self.vlc.toggle_repeat()

    
    def set_repeat_off(self, ev):
        if self.vlc.is_on_repeat():
            self.vlc.toggle_repeat()

    
    def stop(self, ev):
        self.vlc.stop()