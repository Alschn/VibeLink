from django_filters.rest_framework import FilterSet
from friendship.models import Friend


class FriendsFilterSet(FilterSet):
    class Meta:
        model = Friend
        fields = {
            'to_user': ['exact'],
            'to_user__username': ['icontains'],
            'created': ['gte', 'lte', 'isnull'],
        }
