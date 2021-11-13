from phue import Bridge
import mididings.constants as _constants

class Hue():
    def __init__(self, config, scene=None):
        self.bridge = Bridge(config["ip"], config["username"])
        self.context = config["zone"]
        self.scene = scene

    def __call__(self, ev):
        if self.scene:
            self.bridge.run_scene(self.context, self.scene)

