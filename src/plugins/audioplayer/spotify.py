'''
    This plugin plays Spotify stream with Spotipy on a given device
'''
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import mididings.constants as _constants
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene


class SpotifyPlayer(object):
    def __init__(self, config) -> None:
        self.configuration = config
        if not self.configuration["enable"]:
            return

        scope = "user-read-playback-state,user-modify-playback-state"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


        self.track = "spotify:track:{}"
        self.playlist = None

    def __call__(self, ev):
        if not self.get_scene_name() == "Spotify":
            return

        print("SpotifyCallback")
        
        device = self.get_device_by_name(self.configuration["device"])
        if not device:
            print("Device not connected")
            return

        pl_name = self.get_subscene_name()
        if not pl_name in self.configuration:
            return

        pl_id = self.configuration[pl_name]
        self.playlist = self.spotify.playlist(pl_id, "tracks")
        if ev.data1 > self.playlist["tracks"]["total"]:
            return

        index = 0 if ev.data1 == 0 else ev.data1 - 1
        track = self.track.format(self.playlist["tracks"]["items"][index]['track']['id'])
        self.spotify.start_playback(device_id= device["id"], uris=[track])


    def get_device_by_name(self, name):
        self.devices = filter(lambda x : x["name"] == name, self.spotify.devices()["devices"])
        return next(self.devices, None) if self.devices else None

    def get_scene_name(self):
        return scenes()[current_scene()][0]

    def has_subscene(self):
        return scenes()[current_scene()][1]

    def get_subscene_name(self):
        return scenes()[current_scene()][1][current_subscene()-1] if self.has_subscene() else None
