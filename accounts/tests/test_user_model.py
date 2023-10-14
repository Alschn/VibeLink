from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import User


class UserModelTests(TestCase):

    def test_get_user_model(self):
        django_user_model = get_user_model()
        self.assertEqual(django_user_model, User)
