
from rest_framework_dataclasses.serializers import DataclassSerializer

from tracks.providers.spotify.models import (
    SpotifyImage,
    SpotifyArtistEmbedded,
    SpotifyAlbum,
    SpotifyTrack,
    SpotifyArtist
)


class SpotifyImageSerializer(DataclassSerializer[SpotifyImage]):
    class Meta:
        dataclass = SpotifyImage


class SpotifyArtistEmbeddedSerializer(DataclassSerializer[SpotifyArtistEmbedded]):
    class Meta:
        dataclass = SpotifyArtistEmbedded


class SpotifyAlbumSerializer(DataclassSerializer[SpotifyAlbum]):
    class Meta:
        dataclass = SpotifyAlbum


class SpotifyTrackSerializer(DataclassSerializer[SpotifyTrack]):
    class Meta:
        dataclass = SpotifyTrack


class SpotifyArtistSerializer(DataclassSerializer[SpotifyArtist]):
    class Meta:
        dataclass = SpotifyArtist
