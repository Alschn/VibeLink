from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test.utils import override_settings
from friendship.models import Friend
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import UserFactory, FriendshipRequestFactory
from friends.serializers import FriendshipRequestSerializer


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
)
class FriendshipRequestsViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_list_friend_requests(self):
        requests = FriendshipRequestFactory.create_batch(3, to_user=self.user)
        FriendshipRequestFactory.create_batch(1)

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('friends:friendship-requests-list'))
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], len(requests))
        self.assertEqual(
            response_json['results'],
            FriendshipRequestSerializer(requests, many=True).data
        )

    def test_list_sent_friend_requests(self):
        requests = FriendshipRequestFactory.create_batch(3, from_user=self.user)
        FriendshipRequestFactory.create_batch(1)

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('friends:friendship-requests-sent'))
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], len(requests))
        self.assertEqual(
            response_json['results'],
            FriendshipRequestSerializer(requests, many=True).data
        )

    def test_list_received_friend_requests(self):
        requests = FriendshipRequestFactory.create_batch(3, to_user=self.user)
        FriendshipRequestFactory.create_batch(1)

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('friends:friendship-requests-received'))
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], len(requests))
        self.assertEqual(
            response_json['results'],
            FriendshipRequestSerializer(requests, many=True).data
        )

    def test_accept_friend_request(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(to_user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-accept', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_friend_request_self_sender(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-accept', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_accept_friend_request_not_exists(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-accept', args=(1234,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_reject_friend_request(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(to_user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-reject', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reject_friend_request_self_sender(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-reject', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_reject_friend_request_not_exists(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-reject', args=(69,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_cancel_friend_request(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)
        request_id = request.id

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-cancel', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(ObjectDoesNotExist):
            Friend.objects.get(id=request_id)

    def test_cancel_friend_request_receiver(self):
        to_user = UserFactory()
        request = Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(to_user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-cancel', args=(request.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_cancel_friend_request_not_exists(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friendship-requests-cancel', args=(2023,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
