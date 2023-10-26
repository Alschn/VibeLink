from rest_framework.routers import DefaultRouter

from friends.views import (
    FriendsViewSet,
    FriendshipRequestsViewSet,
)

router = DefaultRouter()
router.register('friends', FriendsViewSet, basename='friends')
router.register('friendship-requests', FriendshipRequestsViewSet, basename='friendship-requests')

urlpatterns = router.urls
