'''
    Handle the LED state of an AKAI MIDI Mix controller
    
    The MIDI Mix switch must be keep to the default values and channel 1
    Note 1 = MUTE 1
    Note 2 = SOLO 1
    Note 3 = ARM/REC 1
    Note 4 = MUTE 2 
    Etc...
'''


class MidiMix():
    def __init__(self):
        self.switches = []


    def __call__(self, ev):
        return self.toggle_led(ev)
        

    def toggle_led(self, ev):
        candidate = next((switch for switch in self.switches if switch.id == ev.data1), False)
        if not candidate:
            candidate = Switch(ev.data1)
            self.switches.append(candidate)

        candidate.led.open = not candidate.led.open
        ev.data2 = 0 if not candidate.led.open else 127

        return [ev]


class Switch():
    ''' Physical candidate '''
    def __init__(self, id):
        self.id = id
        self.led = Led()


class Led():
    ''' Led for a candidate '''
    def __init__(self):
        self.open = False