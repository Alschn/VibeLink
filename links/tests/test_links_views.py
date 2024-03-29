from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from core.shared.factories import UserFactory, LinkRequestFactory, LinkFactory
from links.models import Link
from links.serializers.link import LinkSerializer

patch_create_async_task = patch('links.views.links.create_async_task', return_value=None)


class LinksViewSetTests(TestCase):
    links_list_url = reverse_lazy('links:links-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_list_links(self):
        LinkFactory.create_batch(3, user=self.user)
        LinkFactory.create_batch(2)

        expected_queryset = Link.objects.filter(user=self.user).order_by('-created_at')

        self.client.force_login(self.user)
        response = self.client.get(self.links_list_url)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], expected_queryset.count())
        self.assertEqual(
            response_json['results'],
            LinkSerializer(expected_queryset, many=True).data,
        )

    @patch_create_async_task
    def test_create_link_youtube(self, mock_async_task):
        link_request = LinkRequestFactory(user=self.user)
        song_url = 'https://www.youtube.com/watch?v=bwQDEvTcvUg&ab_channel=Narkopop'

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'Youtube link',
                'description': 'Test',
                'url': song_url,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_async_task.assert_called_once()

        source_type = response_json['source_type']
        self.assertEqual(Link.SourceType(source_type), Link.SourceType.YOUTUBE)

        link_id = response_json['id']
        link = Link.objects.get(id=link_id)

        link_request.refresh_from_db()
        self.assertEqual(link_request.link, link)
        self.assertIsNotNone(link_request.fulfilled_at)
        self.assertIn('task_id', response_json)

    @patch_create_async_task
    def test_create_link_spotify(self, mock_async_task):
        link_request = LinkRequestFactory(user=self.user)
        song_url = 'https://open.spotify.com/track/5CTNmaXOY1nSnIUsxCpiyU?si=b395d83e839544b1'

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'Spotify link',
                'url': song_url,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_async_task.assert_called_once()

        link_id = response_json['id']
        self.assertTrue(Link.objects.filter(id=link_id).exists())

        source_type = response_json['source_type']
        self.assertEqual(Link.SourceType(source_type), Link.SourceType.SPOTIFY)
        self.assertIn('task_id', response_json)

    @patch_create_async_task
    def test_create_link_other_source(self, mock_async_task):
        link_request = LinkRequestFactory(user=self.user)
        song_url = 'https://soundcloud.com/hahaahahahahah/controlla'

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'Soundcloud link (not supported yet)',
                'url': song_url,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_async_task.assert_called_once()

        link_id = response_json['id']
        self.assertTrue(Link.objects.filter(id=link_id).exists())

        source_type = response_json['source_type']
        self.assertEqual(Link.SourceType(source_type), Link.SourceType.UNKNOWN)
        self.assertIn('task_id', response_json)

    def test_create_link_invalid_url(self):
        link_request = LinkRequestFactory(user=self.user)

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'Soundcloud link (not supported yet)',
                'url': 'XDDD',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('url', response.json())

    def test_create_link_invalid_link_request_id(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': 1234,
                'title': 'Sentino - Lato (Majki Bootleg)',
                'url': 'https://www.youtube.com/watch?v=B7p2D52lZ68',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('link_request', response.json())

    def test_create_link_link_request_does_not_belong_to_user(self):
        link_request = LinkRequestFactory()

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'MUZA DO BICIA ŻONY (tylko dla prawdziwych mężczyzn)',
                'url': 'https://www.youtube.com/watch?v=t2mL8ynHni4&t=602s&ab_channel=TuWstawNazwe',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('link_request', response.json())

    def test_create_link_http(self):
        link_request = LinkRequestFactory(user=self.user)
        url = 'http://localhost:8000'

        validator = URLValidator(schemes=Link.ALLOWED_SCHEMES)
        with self.assertRaises(ValidationError):
            validator(url)

        self.client.force_login(self.user)
        response = self.client.post(
            self.links_list_url,
            data={
                'link_request': link_request.id,
                'title': 'HTTP link test',
                'url': url
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('url', response.json())
