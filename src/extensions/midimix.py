'''
    Handle the state of an AKAI MIDI Mix controller
    Note 1 = MUTE 1
    Note 2 = SOLO 1
    Note 3 = ARM/REC 1
'''
from mididings.event import NoteOnEvent
import mididings.constants as _constants


class MidiMix():
    def __init__(self):
        #self.knobs = []
        #self.cursors = []
        self.switches = []
        for index in range(1, 28):
            self.switches.append(Switch(index))

    def __call__(self, ev):
        return self.on_call(ev)
        
    def on_call(self, ev):
        switch = next((sw for sw in self.switches if sw.id == ev.data1), False)
        return switch.toggle(ev)


class Switch():
    def __init__(self, id):
        self.id = id
        self.on = False

    def toggle(self, ev):
        self.on = not self.on
        ev.data2 = 0 if not self.on else 127
        return ev

class MidiMixLed():
    def __init__(self):
        pass

    def __call__(self, ev):
        return NoteOnEvent(ev.port, 1, ev.data1, ev.data2)
'''
class Knob():
    def __init__(self, id):
        self.id = id
        self.value = -1

    def value(self, ev):
        self.value = ev.data2


class Cursor():
    def __init__(self, id, master = False):
        self.id = id
        self.value = -1
        self.master = master 

    def value(self, ev):
        self.value = ev.data2    
'''