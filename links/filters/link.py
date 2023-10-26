from django_filters.rest_framework import FilterSet

from links.models import Link


class LinksFilterSet(FilterSet):
    class Meta:
        model = Link
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'url': ['icontains'],
            'source_type': ['exact'],
            'track': ['exact', 'in'],
            'created_at': ['gte', 'lte'],
            'updated_at': ['gte', 'lte'],
        }
