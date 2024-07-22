"""
Resource:

- https://developers.google.com/youtube/v3/docs/videos/list
"""
from rest_framework_dataclasses.serializers import DataclassSerializer

from tracks.providers.youtube.models import (
    YoutubePageInfo,
    YoutubeVideoStatistics,
    YoutubeVideoSnippet,
    YoutubeVideo,
    YoutubeVideoList
)


class YoutubePageInfoSerializer(DataclassSerializer[YoutubePageInfo]):
    class Meta:
        dataclass = YoutubePageInfo


class YoutubeVideoStatisticsSerializer(DataclassSerializer[YoutubeVideoStatistics]):
    class Meta:
        dataclass = YoutubeVideoStatistics


class YoutubeVideoSnippetSerializer(DataclassSerializer[YoutubeVideoSnippet]):
    class Meta:
        dataclass = YoutubeVideoSnippet


class YoutubeVideoSerializer(DataclassSerializer[YoutubeVideo]):
    class Meta:
        dataclass = YoutubeVideo


class YoutubeVideoListSerializer(DataclassSerializer[YoutubeVideoList]):
    class Meta:
        dataclass = YoutubeVideoList
        extra_kwargs = {
            'items': {'min_length': 1}
        }
