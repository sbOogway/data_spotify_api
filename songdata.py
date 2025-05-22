import requests
import re
from pprint import pprint

POPULARITY = r"<dt>Popularity<\/dt>\s*<dd id=\"popular_text\">(\d+)%<\/dd>"
ACOUSTICNESS = r"<dt>Acousticness<\/dt>\s*<dd>(\d+)%<\/dd>"
ENERGY = r"<dt>Energy<\/dt>\s*<dd>(\d+)%<\/dd>"
LIVENESS = r"<dt>Liveness<\/dt>\s*<dd>(\d+)%<\/dd>"
SPEECHINESS = r"<dt>Speechiness<\/dt>\s*<dd>(\d+)%<\/dd>"
DANCEABILITY = r"<dt>Danceability<\/dt>\s*<dd>(\d+)%<\/dd>"
INSTRUMENTALNESS = r"<dt>Instrumentalness<\/dt>\s*<dd>(\d+)%<\/dd>"
LOUDNESS = r"<dt>Loudness<\/dt>\s*<dd>(\d+)%<\/dd>"
VALENCE = r"<dt>Valence<\/dt>\s*<dd>(\d+)%<\/dd>"

def get_audio_features(track_id: str) -> dict:
    response = requests.get(f"https://songdata.io/track/{track_id}/", allow_redirects=True)

    result = {}

    if response.status_code < 400:
        result["popularity"] = int(re.search(POPULARITY, response.text).group(1))
        result["acousticness"] = int(re.search(ACOUSTICNESS, response.text).group(1))
        result["energy"] = int(re.search(ENERGY, response.text).group(1))
        result["liveness"] = int(re.search(LIVENESS, response.text).group(1))
        result["speechiness"] = int(re.search(SPEECHINESS, response.text).group(1))
        result["danceability"] = int(re.search(DANCEABILITY, response.text).group(1))
        result["instrumentalness"] = int(re.search(INSTRUMENTALNESS, response.text).group(1))
        result["loudness"] = int(re.search(LOUDNESS, response.text).group(1))
        result["valence"] = int(re.search(VALENCE, response.text).group(1))
    
    else:
        raise requests.HTTPError()
    
    return result
        

if __name__ == "__main__":
    pprint(get_audio_features("45J4avUb9Ni0bnETYaYFVJ"))
