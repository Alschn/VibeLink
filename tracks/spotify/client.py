import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials


# todo: maybe create custom Spotify client class

def get_spotify_client() -> spotipy.Spotify:
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET
        )
    )
