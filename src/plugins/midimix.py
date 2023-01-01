'''
    Handle the LED state of an AKAI MIDI Mix controller
    
    This class should be use ONCE in the run()/control patch
    
    The MIDI Mix switch note value must be keep to the default value (1 to 26)
    The input channel can be other than 1 for flexibility but is forced to 1 output
    Note 1 = MUTE 1
    Note 2 = SOLO 1
    Note 3 = ARM/REC 1
    Note 4 = MUTE 2 
    Etc...
'''
from mididings.event import NoteOnEvent


class MidiMix():
    ''' AKAI MIDI Mix MIXER '''
    def __init__(self):
        self.switches = []
        for index in range(1, 27):
            self.switches.append(Switch(index))


    def __call__(self, ev):
        return self.toggle(ev)
        

    def toggle(self, ev):
        candidate = next((switch for switch in self.switches if switch.id == ev.data1), False)
        if not candidate:
            return ev

        candidate.led.open = not candidate.led.open
        ev.data2 = 0 if not candidate.led.open else 127

        ev.channel = 1      # Led work only on channel 1

        return [ev]         # Return the event for the next unit(s) in chain


class Switch():
    ''' Physical switch '''
    def __init__(self, id):
        self.id = id
        self.led = Led()


class Led():
    ''' Led status for a switch '''
    def __init__(self):
        self.open = False


''' 
    This class open or close the LED on the MIDI Mix
    It must be use AFTER a Process(MidiMix()) in a chain
    Don't use the class if Process(MidiMix()) is at the end of a chain
    Usage in mod_control.py
'''
class MidiMixLed():
    def __init__(self):
        pass

    def __call__(self, ev):
        return NoteOnEvent(ev.port, ev.channel, ev.data1, ev.data2)