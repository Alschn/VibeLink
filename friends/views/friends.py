from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from django_filters.rest_framework import DjangoFilterBackend
from friendship.models import Friend
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from friends.filters.friend import FriendsFilterSet
from friends.serializers import (
    FriendSerializer,
    FriendAddSerializer
)

User = get_user_model()

FriendsPagination = page_number_pagination_factory(
    page_size=10, max_page_size=100
)


class FriendsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    pagination_class = FriendsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FriendsFilterSet

    def get_queryset(self) -> QuerySet[User]:
        return Friend.objects.select_related(
            'from_user', 'to_user'
        ).filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        ).distinct().order_by('id')

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendAddSerializer

        if self.action == 'destroy':
            return serializers.Serializer

        return FriendSerializer

    def get_serializer(self, *args: Any, **kwargs: Any):
        if self.action in ('create', 'destroy'):
            kwargs.update({'user': self.request.user})

        return super().get_serializer(*args, **kwargs)

    def perform_destroy(self, instance: Friend) -> None:
        Friend.objects.remove_friend(instance.from_user, instance.to_user)
