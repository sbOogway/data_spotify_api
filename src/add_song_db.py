import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint
import spotify
import songdata
from pymongo import MongoClient, errors
import os
import sys

if __name__ == "__main__":
    scope = "user-library-read"

    client = MongoClient(os.environ["DB_HOST"])
    songs = client["guess_tha_song"]["songs"]
    songs.create_index("id", unique=True)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # ids = spotify.get_tracks_playlist("5Y9eVQ3u5rBAfL61OmsvDZ")

    playlist_id = "19PgP2QSGPcm6Ve8VhbtpG"

    batch = 100
    pl = sp.playlist_items(playlist_id, limit=batch)

    pl_length = pl["total"]
    items: list = pl["items"]
    
    song_reccate = batch

    while song_reccate < pl_length:
        pl = sp.playlist_items(playlist_id, limit=batch, offset=song_reccate )
        song_reccate += batch
        items += pl["items"]
    
    for track in items:
        id = track["track"]["uri"].split(":")[-1]
        previews = spotify.get_preview(id)
        data = sp.track(id)
        features = songdata.get_audio_features(id)
        data.update(features)
        data.update(previews)
        # del data["album"]["available_markets"]
        # del data["available_markets"]
        # pprint(data)
        # print("="*100)
        
        try:
            songs.insert_one(data)
        except errors.DuplicateKeyError:
            pass
        
        time.sleep(10)
