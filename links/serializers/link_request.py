from rest_framework import serializers

from accounts.serializers.user import UserSerializer
from links.models import LinkRequest


class LinkRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LinkRequest
        fields = (
            'id',
            'user',
            'link',
            'created_at',
            'fulfilled_at',
        )
