"""
Resource:

- https://developers.google.com/youtube/v3/docs/videos/list
"""

from rest_framework import serializers


class YoutubePageInfoSerializer(serializers.Serializer):
    totalResults = serializers.IntegerField()
    resultsPerPage = serializers.IntegerField()


class YoutubeVideoStatisticsSerializer(serializers.Serializer):
    viewCount = serializers.IntegerField()
    likeCount = serializers.IntegerField()
    commentCount = serializers.IntegerField()


class YoutubeVideoSnippetSerializer(serializers.Serializer):
    publishedAt = serializers.DateTimeField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnails = serializers.DictField()
    channelTitle = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    categoryId = serializers.CharField()
    defaultLanguage = serializers.CharField()
    defaultAudioLanguage = serializers.CharField()


class YoutubeVideoSerializer(serializers.Serializer):
    kind = serializers.CharField()
    etag = serializers.CharField()
    id = serializers.CharField()
    snippet = YoutubeVideoSnippetSerializer()
    statistics = YoutubeVideoStatisticsSerializer()


class YoutubeVideoListSerializer(serializers.Serializer):
    kind = serializers.CharField()
    etag = serializers.CharField()
    items = serializers.ListField(
        child=YoutubeVideoSerializer(),
        min_length=1
    )
    pageInfo = YoutubePageInfoSerializer()
