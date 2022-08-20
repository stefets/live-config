import subprocess
from subprocess import check_call

from colorama import Fore, Style
from .frontend import Terminal
from .controller import Transport

from range_key_dict import RangeKeyDict

from mpyg321.MPyg123Player import MPyg123Player
from mpyg321.consts import PlayerStatus

import mididings.constants as _constants
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene
from mididings.event import NoteOnEvent

import alsaaudio

'''
This plugin plays mp3 files, it inherits the mpyg321.mpyg321, a mpg123 wrapper

This is a callable object, __call__ is called via the control patch (src/control.py)

Inspiré du clavier 'lanceur de chanson' de l'émission Québecoise 'Tout le monde en parle'
'''


class Mp3Player(MPyg123Player):
    def __init__(self, config):

        self.enable = config["enable"]
        if not self.enable:
            return

        # Check if card is in my available_devices (is connected) or it will use the onboard card
        card = None
        cards = alsaaudio.cards()

        for device in config["available_devices"]:
            if device in cards:
                card = f"hw:{cards.index(device)},0"
                break

        super().__init__(config["player"], card if card else None, True)

        # For mpg123 >= v1.3*.*
        self.mpg_outs.append(
            {
                "mpg_code" : "@P 3",
                "action" : "end_of_song",
                "description" : "Player has reached the end of the song."
            })

        self.controller = Transport(config["controller"])
        self.playlist = Playlist(config['playlist'])
        self.autonext = False

        # Show things in stdout
        self.terminal = Terminal()

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict({

            (0, 1): self.toggle_autonext,

            (1, 36): self.on_play,
            
            (36, 41): self.navigate_scene,
            (41, 48): self.navigate_player,

            (self.controller.size-1, self.controller.size): self.unassigned,

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
        self.jump_offset = 5
        self.current_entry = 0

        self.vol = 75   # In %
        self.volume(self.vol)

        self.current_scene = -1
        self.current_subscene = -1
        
    # Invoker
    def __call__(self, ev):
        if self.enable:
            self.ctrl_range_mapping[ev.data1](ev) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Logic
    def navigate_scene(self, ev):
        self.note_mapping[ev.data1](ev)

    def navigate_player(self, ev):

        if self.playlist.songs: 
            self.note_mapping[ev.data1](ev)

    # Unassigned key
    def unassigned(self, ev):
        pass

    def toggle_autonext(self, ev):
        self.autonext = not self.autonext
        self.update_display()

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

        switch_scene(index)
        self.current_scene = index

        self.current_entry = 0
        self.playlist.load_from_file()

    def next_subscene(self, ev):
        self.on_switch_subscene(1)

    def prev_subscene(self, ev):
        self.on_switch_subscene(-1)

    def on_switch_subscene(self, offset):
        switch_subscene(current_subscene() + offset)
        self.current_subscene = current_subscene()
        self.current_entry = 0
        self.playlist.load_from_file()

    def on_play(self, ev):
        if self.current_entry == 0 or self.current_scene != current_scene() or self.current_subscene != current_subscene():
            ''' The context has externally been changed '''
            ''' Refresh the playlist according the current scene/subscene '''
            self.stop()
            self.current_scene = current_scene()
            self.current_subscene = current_subscene()
            self.playlist.load_from_file()
        if ev.data1 > self.playlist.length(): 
            return
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

    def on_jump(self, direction):
        if not self.status in [PlayerStatus.PLAYING, PlayerStatus.PAUSED]:
            return
        value = "{}{} s".format(direction, self.jump_offset)
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
        jump = int(ev.data2 / 2)
        if jump % 2 == 0:
            self.jump_offset = jump
            self.update_display()

    def get_current_song(self):
        try:
            if self.current_entry > 0:
                return "{}-{}".format(self.current_entry, self.playlist.songs[self.current_entry-1])
        except IndexError:
            return "IndexError"

    def update_display(self):
        print(" {}VOL={}% | JMP={}s | AN={} | {}{}{}".format(Fore.RED, 
            self.vol, self.jump_offset, self.autonext, self.get_current_song(), self.terminal.spacer, 
            Style.RESET_ALL), end="\r", flush=True)

    '''
    mpyg321 callbacks
    '''
    def on_any_stop(self):
        if self.status != PlayerStatus.PAUSED:
            self.status = PlayerStatus.STOPPED

    def on_music_end(self):
        if self.autonext:
            # Load next entry in playlist with a dummy MIDI event
            ev = NoteOnEvent(self.controller.port, self.controller.channel, 0, 0)
            self.next_entry(ev)


class Playlist():
    def __init__(self, config):
        self.songs = []
        self.filename = None
        self.datasource = config['datasource']
        self.target = config['symlink_target']
        self.builder = config['symlink_builder']
        self.terminal = Terminal()

    def __call__(self, ev):
        self.create()

    def create(self):
        if self.has_subscene():
            filedirname = self.get_subscene_name()
            source = self.datasource + self.get_scene_name() + "/" + self.get_subscene_name()
        else:
            filedirname =  self.get_scene_name()
            source = self.datasource + self.get_scene_name()
        
        full_filename = self.target + filedirname + ".txt"

        try:
            check_call([self.builder, source,  self.target, full_filename])
            self.load_from_file(full_filename)
        except subprocess.CalledProcessError as cpe:
            if cpe.returncode == 3:
                print("Warning: No playlist for " + self.get_scene_name())
            else:
                print("Error: " + str(cpe.returncode))
                    
    def length(self):
        return len(self.songs)

    def has_subscene(self):
        return scenes()[current_scene()][1]

    def load_from_file(self, filename=None):
        self.songs = []
        if not filename:
            fname = self.get_subscene_name() if self.has_subscene() else self.get_scene_name()
            filename = self.target + fname + ".txt"
        
        self.filename = filename
        try:
            with open(self.filename, "r") as pl:
                for number, line in enumerate(pl):
                    title = line.rstrip()
                    self.songs.append(title)
            self.listing()
        except FileNotFoundError:
            pass

    def get_scene_name(self):
        return scenes()[current_scene()][0]

    def get_subscene_name(self):
        return scenes()[current_scene()][1][current_subscene()-1] if self.has_subscene() else None

    def listing(self):
        self.terminal.write_line(self.get_scene_name())
        rank = 0
        for song in self.songs:
            rank += 1
            self.terminal.write_line2(str(rank).zfill(2), song)
