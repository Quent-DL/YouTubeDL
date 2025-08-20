import os
from dotenv import load_dotenv, dotenv_values 
import requests
import Levenshtein

# TODO move in application
# loading API key from the .env file
load_dotenv() 


# TODO: handle access token expiration
def get_access_token() -> str:
    # HTTP arguements
    url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Request
    response = requests.post(url, params=body, headers=headers)

    # Processing
    response.raise_for_status()
    return response.json()['access_token']


def compute_info_from_query(query: str, access_token: str, limit=5) -> list[tuple[str]]:

    def compute_info(track_obj: dict) -> str:
        # Isolating info
        track_name = track_obj['name']
        track_artists = ", ".join([artist_obj['name'] for artist_obj in track_obj['artists']])
        return (track_artists, track_name)

    # HTTP arguments
    url = "https://api.spotify.com/v1/search"
    body = {
        "q": query,
        "type": "track",
        "limit" : limit,
        "offset": 0
    }
    headers = {"Authorization": "Bearer " + access_token}

    # Request
    response = requests.get(url, params=body, headers=headers)
    response.raise_for_status()

    potential_names = [compute_info(track_obj) for track_obj in response.json()['tracks']['items']]
    
    return potential_names


def pick_closest(query_name: str, targets: list[tuple[str]]) -> str:
    def get_score(a: str) -> float:
        return max(
            # TODO
        )
    # TODO INCOMPLETE
    scores = [(t, Levenshtein.ratio(query_name, t)) for t in targets]
    


# TODO debug remove
print(Levenshtein.ratio("Dua Lipa - My Heart", "My Heart - Dua Lipa"))
exit()



query = "Dua Lipa - Break My Heart (Lyrics)"
access_token = get_access_token()

for name in compute_names_from_query(query, access_token, 20):
    print(f"{Levenshtein.ratio(query, name):.3f} - {name}")