import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

# Autenticazione
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

# limit = numero di canzoni
tracks = sp.current_user_saved_tracks(limit=50)

data = []

for item in tracks['items']:
    track = item['track']
    
    try:
        artist = sp.artist(track['artists'][0]['id'])
    except Exception as e:
        print(f"Errore nell'artista: {track['name']} – {e}")
        continue

    try:
        features = sp.audio_features(track['id'])[0]
        if features is None:
            raise Exception("Nessuna audio feature disponibile")
    except Exception as e:
        print(f"Errore nelle audio features: {track['name']} – {e}")
        features = {  # inserisce NaN per le colonne delle audio features
            'danceability': None, 'energy': None, 'key': None, 'loudness': None,
            'mode': None, 'speechiness': None, 'acousticness': None, 'instrumentalness': None,
            'valence': None, 'tempo': None, 'duration_ms': None, 'time_signature': None
        }

    row = {
        'track_name': track['name'],
        'track_id': track['id'],
        'preview_url': track['preview_url'],
        'explicit': track['explicit'],
        'track_popularity': track['popularity'],
        'track_number': track['track_number'],

        'artist_name': artist['name'],
        'artist_id': artist['id'],
        'artist_genres': artist['genres'],
        'artist_popularity': artist['popularity'],
        'artist_followers': artist['followers']['total'],

        'album_name': track['album']['name'],
        'release_date': track['album']['release_date'],
        'total_tracks': track['album']['total_tracks'],
        'album_type': track['album']['album_type'],
        
        #audio features
        'danceability': features['danceability'],
        'energy': features['energy'],
        'key': features['key'],
        'loudness': features['loudness'],
        'mode': features['mode'],
        'speechiness': features['speechiness'],
        'acousticness': features['acousticness'],
        'instrumentalness': features['instrumentalness'],
        'valence': features['valence'],
        'tempo': features['tempo'],
        'duration_ms': features['duration_ms'],
        'time_signature': features['time_signature']
    }

    data.append(row)

# Salva i dati
df = pd.DataFrame(data)
df.to_csv("data/spotify_data_partial.csv", index=False)

print("✅ Dataset salvato come 'spotify_data_partial.csv'")
print("🔢 Numero righe raccolte:", len(df))
