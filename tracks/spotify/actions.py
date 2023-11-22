import logging
import re

import spotipy
from django.db import transaction
from rest_framework import serializers

from links.models import Link
from tracks.models import Track, Author
from tracks.spotify import get_spotify_client
from tracks.spotify.serializers import SpotifyTrackSerializer

logger = logging.getLogger(__name__)


def gather_spotify_metadata(link_id: int, url: str) -> dict:
    spotify_client = get_spotify_client()

    pattern = 'track/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)

    if not match:
        # todo: raise custom exception, catch and log it inside the task
        logger.exception('Failed to parse Spotify track URL: %s', url)
        return {}

    track_id = match.group(1)

    try:
        track = spotify_client.track(track_id=track_id)
    except spotipy.exceptions.SpotifyException as e:
        # todo: raise custom exception, catch and log it inside the task
        logger.exception(e, exc_info=True)
        return {}

    try:
        metadata = transform_spotify_track_data(track)
    except serializers.ValidationError as e:
        # something might have changed in the API response,
        # in that case serializer should be updated as well
        logger.exception(e, exc_info=True)
        return {}

    create_records_from_metadata(link_id, metadata)

    return metadata


def transform_spotify_track_data(track: dict) -> dict:
    serializer = SpotifyTrackSerializer(data=track)
    serializer.is_valid(raise_exception=True)
    return serializer.data


@transaction.atomic
def create_records_from_metadata(link_id: int, metadata: dict) -> Track:
    authors = metadata['artists']
    author = authors[0]

    author, _ = Author.objects.get_or_create(
        name=author['name'],
        defaults={
            'meta': author,
        }
    )

    track, _ = Track.objects.get_or_create(
        name=metadata['name'],
        author=author,
        defaults={
            'meta': metadata,
        }
    )

    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        logger.exception(
            'Link with id %s does not exist. Could not attach track to Link object.',
            link_id
        )
        return track

    link.track = track
    link.save(update_fields=['track'])
    return track
