"""
Reference:

- https://developer.spotify.com/documentation/web-api/reference/get-track
"""

import dataclasses
from typing import Any


@dataclasses.dataclass
class SpotifyImage:
    height: int | None
    url: str | None
    width: int | None


@dataclasses.dataclass
class SpotifyArtistEmbedded:
    id: str
    name: str
    uri: str
    href: str
    external_urls: dict[str, Any]


@dataclasses.dataclass
class SpotifyAlbum:
    id: str
    name: str
    uri: str
    album_type: str
    total_tracks: int
    href: str
    external_urls: dict[str, Any]
    release_date: str
    images: list[SpotifyImage]
    artists: list[SpotifyArtistEmbedded]


@dataclasses.dataclass
class SpotifyTrack:
    id: str
    href: str
    name: str
    uri: str
    duration_ms: int
    explicit: bool
    preview_url: str | None
    external_ids: dict[str, Any]
    external_urls: dict[str, Any]
    album: SpotifyAlbum
    artists: list[SpotifyArtistEmbedded]


@dataclasses.dataclass
class SpotifyArtist:
    id: str
    href: str
    name: str
    uri: str
    external_urls: dict[str, Any]
    followers: dict[str, Any]
    genres: list[str]
    images: list[SpotifyImage]
