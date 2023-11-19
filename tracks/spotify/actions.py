import logging
import re

import spotipy
from django.db import transaction

from tracks.models import Track, Author
from tracks.spotify.client import spotify_client

logger = logging.getLogger(__name__)


def gather_spotify_metadata(url: str) -> dict:
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

    metadata = transform_spotify_track_data(track)

    create_records_from_metadata(metadata)

    return metadata


def transform_spotify_track_data(track: dict) -> dict:
    # todo: transform metadata to our (type-safe and minimal) format

    return track


@transaction.atomic
def create_records_from_metadata(metadata: dict) -> Track:
    authors = metadata['artists']
    author = authors[0]

    author, _ = Author.objects.get_or_create(
        name=author['name'],
        defaults={
            'meta': author,
        }
    )

    track = Track.objects.create(
        name=metadata['name'],
        author=author,
        meta=metadata,
    )
    return track
