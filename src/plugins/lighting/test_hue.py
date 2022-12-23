'''
    Plugin qui contrôle le Philips Hue via Call()
    La valeur du CC 3 permet de définir la transition
'''
import os
from phue import Bridge

# Environment
from dotenv import load_dotenv
load_dotenv()


class HueBase(Bridge):
    def __init__(self):
        super().__init__(os.environ["HUE_IP"], os.environ["HUE_USERNAME"])
        zones = ["Cuisine", "Salle de musique"]
        for zone in zones:
            print(self.get_group_id_by_name(zone))

        zones = [2,4]
        for zone in zones:
            print(self.get_group(zone))
        

    def shutdown(zone):
        zone_lights = self.get_group(self.zone_id, 'lights')
        for light_id in [int(i) for i in zone_lights]:
            print(light_id)
            self[light_id].on = False


base = HueBase()

