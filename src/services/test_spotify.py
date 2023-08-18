import spotipy
from spotipy.oauth2 import SpotifyOAuth

artist = '5vjL05W1AhHwmAjGEkrwZi'
track = 'spotify:track:0jYZojrjaEYZqdvrF4RVPZ'

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#instances = sp.devices()
#tablet = next(filter(lambda x : x["name"] == "SM-T500", instances["devices"]))
#print(tablet["id"])

#pl = sp.playlist('3zkrx4OGDerC4vYoKWZ7d7', "tracks")
#print(pl)
#print(pl["tracks"]["items"][0]['track']['id'])

def show_devices():
    # Shows playing devices
    res = sp.devices()
    for d in res["devices"]:
        print(d)


if __name__ == '__main__':
    show_devices()
#    sp.start_playback(
#        device_id="142d6fbf67dabeb7e40c9ac0594b27e8fb59d296",
#        uris=[track])
