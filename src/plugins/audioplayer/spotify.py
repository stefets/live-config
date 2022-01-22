'''
    This plugin plays Spotify stream with Spotipy on a given device
'''
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlayer(object):
    def __init__(self, config) -> None:
        self.enable = config["enable"]
        if not self.enable:
            return

        scope = "user-read-playback-state,user-modify-playback-state"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        self.artist = "5vjL05W1AhHwmAjGEkrwZi"
        self.track = "spotify:track:0jYZojrjaEYZqdvrF4RVPZ"
        self.device = "142d6fbf67dabeb7e40c9ac0594b27e8fb59d296"

    def __call__(self, ev):
        self.spotify.start_playback(device_id=self.device, uris=[self.track])