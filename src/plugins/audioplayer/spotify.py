'''
    This plugin plays Spotify stream with Spotipy on a given device
'''
import os
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
        self.environ_key = "SPOTIFY_PLAYLIST"

        self.device = None

    def __call__(self, ev):
        # Playlist required
        pl_id = self.getenv(self.environ_key)
        if not pl_id:
            return

        # Device required
        device_name = self.configuration["device"]
        self.device = self.get_device_by_name(device_name)
        if not self.device:
            print(f"Device {0} not connected", device_name)
            return

        self.playlist = self.spotify.playlist(pl_id, "tracks")
        if ev.data1 > self.playlist["tracks"]["total"]:
            return

        index = 0 if ev.data1 == 0 else ev.data1 - 1
        track = self.track.format(self.playlist["tracks"]["items"][index]['track']['id'])
        self.spotify.start_playback(device_id= self.device["id"], uris=[track])


    def get_device_by_name(self, name):
        devices = filter(lambda x : x["name"] == name, self.spotify.devices()["devices"])
        return next(devices, None) if devices else None

    
    def getenv(self, key):
        return os.environ[key] if key in os.environ else None
