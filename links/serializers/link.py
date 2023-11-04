from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.serializers.user import UserSerializer
from links.models import Link, LinkRequest

User = get_user_model()


class LinkSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Link
        fields = (
            'id',
            'title',
            'description',
            'url',
            'source_type',
            'user',
            'track',
            'created_at',
            'updated_at',
        )


class LinkCreateSerializer(serializers.ModelSerializer):
    link_request = serializers.IntegerField(write_only=True)

    def __init__(self, *args, user: User = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.link_request = None

    class Meta:
        model = Link
        fields = (
            'id',
            'title',
            'description',
            'url',
            'link_request',
            'source_type',
            'user',
            'track',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'source_type': {'read_only': True, 'required': False},
            'user': {'read_only': True, 'required': False},
            'track': {'read_only': True, 'required': False},
        }

    def validate_link_request(self, value: int) -> int:
        user = self.user or self.context['request'].user

        try:
            self.link_request = LinkRequest.objects.get(
                id=value, user=user
            )
        except LinkRequest.DoesNotExist:
            raise serializers.ValidationError(
                'The link request does not exist or belong to the user'
            )

        return value

    @transaction.atomic
    def create(self, validated_data: dict):
        user = self.user or self.context['request'].user
        source_type = get_source_type_from_url(validated_data['url'])
        validated_data.pop('link_request')

        instance = super().create({
            **validated_data,
            'user': user,
            'source_type': source_type,
        })
        self.link_request.add_link(instance)
        return instance


def get_source_type_from_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.hostname

    if host.endswith('youtube.com') or host.endswith('youtu.be'):
        return Link.SourceType.YOUTUBE

    if host.endswith('spotify.com'):
        return Link.SourceType.SPOTIFY

    return Link.SourceType.UNKNOWN
