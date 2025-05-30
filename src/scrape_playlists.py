import sys
import os


if __name__ == "__main__":
    interpreter = "python"
    # playlist_ids_file = sys.argv[1]
    # try:
    lines = []
    with open("data/link_playlist2.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        os.system(f"{interpreter} src/scrape_playlist.py {line}")

    # except KeyboardInterrupt:
    #     raise SystemExit()