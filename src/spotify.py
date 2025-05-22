import requests
import re
import time

TRACK_ID = r"track/([a-zA-Z0-9]+)"
PREVIEW = r'content="(https://.\.scdn\.co/.*?)"'
def get_tracks_playlist(playlist_id: str) -> set:
    response = requests.get(f"https://open.spotify.com/playlist/{playlist_id}")

    if response.status_code < 400:
        # print(response.text)
        ids = set(re.findall(TRACK_ID, response.text))
        # print(ids, len(ids), set(ids), len(set(ids)))

        # exit(10)
        return ids
        

        

def get_preview(track_id: str) -> dict:
    response = requests.get(f"https://open.spotify.com/track/{track_id}")

    if response.status_code < 400:

        previews = list(set(re.findall(PREVIEW, response.text)))
        previews.sort()
        return {"image": previews[0], "audio": previews[1]}


if __name__ == "__main__":
    get_tracks_playlist("37i9dQZF1DXcBWIGoYBM5M")