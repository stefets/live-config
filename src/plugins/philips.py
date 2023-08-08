'''
    Plugin qui contrôle le Philips Hue via Call()
    La valeur du CC 3 permet de définir la transition
'''
import os
from phue import Bridge
import mididings.constants as _constants

class HueBase(Bridge):
    def __init__(self, zone_id):
        super().__init__(os.environ["HUE_IP"], os.environ["HUE_USERNAME"])

        self.zones = [1, 2, 4]
        
        self.enable = True
        self.cc_transition =  os.environ["HUE_CC_TRANSITION"]
        
        if zone_id not in self.zones:
            print(f"HuePlugin: Zone {zone_id} not defined")
            self.enable = False
            return
        
        self.zone_id = zone_id
        group = self.get_group(self.zone_id)
        
        self.zone = group["name"]

'''
    Charge la scène de la zone
'''
class HueScene(HueBase):
    def __init__(self, zone_id, scene, transition=4):
        super().__init__(zone_id)

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
    def __init__(self, zone_id):
        super().__init__(zone_id)
        self.zone_lights = self.get_group(self.zone_id, 'lights')

    def __call__(self, ev):
        if self.enable:
            for light_id in [int(i) for i in self.zone_lights]:
                self[light_id].on = False
