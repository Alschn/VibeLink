import logging
import re
from typing import Iterable, Any

import googleapiclient.errors
from django.db import transaction
from rest_framework import serializers

from links.models import Link
from tracks.models import Author, Track
from tracks.youtube import get_youtube_client
from tracks.youtube.serializers import YoutubeVideoListSerializer

logger = logging.getLogger(__name__)


def gather_youtube_metadata(link_id: int, url: str) -> dict:
    id_regex = r'[a-zA-Z0-9_-]+'
    pattern_full = f'watch\?v=({id_regex})'
    pattern_short = f'youtu\.be\/({id_regex})'

    if match_full := re.search(pattern_full, url):
        video_id = match_full.group(1)

    elif match_short := re.search(pattern_short, url):
        video_id = match_short.group(1)

    else:
        logger.exception('Failed to parse YouTube video URL: %s', url)
        return {}

    try:
        videos_list = get_video_data(video_id, parts=('id', 'snippet', 'statistics',))
    except googleapiclient.errors.Error as e:
        logger.exception(e, exc_info=True)
        return {}

    try:
        metadata = transform_youtube_video_data(videos_list)
    except serializers.ValidationError as e:
        # something might have changed in the API response,
        # in that case serializer should be updated as well
        logger.exception(e, exc_info=True)
        return {}

    create_records_from_metadata(link_id, metadata)

    return metadata


def transform_youtube_video_data(results: dict) -> dict:
    serializer = YoutubeVideoListSerializer(data=results)
    serializer.is_valid(raise_exception=True)
    return serializer.data


@transaction.atomic
def create_records_from_metadata(link_id: int, metadata: dict) -> dict:
    video = metadata['items'][0]
    snippet = video['snippet']

    author, _ = Author.objects.get_or_create(
        name=snippet['channelTitle'],
        defaults={
            'meta': {
                'channelId': snippet['channelId'],
                'channelTitle': snippet['channelTitle'],
            },
        }
    )

    track, _ = Track.objects.get_or_create(
        name=snippet['title'],
        author=author,
        defaults={
            'meta': video,
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


def get_video_data(video_id: str, parts: Iterable[str] = None, **kwargs: Any) -> dict:
    parts = parts or ['id', 'snippet', 'statistics']

    youtube_client = get_youtube_client()
    request = youtube_client.videos().list(
        part=','.join(parts),
        id=video_id,
        **kwargs
    )
    return request.execute()
