###############################################################################
### UI scripts
###############################################################################

INFO = {
    'url' : 'Lien URL',
    'path' : 'Destination',
    'name' : 'Nom fichier*',
    'name_info' : '* Optionnel. Ne concerne pas les playlists'}

DL_TYPES = ('Vidéo', 'Playlist')

BROWSE_BUTTON = "Parcourir"

EXT_TYPES = ('.mp3', '.mp4')

DL_BUTTON = "Télécharger"

LOADING_YT_OBJECT = (
    "Accès à la vidéo en cours. Cela peut prendre un moment.", 
    "Accès aux vidéos en cours. Cela peut prendre un moment.")

DOWNLOADING_STREAMS = "Téléchargement en cours"

FINISHED_DOWNLOADING = "Téléchargement terminé ! :)"

###############################################################################
### Downloader scripts
###############################################################################

ERR_URL = "Lien URL invalide"

ERR_NO_PATH = "Emplacement du dossier de destination\nvide ou invalide"

ERR_UNAVAILABLE_VIDEO = """Échec d'accès à la vidéo

Causes possibles :
- Vidéo inexistante
- Restriction d'âge/de pays"""

ERR_VIDEO_PRIVATE = "Téléchargement impossible car la vidéo est privée"

ERR_PLAYLIST = """Téléchargement impossible car la playlist est
inexistante, privée, vide ou ne contient que des vidéos privées.""".strip('\n')

ERR_CONNECTION = """Connexion impossible.
Vérifiez votre connexion internet et réessayez."""