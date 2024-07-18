import dataclasses
import logging

import spotipy
from django.db import transaction
from rest_framework import serializers

from links.models import Link
from tracks.models import Track, Author
from tracks.providers.spotify.client import get_spotify_client
from tracks.providers.spotify.models import SpotifyTrack
from tracks.providers.spotify.serializers import SpotifyTrackSerializer
from tracks.providers.spotify.utils import extract_spotify_track_id_from_url

logger = logging.getLogger(__name__)


def gather_spotify_metadata(link: Link) -> dict:
    track_id = extract_spotify_track_id_from_url(link.url)

    if not track_id:
        # todo: raise custom exception, catch and log it inside the task
        logger.exception('Failed to parse Spotify track URL: %s', link.url)
        return {}

    try:
        spotify_track = get_spotify_track(track_id=track_id)
    except spotipy.exceptions.SpotifyException as e:
        # todo: raise custom exception, catch and log it inside the task
        logger.exception(e, exc_info=True)
        return {}
    except serializers.ValidationError as e:
        # something might have changed in the API response,
        # in that case serializer should be updated as well
        logger.exception(e, exc_info=True)
        return {}

    create_records_from_metadata(link, spotify_track)

    return dataclasses.asdict(spotify_track)


def get_spotify_track(track_id: str, **kwargs) -> SpotifyTrack:
    spotify_client = get_spotify_client()
    data = spotify_client.track(track_id=track_id, **kwargs)

    spotify_track = transform_spotify_track_data(data)
    return spotify_track


def transform_spotify_track_data(data: dict) -> SpotifyTrack:
    serializer = SpotifyTrackSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    track = serializer.save()
    return track


def create_records_from_metadata(link: Link, spotify_track: SpotifyTrack) -> Track:
    track = track_from_spotify_track(spotify_track)
    link.track = track
    link.save(update_fields=['track'])
    return track


@transaction.atomic
def track_from_spotify_track(spotify_track: SpotifyTrack) -> Track:
    # todo: maybe move this functionality to Track objects manager or model

    # todo: maybe create all artists in the list, not just the main one
    spotify_author, *_ = spotify_track.artists
    author, _ = Author.objects.get_or_create(
        name=spotify_author.name,
        defaults={
            'meta': dataclasses.asdict(spotify_author),
        }
    )

    track, _ = Track.objects.get_or_create(
        name=spotify_track.name,
        author=author,
        defaults={
            'meta': dataclasses.asdict(spotify_track),
        }
    )

    return track
