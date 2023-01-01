'''
    This plugin plays Spotify stream with Spotipy on a given device
'''
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

import mididings.constants as _constants
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene


class SpotifyPlayer(object):
    def __init__(self, config) -> None:
        self.configuration = config
        if not self.configuration["enable"]:
            return

        scope = "user-read-playback-state,user-modify-playback-state"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        ''' Track object '''
        self.track_template = "spotify:track:{}"    

        ''' Track Id '''
        self.track = None

        self.playlist = None
        self.environ_key = "SPOTIFY_PLAYLIST"

        self.device = None

        ''' Get first available device '''
        self.device = SpotifyDevice(self.spotify.devices()["devices"], self.configuration["devices"])

        self.position = 0
        self.is_playing = False

    def __call__(self, ev):
        # Device required
        if not self.device:
            print("No device connected")
            return

        if ev.type == _constants.CTRL:
            if ev.data1 == 7:
                self.volume(ev)
            elif ev.data1 == 1:
                pass
            elif ev.data1 == 44:
                self.pause() if ev.data2 == 127 else self.resume()

            return
        
        # Playlist required
        pl_id = self.getenv(self.environ_key)
        if not pl_id:
            print("No playlist in current context")
            return

        self.playlist = self.spotify.playlist(pl_id, "tracks")
        if ev.data1 > self.playlist["tracks"]["total"]:
            return

        index = 0 if ev.data1 == 0 else ev.data1 - 1
        self.track = self.track_template.format(self.playlist["tracks"]["items"][index]['track']['id'])
        self.play()


    def play(self, resume=False):
        if self.device and self.track:
            pms = self.position if resume else 0
            try:
                self.spotify.start_playback(device_id=self.device.id, uris=[self.track], position_ms=pms)
            except SpotifyException:
                ''' The device is gone, try to get a new one '''
                self.device = SpotifyDevice(self.spotify.devices()["devices"], self.configuration["devices"])


    
    def pause(self) -> None:
        ''' Pause and keep current position '''
        self.spotify.pause_playback(self.device.id)
        cp = self.spotify.current_playback()
        self.position = cp["progress_ms"]
        
    
    def resume(self) -> None:
        ''' Resume play '''
        self.play(True)

    
    def volume(self, ev):
        ''' Instead of MIDI, the Spotify API is not real time - set the volume on 5% step to reduce latency '''
        if self.device.volume_enable and ev.data2 % 5 == 0:
            try:
                self.spotify.volume(ev.data2, self.device.id)
            except SpotifyException:
                ''' Player command failed: Cannot control device volume, reason: VOLUME_CONTROL_DISALLOW '''
                self.device.volume_enable = False


    def getenv(self, key):
        ''' Get the selected playlist from envionment '''
        return os.environ[key] if key in os.environ else None


class SpotifyDevice():
    def __init__(self, devices, allowed) -> None:
        self.id = None
        self.name = None
        self.instance = None
        self.connected_devices = devices
        for name in allowed:
            self.instance = self.get_device_by_name(name)
            if self.instance:
                self.name = name
                self.id = self.instance["id"]
                break
    
        self.volume_enable = True

    
    def get_device_by_name(self, name) -> str:
        candidates = filter(lambda element : element["name"] == name, self.connected_devices)
        return next(candidates, None) if candidates else None
