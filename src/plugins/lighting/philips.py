'''
    This plugin send commands to a Philips Hue through a Call()
'''
from phue import Bridge

class HueBase(Bridge):
    def __init__(self, config):
        super().__init__(config["ip"], config["username"])
        
        self.zone = config["zone"]
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
        if self.scene:
            self.run_scene(self.zone, self.scene, self.transition)


'''
    Shutdown les lumières de la zone
'''
class HueBlackout(HueBase):
    def __init__(self, config):
        super().__init__(config)
        self.zone_lights = self.get_group(self.zone_id, 'lights')

    def __call__(self, ev):
        for light_id in [int(i) for i in self.zone_lights]:
            self[light_id].on = False
