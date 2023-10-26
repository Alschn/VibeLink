from friendship.models import FriendshipRequest
from rest_framework import serializers

from accounts.serializers.user import UserSerializer


class FriendshipRequestSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()
    from_user = UserSerializer()

    class Meta:
        model = FriendshipRequest
        fields = (
            'id',
            'from_user',
            'to_user',
            'message',
            'created',
            'rejected',
            'viewed'
        )
