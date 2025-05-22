import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint
import requests
import re
import spotify
import songdata

if __name__ == "__main__":
    scope = "user-library-read"

    # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    ids = spotify.get_tracks_playlist("5Y9eVQ3u5rBAfL61OmsvDZ")

    # pprint(sp.category_playlists("party"))
    # exit(10)
    for id in ids:
        data = sp.track(id)
        features = songdata.get_audio_features(id)
        data.update(features)
        pprint(data)
        time.sleep(5)
