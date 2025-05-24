import os
import time
import subprocess

if __name__ == "__main__":
    while True:
        os.system("git rev-parse HEAD > tmp/current_head")
        time.sleep(60)
        os.system("git pull > /dev/null")    
        os.system("git rev-parse HEAD > tmp/latest_head")        
        os.system("cmp tmp/latest_head tmp/current_head || python src/scrape_playlists.py data/playlist_ids")
        
        