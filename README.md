# cose da fare

- scarica la repo o clonala con ```git clone https://github.com/sbOogway/data_spotify_api```
- crea un app a questo link. devi loggare con il tuo account spoti. https://developer.spotify.com/dashboard
- dopo aver create l app (nome non e importante) devi mettere le info di esse in un file chiamato 
.env con il seguente contenuto. il file deve essere nella cartella della repository tutti i commandi 
successivi devono essere invocati da quel percorso

```
SPOTIPY_CLIENT_ID=client_id_of_ur_app
SPOTIPY_CLIENT_SECRET=client_secret_of_ur_app
SPOTIPY_REDIRECT_URI=redirect_uri_of_ur_app
```
questo file non devi condividerlo con nessuno e come se fosse una password

- apri un powershell e fai girare lo script con questo comando. ricordarti di spostarti nella cartella 
giusta. ```.\setup.ps1```

- fai girare il comando ```python main.py``` la prima volta ti aprira un link nel browser. 
copialo ed incollalo nel powershell e ti verra dato un token che verra scritto nel file 
```.cache``` per interfacciarti con l api

- per chiamare i metodi che ti servono leggi la documentazione e guarda gli esempi in essa
https://spotipy.readthedocs.io/en/pga-v1.1.55/index.html#spotipy.client.Spotify


## limitations
- currently works only 30 trackids from playlist in open spotify 

## ideas
- use bluetooth for game play?
- get song lirycs and song language from genius? https://github.com/johnwmillr/LyricsGenius
- get bpm and key from songdata
- get other streamin platforms links

yoloyy
