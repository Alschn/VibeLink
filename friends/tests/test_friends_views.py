from django.test import TestCase
from django.test.utils import override_settings
from friendship.models import Friend, FriendshipRequest
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import UserFactory, FriendFactory
from friends.serializers import FriendSerializer


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
)
class FriendsViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_list_friends(self):
        friends = FriendFactory.create_batch(3, from_user=self.user)
        FriendFactory.create_batch(1)

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('friends:friends-list'))
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], len(friends))
        self.assertEqual(
            response_json['results'],
            FriendSerializer(friends, many=True).data
        )

    def test_retrieve_friend(self):
        friend = FriendFactory.create(from_user=self.user)

        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('friends:friends-detail', args=(friend.id,))
        )
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, FriendSerializer(friend).data)

    def test_retrieve_user_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('friends:friends-detail', args=(420,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_retrieve_friend_not_friend(self):
        not_our_friend = FriendFactory.create()

        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('friends:friends-detail', args=(not_our_friend.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_add_friend(self):
        to_user = UserFactory()

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friends-list'),
            data={'to_user': to_user.id, 'message': 'Hi!'},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Friend.objects.are_friends(self.user, to_user))

        friend_request = FriendshipRequest.objects.get(
            from_user=self.user,
            to_user=to_user,
        )

        self.assertIn(friend_request, Friend.objects.sent_requests(self.user))
        self.assertEqual(friend_request.message, 'Hi!')

    def test_add_friend_already_friends(self):
        to_user = UserFactory()
        req = Friend.objects.add_friend(self.user, to_user)
        req.accept()

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friends-list'),
            data={'to_user': to_user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_user', response.json())

    def test_add_friend_already_sent(self):
        to_user = UserFactory()
        Friend.objects.add_friend(self.user, to_user)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friends-list'),
            data={'to_user': to_user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_user', response.json())

    def test_add_friend_self(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friends-list'),
            data={'to_user': self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_user', response.json())

    def test_add_friend_user_not_found(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse_lazy('friends:friends-list'),
            data={'to_user': 2137},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_user', response.json())

    def test_remove_friend(self):
        to_user = UserFactory()
        req = Friend.objects.add_friend(self.user, to_user)
        req.accept()

        friend = Friend.objects.get(from_user=self.user, to_user=to_user)

        self.client.force_login(self.user)
        response = self.client.delete(
            reverse_lazy('friends:friends-detail', args=(friend.id,)),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Friend.objects.are_friends(self.user, to_user))

    def test_remove_friend_not_friend(self):
        not_our_friend = FriendFactory()

        self.client.force_login(self.user)
        response = self.client.delete(
            reverse_lazy('friends:friends-detail', args=(not_our_friend.id,)),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_remove_friend_not_found(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            reverse_lazy('friends:friends-detail', args=(1337,)),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
