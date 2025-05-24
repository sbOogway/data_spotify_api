import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint
import spotify
import songdata
from pymongo import MongoClient, errors
import os
import sys
import logging
import requests


import logging.config

logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'log/scrape_playlist.log',
            'level': 'INFO',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}

logging.config.dictConfig(logging_config)


if __name__ == "__main__":
    try:
        playlist_id = sys.argv[1] 
        # playlist_id = "19PgP2QSGPcm6Ve8VhbtpG"


        scope = "user-library-read"

        client = MongoClient(os.getenv("DB_HOST", "mongodb://localhost:27017/"))
        songs = client["guess_tha_song"]["songs"]
        playlists = client["guess_tha_song"]["playlists"]

        songs.create_index("id", unique=True)
        playlists.create_index("id", unique=True)

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        if playlists.find_one({"id": playlist_id}) != None:
            logging.warning(f"playlist already scraped {playlist_id}")
            exit(1)

        logging.info(f"starting scraping playlist {playlist_id}")

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
            try:
                features = songdata.get_audio_features(id)
            except requests.exceptions.HTTPError:
                logging.error(f"error songdata {id}")
                continue
            data.update(features)
            data.update(previews)
            # del data["album"]["available_markets"]
            # del data["available_markets"]
            # pprint(data)
            # print("="*100)
            
            try:
                songs.insert_one(data)
                logging.debug(f"song added to database {id}")
            except errors.DuplicateKeyError:
                logging.warning(f"song already scraped {id}")
                pass
            
            time.sleep(10)
        

        playlist = sp.playlist(playlist_id)
        # try:
        playlists.insert_one(playlist)
        logging.info(f"finished scraping playlist {playlist_id}")
        # except errors.DuplicateKeyError:
            # pass

    except KeyboardInterrupt:
        raise SystemExit()