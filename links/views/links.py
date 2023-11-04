from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from links.filters.link import LinksFilterSet
from links.models import Link
from links.serializers.link import (
    LinkSerializer,
    LinkCreateSerializer
)

LinksPagination = page_number_pagination_factory(
    page_size=30, max_page_size=100
)


class LinksViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    pagination_class = LinksPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinksFilterSet

    def get_queryset(self) -> QuerySet[Link]:
        return Link.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return LinkCreateSerializer

        return LinkSerializer

    def perform_create(self, serializer: LinkCreateSerializer) -> None:
        instance = serializer.save()
        # todo: add celery task to process link and fetch track data
