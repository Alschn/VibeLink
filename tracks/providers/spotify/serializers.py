"""
Reference:

- https://developer.spotify.com/documentation/web-api/reference/get-track
"""
from rest_framework import serializers


class SpotifyImageSerializer(serializers.Serializer):
    height = serializers.IntegerField(allow_null=True)
    url = serializers.CharField(allow_null=True, allow_blank=True)
    width = serializers.IntegerField(allow_null=True)


class SpotifyArtistEmbeddedSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    uri = serializers.CharField()
    href = serializers.CharField()
    external_urls = serializers.DictField()


class SpotifyAlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    uri = serializers.CharField()
    album_type = serializers.CharField()
    total_tracks = serializers.IntegerField(min_value=0)
    href = serializers.CharField()
    external_urls = serializers.DictField()
    release_date = serializers.DateField()
    images = SpotifyImageSerializer(many=True)
    artists = SpotifyArtistEmbeddedSerializer(many=True)


class SpotifyTrackSerializer(serializers.Serializer):
    id = serializers.CharField()
    href = serializers.CharField()
    name = serializers.CharField()
    uri = serializers.CharField()
    duration_ms = serializers.IntegerField()
    explicit = serializers.BooleanField()
    preview_url = serializers.CharField()
    external_ids = serializers.DictField()
    external_urls = serializers.DictField()
    album = SpotifyAlbumSerializer()
    artists = SpotifyArtistEmbeddedSerializer(many=True)


class SpotifyArtistSerializer(serializers.Serializer):
    # not used yet
    id = serializers.CharField()
    href = serializers.CharField()
    name = serializers.CharField()
    uri = serializers.CharField()
    external_urls = serializers.DictField()
    followers = serializers.DictField()
    genres = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    images = SpotifyImageSerializer(many=True)
