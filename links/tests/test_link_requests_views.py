from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import UserFactory, LinkRequestFactory
from links.models import LinkRequest
from links.serializers.link_request import LinkRequestSerializer


class LinkRequestsViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_list_link_requests(self):
        LinkRequestFactory.create_batch(3, user=self.user)
        LinkRequestFactory.create_batch(2)

        expected_queryset = LinkRequest.objects.filter(user=self.user).order_by('-created_at')

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('links:link-requests-list'))
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(
            response_json['results'],
            LinkRequestSerializer(expected_queryset, many=True).data
        )
