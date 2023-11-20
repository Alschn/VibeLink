from typing import Any

from celery.result import AsyncResult
from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.shared.pagination import page_number_pagination_factory
from links.filters.link import LinksFilterSet
from links.models import Link
from links.queue.tasks import gather_metadata_for_link
from links.serializers.link import (
    LinkSerializer,
    LinkCreateSerializer,
    LinkCreateResultSerializer
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

    @transaction.atomic
    def perform_create(self, serializer: LinkCreateSerializer) -> tuple[Link, str]:
        instance: Link = serializer.save()
        result: AsyncResult = gather_metadata_for_link.delay(link_id=instance.id)
        return instance, result.id

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: LinkCreateResultSerializer,
        }
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, task_id = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data, 'task_id': task_id},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
