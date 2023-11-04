from django_filters.rest_framework import FilterSet

from links.models import LinkRequest


class LinkRequestsFilterSet(FilterSet):
    class Meta:
        model = LinkRequest
        fields = {
            'user': ['exact', 'in'],
            'link': ['isnull'],
            'created_at': ['lte', 'gte'],
            'fulfilled_at': ['lte', 'gte'],
        }
