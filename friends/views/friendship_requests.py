from typing import Any

from django.db.models import QuerySet, Q
from django_filters.rest_framework import DjangoFilterBackend
from friendship.models import FriendshipRequest
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.shared.pagination import page_number_pagination_factory
from friends.filters.friendship_request import FriendshipRequestFilterSet
from friends.serializers import FriendshipRequestSerializer

FriendshipRequestsPagination = page_number_pagination_factory(
    page_size=10, max_page_size=100
)


class FriendshipRequestsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = FriendshipRequestsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FriendshipRequestFilterSet

    def get_queryset(self) -> QuerySet[FriendshipRequest]:
        queryset = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).order_by('id')

        if self.action == 'sent_requests':
            return queryset.filter(from_user=self.request.user)

        if self.action == 'received_requests':
            return queryset.filter(to_user=self.request.user)

        if self.action == 'rejected_requests':
            return queryset.filter(
                to_user=self.request.user, rejected__isnull=False
            )

        return queryset.filter(
            Q(to_user=self.request.user) |
            Q(from_user=self.request.user)
        )

    def get_serializer_class(self):
        return FriendshipRequestSerializer

    def get_object(self) -> FriendshipRequest:
        return super().get_object()

    @action(
        detail=False, methods=['GET'],
        url_name='sent', url_path='sent'
    )
    def sent_requests(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)

    @action(
        detail=False, methods=['GET'],
        url_name='received', url_path='received'
    )
    def received_requests(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)

    @action(
        detail=False, methods=['GET'],
        url_name='rejected', url_path='rejected'
    )
    def rejected_requests(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)

    @action(
        detail=True, methods=['POST'],
        url_name='accept', url_path='accept'
    )
    def accept_request(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        friendship_request = self.get_object()

        if friendship_request.to_user != self.request.user:
            return Response(
                {'detail': 'You are not allowed to accept this request!'},
                status=status.HTTP_403_FORBIDDEN
            )

        friendship_request.accept()
        return Response({'message': 'Request accepted!'}, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['POST'],
        url_name='reject', url_path='reject'
    )
    def reject_request(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        friendship_request = self.get_object()

        if friendship_request.to_user != self.request.user:
            return Response(
                {'detail': 'You are not allowed to reject this request!'},
                status=status.HTTP_403_FORBIDDEN
            )

        friendship_request.reject()
        return Response({'message': 'Request rejected!'}, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['POST'],
        url_name='cancel', url_path='cancel'
    )
    def cancel_request(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        friendship_request = self.get_object()

        if friendship_request.from_user != self.request.user:
            return Response(
                {'detail': 'You are not allowed to cancel this request!'},
                status=status.HTTP_403_FORBIDDEN
            )

        friendship_request.cancel()
        return Response({'message': 'Request cancelled!'}, status=status.HTTP_200_OK)
