from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from links.filters.link_request import LinkRequestsFilterSet
from links.models import LinkRequest
from links.serializers.link_request import LinkRequestSerializer

LinkRequestsPagination = page_number_pagination_factory(
    page_size=30, max_page_size=100
)


class LinkRequestsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    pagination_class = LinkRequestsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinkRequestsFilterSet

    def get_serializer_class(self):
        return LinkRequestSerializer

    def get_queryset(self) -> QuerySet[LinkRequest]:
        return LinkRequest.objects.filter(user=self.request.user).order_by('-created_at')
