from rest_framework.routers import DefaultRouter

from links.views.link_requests import LinkRequestsViewSet

router = DefaultRouter()
router.register('link-requests', LinkRequestsViewSet, basename='link-requests')

urlpatterns = router.urls
