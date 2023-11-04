from rest_framework.routers import DefaultRouter

from links.views.link_requests import LinkRequestsViewSet
from links.views.links import LinksViewSet

router = DefaultRouter()
router.register('link-requests', LinkRequestsViewSet, basename='link-requests')
router.register('links', LinksViewSet, basename='links')

urlpatterns = router.urls
