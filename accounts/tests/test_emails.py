import email
from io import StringIO
from unittest.mock import patch

from allauth.account.forms import default_token_generator
from allauth.account.models import EmailConfirmationHMAC, EmailAddress
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

from accounts.adapters import AccountAdapter
from core.shared.factories import UserFactory

mock_stdout = patch('sys.stdout', new_callable=StringIO)


# todo: in memory email backend + spy on render_mail (instead of reading from stdout)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    USE_SMTP=False,
    FRONTEND_SITE_NAME='VibeLink',
    DEFAULT_FROM_EMAIL='vibelink@example.com'
)
class AuthEmailsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.email_address = EmailAddress.objects.create(
            user=cls.user,
            email=cls.user.email,
            primary=True,
            verified=True
        )
        cls.frontend_site = Site.objects.create(
            name='VibeLink',
            domain='http://localhost:3000'
        )
        cls.adapter = AccountAdapter()

    def test_send_confirmation_signup_mail(self):
        email_confirmation = EmailConfirmationHMAC(self.email_address)
        with mock_stdout as stdout:
            self.adapter.send_confirmation_mail(
                None,
                email_confirmation,
                signup=True,
            )

        url = self.adapter.get_email_confirmation_url(None, email_confirmation)
        ctx = {
            "user": self.user,
            "activate_url": url,
            "current_site": self.frontend_site,
            "key": email_confirmation.key,
        }

        message = self.adapter.render_mail(
            self.adapter.email_confirmation_template,
            self.email_address.email,
            ctx,
        )
        email_from_stdout = email.message_from_string(stdout.getvalue())

        self.assertEqual(email_from_stdout.get('subject'), message.subject)
        # todo: assert email body

    def test_send_confirmation_mail(self):
        email_confirmation = EmailConfirmationHMAC(self.email_address)
        with mock_stdout as stdout:
            self.adapter.send_confirmation_mail(
                None,
                email_confirmation,
                signup=False,
            )

        url = self.adapter.get_email_confirmation_url(
            None,
            email_confirmation,
        )
        ctx = {
            'current_site': self.frontend_site,
            'user': self.user,
            'password_reset_url': url,
            'request': None,
        }

        message = self.adapter.render_mail(
            self.adapter.email_confirmation_template,
            self.email_address.email,
            ctx,
        )
        email_from_stdout = email.message_from_string(stdout.getvalue())

        self.assertEqual(email_from_stdout.get('subject'), message.subject)
        # todo: assert email body

    def test_send_password_reset_mail(self):
        with mock_stdout as stdout:
            self.adapter.send_password_reset_mail(
                None,
                self.user.email,
                self.user,
            )

        url = self.adapter.get_password_reset_url(
            None,
            self.user.pk,
            token=default_token_generator.make_token(self.user),
        )
        ctx = {
            'current_site': self.frontend_site,
            'user': self.user,
            'password_reset_url': url,
            'request': None,
        }

        message = self.adapter.render_mail(
            self.adapter.password_reset_template,
            self.email_address.email,
            ctx,
        )
        email_from_stdout = email.message_from_string(stdout.getvalue())

        self.assertEqual(email_from_stdout.get('subject'), message.subject)
        # todo: assert email body
