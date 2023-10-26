from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from friendship.exceptions import AlreadyFriendsError, AlreadyExistsError
from friendship.models import Friend, FriendshipRequest
from rest_framework import serializers

from accounts.serializers.user import UserSerializer

User = get_user_model()


class FriendSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()

    class Meta:
        model = Friend
        fields = (
            'id',
            'from_user',
            'to_user',
            'created'
        )


class FriendAddSerializer(serializers.ModelSerializer):

    def __init__(self, *args, user: User = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_user = user

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
        read_only_fields = (
            'id',
            'from_user',
            'created',
            'rejected',
            'viewed'
        )

    @transaction.atomic
    def create(self, validated_data) -> Friend:
        from_user = self.from_user or self.context['request'].user
        to_user = validated_data['to_user']
        message = validated_data.get('message')

        try:
            friend_request = Friend.objects.add_friend(from_user, to_user, message)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'to_user': e.message})
        except (AlreadyFriendsError, AlreadyExistsError) as e:
            raise serializers.ValidationError({'to_user': e})

        return friend_request
