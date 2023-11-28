from unittest.mock import patch, MagicMock

from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.utils import jwt_encode
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase, override_settings

from accounts.models import User
from core.shared.factories import UserFactory, DEFAULT_USER_FACTORY_PASSWORD

patch_adapter_send_confirmation_mail = patch('accounts.adapters.AccountAdapter.send_confirmation_mail')
patch_adapter_send_password_reset_mail = patch('accounts.adapters.AccountAdapter.send_password_reset_mail')


@override_settings(
    CACHES={
        'default': {
            # disable rate limiting on auth views
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
)
class AuthAPIViewsTests(APITestCase):
    logout_url = reverse_lazy('accounts:logout')
    token_url = reverse_lazy('accounts:token')
    token_verify_url = reverse_lazy('accounts:token_verify')
    token_refresh_url = reverse_lazy('accounts:token_refresh')
    password_change_url = reverse_lazy('accounts:password_change')
    password_reset_url = reverse_lazy('accounts:password_reset')
    password_reset_confirm_url = reverse_lazy('accounts:password_reset_confirm')
    register_url = reverse_lazy('accounts:register')
    register_verify_url = reverse_lazy('accounts:register_verify_email')
    register_confirm_url = reverse_lazy('accounts:register_resend_email')

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_email = EmailAddress.objects.create(
            user=cls.user,
            email=cls.user.email,
            primary=True,
            verified=True,
        )

    def test_login(self):
        response = self.client.post(self.token_url, data={
            'username': self.user.username,
            'password': DEFAULT_USER_FACTORY_PASSWORD,
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_json)
        self.assertIn('refresh', response_json)
        self.assertIn('user', response_json)
        # default dj-rest-auth serializer
        serializer = UserDetailsSerializer(instance=self.user)
        self.assertEqual(response_json['user'], serializer.data)

    def test_login_email_not_verified(self):
        user = UserFactory()
        response = self.client.post(self.token_url, data={
            'username': user.username,
            'password': DEFAULT_USER_FACTORY_PASSWORD,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    def test_login_wrong_password(self):
        response = self.client.post(self.token_url, data={
            'username': self.user.username,
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    def test_login_wrong_username(self):
        response = self.client.post(self.token_url, data={
            'username': 'wrong_username',
            'password': DEFAULT_USER_FACTORY_PASSWORD,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    def test_login_with_email(self):
        response = self.client.post(self.token_url, data={
            'email': self.user.email,
            'password': DEFAULT_USER_FACTORY_PASSWORD,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    @patch_adapter_send_confirmation_mail
    def test_register(self, mock_send_confirmation_mail: MagicMock):
        response = self.client.post(self.register_url, data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password1': 'new_password',
            'password2': 'new_password',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.json())

        mock_send_confirmation_mail.assert_called_once()

        user = User.objects.get(username='test1')
        email_address = EmailAddress.objects.get(user=user)
        self.assertTrue(email_address.primary)
        self.assertFalse(email_address.verified)

    def test_register_passwords_mismatch(self):
        response = self.client.post(self.register_url, data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password1': 'new_password',
            'password2': 'wrong_password',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    def test_register_password_too_short(self):
        response = self.client.post(self.register_url, data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password1': 'axc',
            'password2': 'axc',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.json())

    def test_register_password_too_common(self):
        response = self.client.post(self.register_url, data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password1': 'admin123',
            'password2': 'admin123',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.json())

    def test_register_verify_email(self):
        user = UserFactory()
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=False,
        )
        key_sent_via_email = EmailConfirmationHMAC(email_address).key
        response = self.client.post(self.register_verify_url, {
            'key': key_sent_via_email,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

        email_address.refresh_from_db()
        self.assertTrue(email_address.verified)

    def test_register_verify_email_wrong_key(self):
        response = self.client.post(self.register_verify_url, {
            'key': 'wrong_key',
        })
        # 404 is thrown by allauth (ConfirmEmailView.get)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    @patch_adapter_send_confirmation_mail
    def test_register_resend_email(self, mock_send_confirmation: MagicMock):
        user = UserFactory()
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=False,
        )
        response = self.client.post(self.register_confirm_url, {
            'email': email_address.email,
        })
        mock_send_confirmation.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

    def test_register_resend_email_no_email_provided(self):
        response = self.client.post(self.register_confirm_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    @patch_adapter_send_confirmation_mail
    def test_register_resend_email_wrong_email(self, mock_send_confirmation: MagicMock):
        fake_email = 'fake.email@example.com'
        response = self.client.post(self.register_confirm_url, {
            'email': fake_email,
        })
        user_email_exists = (
            User.objects.filter(email=fake_email).exists() or
            EmailAddress.objects.filter(email=fake_email).exists()
        )
        mock_send_confirmation.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(user_email_exists)

    @patch_adapter_send_confirmation_mail
    def test_register_resend_email_already_verified(self, mock_send_confirmation: MagicMock):
        user = UserFactory()
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True,
        )
        response = self.client.post(self.register_confirm_url, {
            'email': email_address.email,
        })
        mock_send_confirmation.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

    def test_password_change(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(self.password_change_url, data={
            'old_password': DEFAULT_USER_FACTORY_PASSWORD,
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

    def test_password_change_passwords_mismatch(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(self.password_change_url, data={
            'new_password1': 'new_password',
            'new_password2': 'wrong_password',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response.json())

    def test_password_change_password_too_short(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(self.password_change_url, data={
            'new_password1': 'axc',
            'new_password2': 'axc',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response.json())

    def test_password_change_password_too_common(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(self.password_change_url, data={
            'new_password1': 'admin123',
            'new_password2': 'admin123',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response.json())

    @patch_adapter_send_password_reset_mail
    def test_password_reset(self, mock_send_password_reset_mail: MagicMock):
        user = UserFactory()
        response = self.client.post(self.password_reset_url, data={
            'email': user.email,
        })
        mock_send_password_reset_mail.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

    def test_password_reset_no_email_provided(self):
        response = self.client.post(self.password_reset_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())

    @patch_adapter_send_password_reset_mail
    def test_password_reset_wrong_email(self, mock_send_password_reset_mail: MagicMock):
        fake_email = 'fake.email@example.com'
        response = self.client.post(self.password_reset_url, data={
            'email': fake_email,
        })
        mock_send_password_reset_mail.assert_not_called()
        user_email_exists = (
            User.objects.filter(email=fake_email).exists() or
            EmailAddress.objects.filter(email=fake_email).exists()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())
        self.assertFalse(user_email_exists)

    @freeze_time('2020-01-01 00:00:00')
    def test_password_reset_confirm(self):
        uid_from_email = user_pk_to_url_str(self.user)
        token_from_email = default_token_generator.make_token(self.user)

        new_password = 'new_password_123'
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': self.user.pk,
            'token': token_from_email,
            'new_password1': new_password,
            'new_password2': new_password,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password_123'))

    def test_password_reset_confirm_missing_data(self):
        response = self.client.post(self.password_reset_confirm_url, {})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('uid', response_json)
        self.assertIn('token', response_json)
        self.assertIn('new_password1', response_json)
        self.assertIn('new_password2', response_json)

    def test_password_reset_confirm_passwords_mismatch(self):
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': user_pk_to_url_str(self.user),
            'token': token,
            'new_password1': 'new_password_123',
            'new_password2': 'new_password_321',
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response_json)

    def test_password_reset_confirm_password_too_short(self):
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': user_pk_to_url_str(self.user),
            'token': token,
            'new_password1': 'axc',
            'new_password2': 'axc',
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response_json)

    def test_password_reset_confirm_password_too_long(self):
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': user_pk_to_url_str(self.user),
            'token': token,
            'new_password1': 'a' * 129,
            'new_password2': 'a' * 129,
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response_json)

    def test_password_reset_confirm_password_too_common(self):
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': user_pk_to_url_str(self.user),
            'token': token,
            'new_password1': 'admin123',
            'new_password2': 'admin123',
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password2', response_json)

    def test_logout(self):
        _, refresh = jwt_encode(self.user)
        response = self.client.post(self.logout_url, data={
            'refresh': str(refresh),
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.json())

    def test_logout_no_token(self):
        response = self.client.post(self.logout_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())

    def test_logout_wrong_token(self):
        response = self.client.post(self.logout_url, data={
            'refresh': 'wrong_token',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())
