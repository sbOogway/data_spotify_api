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

        songs_db = songs.find({}, {"id": 1, "_id": 0})

        songs_db = list(map(lambda x : list(x.values())[0], songs_db))

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        if playlists.find_one({"id": playlist_id}) != None:
            logging.info(f"playlist already scraped {playlist_id}")
            exit(1)

        logging.info(f"starting scraping playlist {playlist_id}")

        batch = 100
        try:
            pl = sp.playlist_items(playlist_id, limit=batch)
        except spotipy.exceptions.SpotifyException:
            playlists.insert_one({"id": playlist_id})
            logging.info(f"finished scraping playlist {playlist_id}")
            exit(1)

        pl_length = pl["total"]        
        items: list = pl["items"]
        logging.debug(f"number of songs in {playlist_id} - {pl_length}")

        
        
        song_reccate = batch

        while song_reccate < pl_length:
            pl = sp.playlist_items(playlist_id, limit=batch, offset=song_reccate )
            song_reccate += batch
            items += pl["items"]
        
        ids = []
        
        for track in items:
            id = track["track"]["uri"].split(":")[-1]
            ids.append(id)

        intersection = set(ids) & set(songs_db)
        ids = list(set(ids) - intersection)
        # exit(10)

        for index, id in enumerate(ids):
            try:
                previews = spotify.get_preview(id)
            except IndexError:
                logging.error(f"error spotify preview {id}")
                continue

            data = sp.track(id)
            try:
                features = songdata.get_audio_features(id)
            except requests.exceptions.HTTPError:
                logging.error(f"error songdata {id}")
                time.sleep(10)
                continue
            data.update(features)
            data.update(previews)
            # del data["album"]["available_markets"]
            # del data["available_markets"]
            # pprint(data)
            # print("="*100)
            
            try:
                songs.insert_one(data)
                logging.debug(f"song added to database {id} {index+1}/{pl_length}")
            except errors.DuplicateKeyError:
                logging.debug(f"song already scraped {id}")
                pass
            
            time.sleep(20)
        

        playlist = sp.playlist(playlist_id)
        playlists.insert_one(playlist)
        logging.info(f"finished scraping playlist {playlist_id}")
        # except errors.DuplicateKeyError:
            # pass

    except KeyboardInterrupt:
        raise SystemExit()