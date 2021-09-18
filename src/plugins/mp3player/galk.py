import json
import os

from mpyg321.mpyg321 import MPyg321Player, PlayerStatus


import subprocess
from subprocess import check_call
from colorama import Fore, Back, Style

import mididings.constants as _constants
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene

from range_key_dict import RangeKeyDict


'''
Class Mp3Player

This class is a plugin to play mp3 files with the mpyg321.mpyg321 wrapper for mpg123
when (actually) NOTEON or CTRL event type is received in the __call__ function

Inspiré du clavier 'lanceur de chanson' de l'émission Québecoise 'Tout le monde en parle'
'''


class Mp3Player(MPyg321Player):
    def __init__(self, config):
        super().__init__(config["player"], config["audiodevice"], True)

        self.configuration = config
        self.playlist = self.configuration['playlist']
        self.ksize = self.configuration["keyboard_size"]

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict({

            (0, 1): self.on_zero,

            (1, 36): self.on_play,
            
            (36, 41): self.navigate_scene,
            (41, 48): self.navigate_player,

            (self.ksize-1, self.ksize): self.list_playlist,

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
        self.ctrl_range_mapping = RangeKeyDict({
            (0, 2): self.set_offset,
            (7, 8): self.set_volume,
        })

        self.current_entry = 0
        self.jump_offset = 0
        self.vol = 0
        self.songs = []
        self.spacer = " " * 15

    def __call__(self, ev):
        self.ctrl_range_mapping[ev.data1](ev) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    #
    # Call the method defined in the mapping dictionnaries
    #
    def navigate_scene(self, ev):
        self.note_mapping[ev.data1](ev)

    def navigate_player(self, ev):
        if self.songs: self.note_mapping[ev.data1](ev)

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

        self.build_playlist(index)


    def next_subscene(self, ev):
        switch_subscene(current_subscene() + 1)

    def prev_subscene(self, ev):
        switch_subscene(current_subscene() - 1)

    def on_play(self, ev):
        self.load_list(ev.data1, self.playlist)
        self.current_entry = ev.data1
        self.update_display()

    def on_pause(self, ev):
        if self.status == PlayerStatus.PLAYING:
            self.pause()
        elif self.status == PlayerStatus.PAUSED:
            self.resume()

    def forward(self, ev):
        self.on_jump("+")

    def rewind(self, ev):
        self.on_jump("-")

    def on_jump(self, sign):
        value = "{}{} s".format(sign, self.jump_offset)
        self.jump(value)

    def next_entry(self, ev):
        if len(self.songs) >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.on_play(ev)

    def set_volume(self, ev):
        self.vol = ev.data2
        self.volume(ev.data2)
        self.update_display()

    def set_offset(self, ev):
        mod =  ev.data2 % 2
        if mod == 0:
            self.jump_offset = ev.data2 / 2
            self.update_display()

    def load_playlist(self, ev=None):
        self.songs = []
        try:
            with open(self.playlist, "r") as pl:
                for number, line in enumerate(pl):
                    title = line.rstrip()
                    self.songs.append(title)
            self.list_playlist()
        except FileNotFoundError:
            pass


    def build_playlist(self, index):
        source = self.configuration['repository'] + scenes()[index][0]
        target = self.configuration['symlink-target']
        check_call([self.configuration['symlink-builder'], source, target])

        self.load_playlist()


    def get_current_song(self):
        if self.current_entry > 0:
            return "{}-{}".format(self.current_entry, self.songs[self.current_entry-1])
        return ""

    def update_display(self):
        print("{}VOL={}% | JMP={}s | {}{}{}".format(Fore.RED, 
            self.vol, self.jump_offset, self.get_current_song(), self.spacer, 
            Style.RESET_ALL), end="\r", flush=True)

    def list_playlist(self, ev=None):
        #print("", end='\n', flush=True)
        index = 0
        for song in self.songs:
            index += 1
            print("{}-{}".format(index, song))
        self.update_display()

    '''
    mpyg321 callbacks region
    '''
    def on_any_stop(self):
        pass
