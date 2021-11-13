from phue import Bridge
import mididings.constants as _constants

'''
This plugin send commands to a Philips Hue through a Call()
'''
class MididingsHueBase(Bridge):
    def __init__(self, config):
        ip = config["ip"]
        username = config["username"]
        super().__init__(ip, username)
        
        self.zone = config["zone"]
        gid = self.get_group_id_by_name(self.zone)
        self.zone_lights = self.get_group(gid, 'lights')

'''
    Change la scène de la zone
'''
class HueScene(MididingsHueBase):
    def __init__(self, config, scene=None):
        super().__init__(config)
        self.scene = scene

    def __call__(self, ev):
        if self.scene:
            self.run_scene(self.zone, self.scene)


'''
    Shutdown les lumières de la zone
'''
class HueBlackout(MididingsHueBase):
    def __init__(self, config):
        super().__init__(config)

    def __call__(self, ev):
        for light in self.zone_lights:
            light.on = False
