import dataclasses
import logging
from typing import Iterable, Any

import googleapiclient.errors
from django.db import transaction
from rest_framework import serializers

from links.models import Link
from tracks.models import Author, Track
from tracks.providers.youtube.client import get_youtube_client
from tracks.providers.youtube.models import YoutubeVideoList, YoutubeVideo, YoutubeParts
from tracks.providers.youtube.serializers import YoutubeVideoListSerializer
from tracks.providers.youtube.utils import extract_youtube_video_id_from_url

logger = logging.getLogger(__name__)

DEFAULT_PARTS = [YoutubeParts.VIDEO_ID, YoutubeParts.SNIPPET, YoutubeParts.STATISTICS]


def gather_youtube_metadata(link: Link) -> dict:
    video_id = extract_youtube_video_id_from_url(link.url)

    if not video_id:
        logger.exception('Failed to parse YouTube video URL: %s', link.url)
        return {}

    try:
        youtube_video = get_youtube_video(video_id)
    except googleapiclient.errors.Error as e:
        logger.exception(e, exc_info=True)
        raise e
    except serializers.ValidationError as e:
        # something might have changed in the API response,
        # in that case serializer should be updated as well
        logger.exception(e, exc_info=True)
        raise e

    create_records_from_metadata(link, youtube_video)

    return dataclasses.asdict(youtube_video)


def get_video_data(video_id: str, parts: Iterable[str] = None, **kwargs: Any) -> dict:
    parts = parts or DEFAULT_PARTS

    youtube_client = get_youtube_client()
    request = youtube_client.videos().list(
        part=','.join(parts),
        id=video_id,
        **kwargs
    )
    return request.execute()


def transform_youtube_video_data(data: dict) -> YoutubeVideoList:
    serializer = YoutubeVideoListSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    video_list = serializer.save()
    return video_list


def get_youtube_video(video_id: str) -> YoutubeVideo:
    data = get_video_data(video_id, parts=('id', 'snippet', 'statistics',))

    video_list = transform_youtube_video_data(data)
    video = video_list.items[0]
    return video


def create_records_from_metadata(link: Link, youtube_video: YoutubeVideo) -> Track:
    track = track_from_youtube_video(youtube_video)
    link.track = track
    link.save(update_fields=['track'])
    return track


@transaction.atomic
def track_from_youtube_video(youtube_video: YoutubeVideo) -> Track:
    snippet = youtube_video.snippet

    author, _ = Author.objects.get_or_create(
        name=snippet.channelTitle,
        defaults={
            'meta': {
                'channelId': snippet.channelId,
                'channelTitle': snippet.channelTitle,
            },
        }
    )

    track, _ = Track.objects.get_or_create(
        name=snippet.title,
        author=author,
        defaults={
            'meta': dataclasses.asdict(youtube_video),
        }
    )

    return track
