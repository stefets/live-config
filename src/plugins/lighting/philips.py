from phue import Bridge
import mididings.constants as _constants

'''
This plugin send commands to a Philips Hue through a Call()
'''
class Hue(Bridge):
    def __init__(self, config, scene=None):
        super().__init__(config["ip"], config["username"])
        self.group = config["zone"]
        self.scene = scene

    def __call__(self, ev):
        if self.group and self.scene:
            self.run_scene(self.group, self.scene)

