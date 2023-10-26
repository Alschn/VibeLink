from django_filters.rest_framework import FilterSet
from friendship.models import Friend, FriendshipRequest


class FriendshipRequestFilterSet(FilterSet):
    class Meta:
        model = FriendshipRequest
        fields = {
            'to_user': ['exact'],
            'to_user__username': ['icontains'],
            'created': ['gte', 'lte', 'isnull'],
            'rejected': ['gte', 'lte', 'isnull'],
            'viewed': ['gte', 'lte', 'isnull']
        }
