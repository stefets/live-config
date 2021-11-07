import os
import json
import time
import subprocess
from subprocess import check_call

from colorama import Fore, Back, Style

from range_key_dict import RangeKeyDict

from mpyg321.mpyg321 import MPyg321Player, PlayerStatus

import mididings.constants as _constants
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene

'''
This plugin play mp3 files, it inherits the mpyg321.mpyg321, a mpg123 wrapper

This is a callable object, __call__ is called via the Mididings control patch

Inspiré du clavier 'lanceur de chanson' de l'émission Québecoise 'Tout le monde en parle'
'''


class Mp3Player(MPyg321Player):
    def __init__(self, config):
        super().__init__(config["player"], config["audiodevice"] if config["audiodevice"] else None, True)

        self.playlist = Playlist(config['playlist'], self)

        self.controller = config["controller"]
        self.ksize = self.controller["size"]

        self.clear_screen = lambda: print("\033c\033[3J", end='')

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict({

            (0, 1): self.on_zero,

            (1, 36): self.on_play,
            
            (36, 41): self.navigate_scene,
            (41, 48): self.navigate_player,

            (self.ksize-1, self.ksize): self.playlist.listing,

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
        self.vol = 10
        self.jump_offset = 5
        #

        self.current_entry = 0
        self.spacer = " " * 15

        self.volume(self.vol)

    # Invoker
    def __call__(self, ev):
        self.ctrl_range_mapping[ev.data1](ev) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Logic
    def navigate_scene(self, ev):
        self.note_mapping[ev.data1](ev)

    def navigate_player(self, ev):
        if self.playlist.songs: self.note_mapping[ev.data1](ev)

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

    def on_switch_scene(self, offset):
        index = current_scene() + offset

        # Patch 1 is Initialize, nothing below
        if index <= 1:
            return

        if index > len(scenes()):
            index = 2

        self.clear_screen()

        switch_scene(index)

        time.sleep(0.375) # Offset, wait for Mididings to write its infos to stdout

        self.current_entry = 0
        self.playlist.create(index, self.playlist.filename)


    def next_subscene(self, ev):
        self.on_switch_subscene(1)

    def prev_subscene(self, ev):
        self.on_switch_subscene(-1)

    def on_switch_subscene(self, offset):
        # TODO : Ne pas switcher si il n'y pas de subscene
        self.clear_screen()
        switch_subscene(current_subscene() + offset)
        time.sleep(0.375)
        self.update_display()

    def on_play(self, ev):
        if ev.data1 > self.playlist.length(): return
        self.load_list(ev.data1, self.playlist.filename)
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

    def on_jump(self, offset):
        if not self.status in [PlayerStatus.PLAYING, PlayerStatus.PAUSED]:
            return
        value = "{}{} s".format(offset, self.jump_offset)
        self.jump(value)

    def next_entry(self, ev):
        if self.playlist.length() >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.on_play(ev)

    def set_volume(self, ev):
        self.vol = ev.data2
        self.volume(self.vol)
        self.update_display()

    def set_offset(self, ev):
        mod =  ev.data2 % 2
        if mod == 0:
            self.jump_offset = ev.data2 / 2
            self.update_display()

    def get_current_song(self):
        try:
            if self.current_entry > 0:
                return "{}-{}".format(self.current_entry, self.playlist.songs[self.current_entry-1])
        except IndexError:
            return "IndexError"

    def update_display(self):
        print(" {}VOL={}% | JMP={}s | {}{}{}".format(Fore.RED, 
            self.vol, self.jump_offset, self.get_current_song(), self.spacer, 
            Style.RESET_ALL), end="\r", flush=True)

    '''
    mpyg321 callbacks region
    '''
    def on_any_stop(self):
        if self.status != PlayerStatus.PAUSED:
            self.status = PlayerStatus.STOPPED


class Playlist():
    def __init__(self, config, parent):
        self.songs = []
        self.filename = config['filename']
        self.datasource = config['datasource']
        self.target = config['symlink_target']
        self.builder = config['symlink_builder']
        self.parent = parent

    def create(self, index, configuration):
        context = scenes()[index][0]
        source = self.datasource + context
        try:
            check_call([self.builder, source,  self.target, self.filename])
            self.load()
        except subprocess.CalledProcessError as cpe:
            if cpe.returncode == 3:
                print("Warning: No playlist for " + context)
            else:
                print("Error: " + str(cpe.returncode))
                    

    def length(self):
        return len(self.songs)

    def listing(self, ev=None):
        rank = 0
        for song in self.songs:
            rank += 1
            print("{}-{}".format(rank, song))
        self.parent.update_display()

    def load(self, ev=None):
       self.songs = []
       try:
           with open(self.filename, "r") as pl:
               for number, line in enumerate(pl):
                   title = line.rstrip()
                   self.songs.append(title)
           self.listing()
       except FileNotFoundError:
           pass

