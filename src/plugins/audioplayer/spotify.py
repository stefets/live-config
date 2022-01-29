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

        self.device_name = self.configuration["device"]
        self.device = self.get_device_by_name(self.device_name)

    def __call__(self, ev):

        # Device required
        if not self.device:
            print(f"Device {0} not connected", self.device_name)
            return

        if ev.type == _constants.CTRL:
            if ev.data1 == 7:
                self.volume(ev)
            elif ev.data1 == 1:
                pass

            return
        

        # Playlist required
        pl_id = self.getenv(self.environ_key)
        if not pl_id:
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

    
    def volume(self, ev):
        ''' Instead of MIDI, the Spotify API is not real time - set the volume on 5% step to reduce payload '''
        if ev.data2 % 5 == 0:
            self.spotify.volume(ev.data2, self.device["id"])


    def getenv(self, key):
        ''' Get the selected playlist from envionment '''
        return os.environ[key] if key in os.environ else None
