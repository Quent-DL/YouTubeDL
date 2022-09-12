###############################################################################
### UI scripts
###############################################################################

INFO = {
    'url' : 'Lien URL',
    'path' : 'Destination',
    'name' : 'Nom fichier*',
    'name_info' : '* Optionnel. Ne concerne pas les playlists'}

DL_TYPES = ('Vidéo', 'Playlist')

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

ERR_UNAVAILABLE_VIDEO = """Échec d'accès à la vidéo

Causes possibles :
- Vidéo inexistante
- Vidéo privée
- Restriction d'âge/de pays"""

ERR_UNAVAILABLE_PLAYLIST = "Playlist vide ou privée"

ERR_CONNECTION = """Connexion impossible.
Vérifiez votre connexion internet et réessayez."""