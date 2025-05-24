FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN apt update && apt install -y python3 python3-venv python3-pip

RUN python3 -m venv venv && pip install --break-system-packages -r requirements.txt

RUN set -a; source /env_server; set +a

ENTRYPOINT [ "python3", "src/scrape_playlists.py" ]

