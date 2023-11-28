from io import StringIO
from unittest.mock import patch

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase

mock_stdout = patch('sys.stdout', new_callable=StringIO)


class CreateSiteCommandTests(TestCase):

    @mock_stdout
    def test_create_site_domain_already_exists(self, _mock_stdout):
        Site.objects.create(domain='https://example.com', name='Example Site')
        call_command(
            'create_site',
            'https://domain.com',
            'Example Site'
        )
        self.assertFalse(
            Site.objects.filter(domain='https://domain.com').exists()
        )

    @mock_stdout
    def test_create_site_display_name_already_exists(self, _mock_stdout):
        Site.objects.create(domain='https://example.com', name='Example Site')
        call_command(
            'create_site',
            'https://example.com',
            'Example Site'
        )
        self.assertEqual(
            Site.objects.filter(domain='https://example.com').count(),
            1
        )

    @mock_stdout
    def test_create_site_domain_without_http(self, _mock_stdout):
        call_command(
            'create_site',
            'example.com',
            'Example Site'
        )
        self.assertFalse(
            Site.objects.filter(domain='https://example.com').exists()
        )

    @mock_stdout
    def test_create_site_success(self, _mock_stdout):
        call_command(
            'create_site',
            'https://example.com',
            'Example Site'
        )
        self.assertTrue(
            Site.objects.filter(domain='https://example.com').exists()
        )
