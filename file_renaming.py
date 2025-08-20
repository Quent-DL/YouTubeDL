import os
from dotenv import load_dotenv, dotenv_values 
import requests
from thefuzz import fuzz
from numpy import argmax
from typing import NewType
import re

# Detailed subtypes, for documentation purposes
TrackArtist = NewType("TrackArtist", str)
TrackName = NewType("TrackName", str)
SpotifyResults = NewType("SpotifyResults", list[tuple[TrackArtist, TrackName]])


# Constants
MIN_CONFIDENCE = 90

# loading API key from the .env file when importing this Python file
load_dotenv() 

# by default, no Spotify access key is defined
access_token = None


# TODO: handle access token expiration
def _get_access_token() -> str:
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


def _compute_info_from_query(query: str, access_token: str, limit=50) -> SpotifyResults:

    def compute_info(track_obj: dict) -> tuple[TrackArtist, TrackName]:
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

    spotify_results = [compute_info(track_obj) for track_obj in response.json()['tracks']['items']]
    return spotify_results


def _pick_most_relevant(query: str, spotify_results: SpotifyResults, min_confidence: int = MIN_CONFIDENCE) -> str:
    def score(artist: str, title: str) -> float:
        # Disregards order of the info in the query
        return fuzz.partial_token_sort_ratio(
            query, f"{artist} {title}")

    scores = [score(*track_info) for track_info in spotify_results]

    # Using query name OR Spotify name, based on confidence threshold
    best_idx = argmax(scores)
    if scores[best_idx] >= min_confidence:
        best_artist, best_title = spotify_results[argmax(scores)]
        return f"{best_artist} - {best_title}"
    else:
        return query


def get_spotify_name(query: str, min_confidence: int=MIN_CONFIDENCE) -> str:
    # Only fetching an access token once for the following calls
    global access_token
    if not access_token:
        access_token = _get_access_token()

    # Processing query
    ## removing parentheses content (eg. "(lyrics)", "[lyrics]", ...)
    query = re.sub(r'\(([^)]+)\)', "", query)
    query = re.sub(r'\[([^]]+)\]', "", query)
    query = re.sub(r'\{([^}]+)\}', "", query)
    ## removing successive spaces between words
    query = re.sub(r'[ ]+', " ", query)

    # Selecting appropriate name based on query
    return _pick_most_relevant(
        query, _compute_info_from_query(query, access_token), min_confidence)
