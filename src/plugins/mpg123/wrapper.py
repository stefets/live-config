import json
import os
from subprocess import Popen, PIPE, check_call

import mididings.constants as _constants
from mididings.engine import *


# Class MPG123
#
# This class control mpg123 in remote mode with a keyboard (or any other midi devices of your choice)
# when (actually) NOTEON or CTRL event type is received in the __call__ function
#
# It's inspired of the 'song trigger keyboard' of the Quebec TV Show 'Tout le monde en parle'
#
# Limitations :
# - Can't get the number of entry in playlist


class MPG123:
    def __init__(self):
        hostname = os.uname()[1]
        file = os.getcwd() + '/plugins/mpg123/config.json'
        with open(file) as json_file:
            self.configuration = json.load(json_file)

        # MPG123 process
        self.process = Popen(['mpg123', '--audiodevice', self.configuration[hostname]['hw'], '--quiet', '--remote'],
                             stdin=PIPE)
        self.write('silence')

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict({
            (0, 1): self.not_implemented,
            (1, 36): self.play,
            (36, 48): self.invoke,
            (48, 49): self.list_files,
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
            44: self.pause,
            46: self.next_entry,

        }

        # Control change mapping
        self.ctrl_mapping = {
            1: self.cc_modulation,
            7: self.cc_volume,
        }

        self.current_entry = 0

    def __del__(self):
        self.process.terminate()

    def __call__(self, ev):
        self.ctrl_mapping[ev.data1](ev) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Write a command to the mpg123 process
    def write(self, cmd):
        self.process.stdin.write(cmd + '\n')

    #
    # Call the method defined in the note_mapping dict
    #
    def invoke(self, ev):
        self.note_mapping[ev.data1](ev)

    #
    # dict values command functions
    #
    def not_implemented(self, ev):
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
        if index > len(scenes()):
            index = 2
        switch_scene(index)
        # Patch 1 is Initialize, nothing below
        if index <= 1:
            return

        source = self.configuration['albums'] + scenes()[index][0]
        target = self.configuration['symlink-target']
        check_call([self.configuration['symlink-builder'], source, target])

    def next_subscene(self, ev):
        switch_subscene(current_subscene() + 1)

    def prev_subscene(self, ev):
        switch_subscene(current_subscene() - 1)

    # MPG123 remote call ------------------------
    def play(self, ev):
        self.write('ll {} {}/playlist'.format(ev.data1, self.configuration['symlink-target']))
        self.current_entry = ev.data1

    def pause(self, ev):
        self.write('p')

    def forward(self, ev):
        self.jump('+5 s') if ev.data1 == 45 else self.jump('+30 s')

    def rewind(self, ev):
        self.jump('-5 s') if ev.data1 == 43 else self.jump('-30 s')

    def jump(self, offset):
        self.write('j ' + offset)

    def next_entry(self, ev):
        ev.data1 = self.current_entry + 1
        self.play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
            self.play(ev)

    def cc_volume(self, ev):
        self.write('v {}'.format(ev.data2))

    def cc_modulation(self, ev):
        pass

    def list_files(self, ev):
        self.write('ll {} {}/playlist'.format(-1, self.configuration['symlink-target']))


#
# Borrowed here : https://github.com/albertmenglongli/range-key-dict/blob/master/range_key_dict/range_key_dict.py
#


class RangeKeyDict:
    def __init__(self, my_dict):
        # !any(!A or !B) is faster than all(A and B)
        assert not any(map(lambda x: not isinstance(x, tuple) or len(x) != 2 or x[0] > x[1], my_dict))

        def lte(bound):
            return lambda x: bound <= x

        def gt(bound):
            return lambda x: x < bound

        # generate the inner dict with tuple key like (lambda x: 0 <= x, lambda x: x < 100)
        self._my_dict = {(lte(k[0]), gt(k[1])): v for k, v in my_dict.items()}

    def __getitem__(self, number):
        from functools import reduce
        _my_dict = self._my_dict
        try:
            result = next((_my_dict[key] for key in _my_dict if list(reduce(lambda s, f: filter(f, s), key, [number]))))
        except StopIteration:
            raise KeyError(number)
        return result

    def get(self, number, default=None):
        try:
            return self.__getitem__(number)
        except KeyError:
            return default
