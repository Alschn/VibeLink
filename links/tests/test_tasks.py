from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from freezegun import freeze_time

from accounts.models import User
from core.shared.factories import UserFactory
from core.shared.tasks import get_function_module_path
from links.models import LinkRequest
from links.queue.schedules import schedule_generate_link_requests
from links.queue.tasks import generate_link_requests


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_STORE_EAGER_RESULTS=True,
    CELERY_BROKER_URL='memory://',
)
class LinkRequestsTasksTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    @patch('links.queue.tasks.send_link_requests_email_notifications')
    def test_generate_link_requests_task(self, mock_emails: MagicMock):
        UserFactory.create_batch(2)
        users = User.objects.all()

        ids = generate_link_requests()
        queryset = LinkRequest.objects.filter(user_id__in=users.values_list('id', flat=True))

        self.assertEqual(len(ids), queryset.count())
        self.assertTrue(mock_emails.called)

    @freeze_time('2021-01-01 00:00:00')
    @patch('random.randint')
    def test_schedule_generate_link_requests_task(self, mock_random: MagicMock):
        mock_random.return_value = 6000
        now = timezone.now()
        random_time = now + timezone.timedelta(seconds=mock_random.return_value)

        schedule_generate_link_requests()

        task_name = 'generate-link-requests-' + random_time.strftime('%Y-%m-%d-%H-%M-%S')

        self.assertTrue(
            ClockedSchedule.objects.filter(clocked_time=random_time).exists()
        )
        self.assertTrue(
            PeriodicTask.objects.filter(
                name=task_name,
                task=get_function_module_path(generate_link_requests),
                one_off=True,
                start_time=random_time,
            ).exists()
        )
