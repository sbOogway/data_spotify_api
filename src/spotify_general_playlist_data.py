import songdata
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# --- Autenticazione ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private"))

# --- ID della playlist pubblica (puoi cambiarlo con una tua) ---
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Esempio: Today's Top Hits

# --- Recupera tutti gli elementi della playlist ---
results = sp.playlist_items(playlist_id)
tracks = results['items']

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# --- Prepara il dataset ---
data = []

for item in tracks:
    track = item['track']
    
    # Evita problemi con brani non disponibili
    if track is None:
        continue

    try:
        artist = sp.artist(track['artists'][0]['id'])
    except:
        artist = {
            'name': 'Unknown',
            'id': None,
            'genres': [],
            'popularity': None,
            'followers': {'total': None}
        }

    audio_features = songdata.get_audio_features(track) 

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
    }

    data.append(row)

# --- Salva su CSV o mostra ---
df = pd.DataFrame(data)
df.to_csv("data/playlist_dataset.csv", index=False)
print("✅ Dataset salvato: playlist_dataset.csv")
print(df.head())
