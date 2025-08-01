import time
import itertools
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
        # playlist_id = sys.argv[1] 
        # playlist_id = "19PgP2QSGPcm6Ve8VhbtpG"


        scope = "user-library-read"

        client = MongoClient(os.getenv("DB_HOST", "mongodb://localhost:27017/"))
        songs = client["guess_tha_song"]["songs"]
        artists = client["guess_tha_song"]["artists"]

        artists.create_index("id", unique=True)

        songs_db = songs.find({}, {"artists": 1, "_id": 0})
        artists_db = artists.find({}, {"id":1, "_id":0} )

        
        
        songs_db = list(map(lambda x : x['artists'], songs_db))
        artists_db = set(list(map(lambda x : x["id"], artists_db)))
        pprint(artists_db)

        flat_db = list(itertools.chain.from_iterable(songs_db))

        flat_db = set(list(map(lambda x: x["id"], flat_db)))


        # pprint(flat_db)
        print(len(flat_db))

        
        artists_to_find = flat_db - artists_db
        print(len(artists_to_find))

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        for art in artists_to_find:
            artist = sp.artist(art)
            artists.insert_one(artist)
            logging.debug(f'new artists added to database {artist["name"]} - {artist["genres"]}')
            time.sleep(20)

        exit()
    except KeyboardInterrupt:
        raise SystemExit()