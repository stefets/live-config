import json
import mididings.constants as _constants
from mididings.event import NoteOnEvent

from .common import (
    Transport, 
    Terminal
)

from range_key_dict import RangeKeyDict
from python_vlc_http import HttpVLC
'''
from mididings.engine import (
    scenes,
    current_scene,
    switch_scene,
    current_subscene,
    switch_subscene,
)
'''


"""
This class allow the control of the VLC player API with a mididings callable object
"""


class VlcPlayer(HttpVLC):
    def __init__(self):
        with open('./services/vlc.json') as json_file:
            config = json.load(json_file)       

        if not config["enable"]:
            return
        
        self.enable = True

        try:
            super().__init__(config["host"], config["username"], config["password"])
        except:
            print("error: VLC server not available. Plugin disabled")
            self.enable = False
            return

        # Configure playlist
        self.playlist = []
        pl_name = config["playlist"]
        playlists = self.fetch_playlist(pl_name)
        if playlists:
            self.playlist = playlists[0]["children"]
        else:
            print(f"error: Playlist {pl_name} not found")
            self.enable = False
            return

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        # Allow note 0 to 127
        self.note_range_mapping = RangeKeyDict(
            {
                (0, 128): self.on_play,
            }
        )

        # NoteOn mapping
        self.note_mapping = { }

        # Control change mapping
        self.ctrl_range_mapping = RangeKeyDict(
            {
                (0, 2): self.unassigned,
                (7, 8): self.set_volume,
            }
        )
        self.current_entry = 0


    # Invoke
    def __call__(self, ev):
        if self.enable:
            self.ctrl_range_mapping[ev.data1](
                ev
            ) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)


    def on_play(self, ev):
        if ev.data1 > len(self.playlist) - 1:
            return
        self.current_entry = ev.data1
        candidate = self.playlist[ev.data1]
        try:
            self.play_playlist_item(candidate["id"])
        except Exception as e:
            print(f"error: {repr(e)}")

    
    def unassigned(self, ev):
        pass


    def on_pause(self, ev):
        pass


    def next_entry(self, ev):
        pass


    def prev_entry(self, ev):
        pass


    def on_replay(self, ev):
        pass

    def set_volume(self, ev):
        pass
