import os
import json
from range_key_dict import RangeKeyDict
from colorama import Fore, Style

from extensions.common import (
    Transport, 
    Terminal
)

import mididings.constants as _constants
from mididings.engine import (
    scenes,
    current_scene,
    switch_scene,
    current_subscene,
    switch_subscene,
)
from mididings.event import NoteOnEvent

from plugins.mpv import MpvClient

class MpvAdapter():
    def __init__(self, address: str, playlist):
        if address is None:
            raise ValueError("IPC socket path must be provided")

        self.playlist = playlist
        self.jump_offset = 10
        self.autonext = False

        # The MPV client instance        
        self.mpv = MpvClient(address)

        self.volume = 100
        self.mpv.volume(self.volume)

        # Show things in stdout
        self.terminal = Terminal()
        
        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict(
            {
                (0, 1): self.unassigned,
                (1, 36): self.on_play,
                (36, 41): self.navigate_scene,
                (41, 48): self.navigate_player,
                #(self.controller.size - 1, self.controller.size): self.on_replay,
            }
        )

        # NoteOn mapping
        self.note_mapping = {
            36: self.prev_scene,
            37: self.prev_subscene,
            38: self.home_scene,
            39: self.next_subscene,
            40: self.next_scene,
            # White keys
            41: self.rewind,
            43: self.toggle_autonext,
            45: self.on_toggle_mute,
            47: self.forward,
            # Black keys
            42: self.prev_entry,
            44: self.on_toggle_pause,
            46: self.next_entry,
        }

        # Control change mapping
        self.ctrl_range_mapping = RangeKeyDict(
            {
                (0, 2): self.set_offset,
                (7, 8): self.set_volume,
            }
        )

        self.current_entry = -1

    # call from mididings
    def __call__(self, ev):
        self.ctrl_range_mapping[ev.data1](
            ev
        ) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Logic
    def navigate_scene(self, ev):
        self.note_mapping[ev.data1](ev)

    def navigate_player(self, ev):
        if self.playlist.songs:
            self.note_mapping[ev.data1](ev)

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
        self.update_display()

    # Scenes navigation
    def home_scene(self, ev):
        self.set_scene(1)

    def set_scene(self, index):
        switch_scene(index)

    def next_scene(self, ev):
        self.on_switch_scene(1)

    def prev_scene(self, ev):
        self.on_switch_scene(-1)

    def on_switch_scene(self, offset):
        self.current_scene = index = current_scene() + offset

        # Go to first or last scene
        if index < 1:
            self.current_scene = len(scenes())
        elif index > len(scenes()):
            self.current_scene = 1

        switch_scene(self.current_scene)

        self.current_entry = 0

    def next_subscene(self, ev):
        self.on_switch_subscene(1)

    def prev_subscene(self, ev):
        self.on_switch_subscene(-1)

    def on_switch_subscene(self, offset):
        switch_subscene(current_subscene() + offset)
        self.current_subscene = current_subscene()
        self.current_entry = 0

    def on_play(self, ev):
        index = ev.data1

        if index > len(self.playlist.songs):
            return

        self.mpv.unpause()  # Unpause before loading the file to ensure playback starts immediately
        self.mpv.load(
            str(self.playlist.songs[index - 1])
        )
        self.current_entry = index

    def on_toggle_pause(self, ev):
        """Pause if playing, else resume if paused"""
        self.mpv.toggle_pause()

    def on_toggle_mute(self, ev):
        """Mute or UnMute if playing"""
        self.mpv.toggle_mute()

    def forward(self, ev):
        self.on_seek(self.jump_offset)

    def rewind(self, ev):
        self.on_seek(-self.jump_offset)

    def on_seek(self, offset):
        self.mpv.seek(offset)

    def next_entry(self, ev):
        if self.playlist.len() >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.on_play(ev)

    def set_volume(self, ev):
        if ev.data2 % 2 != 0:
            return
        self.volume = ev.data2
        self.mpv.volume(self.volume)
        self.update_display()


    def set_offset(self, ev):
        jump = int(ev.data2 / 2)
        if jump % 2 == 0:
            self.jump_offset = jump
            self.update_display()

    def get_current_song(self):
        try:
            if self.current_entry > 0:
                return "{}-{}".format(
                    self.current_entry, self.playlist.songs[self.current_entry - 1]
                )
        except IndexError:
            return "IndexError"

    def update_display(self):
        print(
            " {}VOL={}% | JMP={}s | AN={} | {}{}{}".format(
                Fore.RED,
                self.volume,
                self.jump_offset,
                self.autonext,
                self.get_current_song(),
                self.terminal.spacer,
                Style.RESET_ALL,
            ),
            end="\r",
            flush=True,
        )

    def on_replay(self, ev):
        if self.current_entry > 0:
            # TODO: Replay the current entry
            pass
            #self.mpv.load_list(self.current_entry, self.playlist.filename)        