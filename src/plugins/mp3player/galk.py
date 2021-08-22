import json
import os

from mpyg321.mpyg321 import MPyg321Player, PlayerStatus

import subprocess
from subprocess import check_call

import mididings.constants as _constants
from mididings.engine import *

from range_key_dict import RangeKeyDict


'''
Class Mp3Player

This class is a plugin to play mp3 files with the mpyg321.mpyg321 wrapper for mpg123
when (actually) NOTEON or CTRL event type is received in the __call__ function

Inspiré du clavier 'lanceur de chansons' de l'émission Québecoise 'Tout le monde en parle'
'''


class Mp3Player(MPyg321Player):
    def __init__(self, config):
        super().__init__(config["player"], config["audiodevice"], True)

        self.configuration = config
        self.playlist = self.configuration['playlist']

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict({
            (0, 1): self.on_zero,
            (1, 36): self.on_play,
            (36, 48): self.invoke,
            (48, 49): self.load_playlist,
        })

        # NoteOn mapping
        self.note_mapping = {

            36: self.prev_scene,
            37: self.prev_subscene,
            38: self.home_scene,
            39: self.next_subscene,
            40: self.next_scene,

            # White keys
            41: self.rewind,
            43: self.rewind,
            45: self.forward,
            47: self.forward,

            # Black keys
            42: self.prev_entry,
            44: self.on_pause,
            46: self.next_entry,

        }

        # Control change mapping
        self.ctrl_mapping = {
            1: self.cc_modulation,
            7: self.cc_volume,
        }

        self.current_entry = 0
        self.entry_count = 0

    def __call__(self, ev):
        self.ctrl_mapping[ev.data1](ev) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    #
    # Call the method defined in the note_mapping dict
    #
    def invoke(self, ev):
        self.note_mapping[ev.data1](ev)

    #
    # dict values command functions
    #

    # Note zero (tmp)
    def on_zero(self, ev):
        pass

    # Scenes navigation
    def home_scene(self, ev):
        switch_scene(0)

    def next_scene(self, ev):
        self.on_switch_scene(1)

    def prev_scene(self, ev):
        self.on_switch_scene(-1)

    def on_switch_scene(self, direction):
        index = current_scene() + direction

        # Patch 1 is Initialize, nothing below
        if index <= 1:
            return

        if index > len(scenes()):
            index = 2

        switch_scene(index)

        source = self.configuration['repository'] + scenes()[index][0]
        target = self.configuration['symlink-target']
        check_call([self.configuration['symlink-builder'], source, target])

        self.load_playlist()

    def next_subscene(self, ev):
        switch_subscene(current_subscene() + 1)

    def prev_subscene(self, ev):
        switch_subscene(current_subscene() - 1)

    # MPG123 remote call ------------------------
    def on_play(self, ev):
        self.load_list(ev.data1, self.playlist)
        self.current_entry = ev.data1

    def on_pause(self, ev):
        if self.status == PlayerStatus.PLAYING:
            self.pause()
        elif self.status == PlayerStatus.PAUSED:
            self.resume()

    def forward(self, ev):
        self.jump('+5 s') if ev.data1 == 45 else self.jump('+30 s')

    def rewind(self, ev):
        self.jump('-5 s') if ev.data1 == 43 else self.jump('-30 s')

    def next_entry(self, ev):
        if self.entry_count >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.on_play(ev)

    def cc_volume(self, ev):
        self.volume(ev.data2)

    def cc_modulation(self, ev):
        pass

    def load_playlist(self, ev=None):
        self.entry_count = 0
        with open(self.playlist, "r") as pl:
            for number, line in enumerate(pl):
                self.entry_count = number+1
                print(str(self.entry_count) + " " + line.rstrip())

    '''
    mpyg321 callbacks region
    '''
    def on_any_stop(self):
        # wip
        print("on_any_stop")
