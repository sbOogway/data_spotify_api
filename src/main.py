import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint
import requests
import re



scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# print(sp.artist("spotify:artist:3jOstUTkEu2JkjvRdBA5Gu"))

t = sp.current_user_saved_tracks(limit=40)


pprint(t)