from pathlib import Path

from colorama import Fore, Style

from range_key_dict import RangeKeyDict

from python_vlc_http import HttpVLC

import mididings.constants as _constants
from mididings.engine import (
    scenes,
    current_scene,
    switch_scene,
    current_subscene,
    switch_subscene,
)
from mididings.event import NoteOnEvent


"""
TODO
"""


class VlcPlayer(HttpVLC):
    def __init__(self, config):
        self.enable = config["enable"]
        if not self.enable:
            return
        
        try:
            super().__init__(config["host"], config["username"], config["password"])
        except:
            print("warning: VLC server not available. Plugin disabled")
            self.enable = False
            return

        self.controller = Transport(config["controller"])
        self.playlist = None
        playlists = self.fetch_playlist(config["playlist"])
        if playlists:
            self.playlist = playlists[0]["children"]
        else:
            print("Playlist not found")
            self.enable = False
            return

        #print(self.playlist)
        self.autonext = False

        # Show things in stdout
        self.terminal = Terminal()

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict(
            {
                #(0, 1): self.unassigned,
                (0, self.controller.size): self.on_play,
                #(self.controller.size - 1, self.controller.size): self.on_replay,
            }
        )

        # NoteOn mapping
        self.note_mapping = { }

        # Control change mapping
        self.ctrl_range_mapping = RangeKeyDict(
            {
                (0, 2): self.set_offset,
                (7, 8): self.set_volume,
            }
        )
        self.jump_offset = config["default_jump"]
        self.current_entry = 0

        self.vol = config["default_volume"]  # In %
        #self.volume(self.vol)

        self.current_scene = -1
        self.current_subscene = -1

    # Invoker
    def __call__(self, ev):
        if self.enable:
            print("Vlc call")
            self.ctrl_range_mapping[ev.data1](
                ev
            ) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Unassigned key
    def unassigned(self, ev):
        pass

    def enable_autonext(self, ev):
        self.set_autonext(True)

    def disable_autonext(self, ev):
        self.set_autonext(False)

    def toggle_autonext(self, ev):
        self.set_autonext(not self.autonext)

    def set_autonext(self, value):
        self.autonext = value

    def on_play(self, ev):
        if ev.data1 > len(self.playlist)-1:
            return
        candidate = self.playlist[ev.data1]
        self.play_playlist_item(candidate["id"])

    def on_pause(self, ev):
        if self.status == PlayerStatus.PLAYING:
            self.pause()
        elif self.status == PlayerStatus.PAUSED:
            self.resume()

    def forward(self, ev):
        self.on_jump("+")

    def rewind(self, ev):
        self.on_jump("-")

    def on_jump(self, direction):
        if not self.status in [PlayerStatus.PLAYING, PlayerStatus.PAUSED]:
            return
        value = "{}{} s".format(direction, self.jump_offset)
        self.jump(value)

    def next_entry(self, ev):
        if self.playlist.len() >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.on_play(ev)

    def set_offset(self, ev):
        jump = int(ev.data2 / 2)
        if jump % 2 == 0:
            self.jump_offset = jump

    def get_current_song(self):
        try:
            if self.current_entry > 0:
                return "{}-{}".format(
                    self.current_entry, self.playlist.songs[self.current_entry - 1]
                )
        except IndexError:
            return "IndexError"

    def on_replay(self, ev):
        if self.current_entry > 0:
            self.load_list(self.current_entry, self.playlist.filename)
