'''
    Plugin qui contrôle le Philips Hue via Call()
    La valeur du CC 3 permet de définir la transition
'''
import os
from phue import Bridge
import mididings.constants as _constants

class HueBase(Bridge):
    def __init__(self, config):
        super().__init__(os.environ["HUE_IP"], os.environ["HUE_USERNAME"])
        
        self.enable = config["enable"]
        self.zone = config["zone"]
        self.cc_transition =  config["cc_transition"]
        self.zone_id = self.get_group_id_by_name(self.zone)


'''
    Charge la scène de la zone
'''
class HueScene(HueBase):
    def __init__(self, config, scene, transition=4):
        super().__init__(config)

        self.scene = scene
        self.transition = transition

    def __call__(self, ev):
        if self.enable:
            transition = ev.data2 if ev.type == _constants.CTRL and ev.data1 == self.cc_transition else self.transition
            self.run_scene(self.zone, self.scene, transition)


'''
    Shutdown les lumières de la zone
'''
class HueBlackout(HueBase):
    def __init__(self, config):
        super().__init__(config)
        self.zone_lights = self.get_group(self.zone_id, 'lights')

    def __call__(self, ev):
        if self.enable:
            for light_id in [int(i) for i in self.zone_lights]:
                self[light_id].on = False
