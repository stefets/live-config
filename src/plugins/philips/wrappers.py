from phue import Bridge
import mididings.constants as _constants

class Hue():
    def __init__(self, config):
        self.bridge = Bridge(config["ip"], config["username"])

    def __call__(self, ev):
        self.bridge.set_light('Studio 2', 'on', True) if ev.type == _constants.NOTEON else self.bridge.set_light('Studio 2', 'on', False)

