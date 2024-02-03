from unittest.mock import patch

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.test import TestCase

from emails.backends import DjangoQBackend, send_message
from emails.serialization import email_to_dict

patch_create_async_task = patch('emails.backends.create_async_task')


class DjangoQEmailBackendTests(TestCase):

    @patch_create_async_task
    def test_send_messages_creates_async_task(self, mock_create_async_task):
        message = EmailMessage(
            subject='Subject',
            body='Body',
            from_email='test@example.com',
            to=['test1@example.com']
        )
        dict_message = email_to_dict(message)

        backend = DjangoQBackend()
        backend.use_dicts = True
        backend.send_messages([message])

        mock_create_async_task.assert_called_once_with(send_message, dict_message)

    @patch_create_async_task
    def test_send_messages_creates_multiple_async_tasks(self, mock_create_async_task):
        message1 = EmailMessage(
            subject='Subject',
            body='Body',
            from_email='test@example.com',
            to=['test1@example.com']
        )
        message2 = EmailMultiAlternatives(
            subject='Subject',
            body='Body',
            from_email='test@example.com',
            to=['test1@example.com']
        )
        message2.attach_alternative('<body>Hello world!</body>', 'text/html')

        backend = DjangoQBackend()
        backend.use_dicts = True
        backend.send_messages([message1, message2])

        self.assertEqual(mock_create_async_task.call_count, 2)

    @patch_create_async_task
    def test_send_messages_creates_async_task_use_dicts_false(self, mock_create_async_task):
        message = EmailMessage(
            subject='Subject',
            body='Body',
            from_email='test@example.com',
            to=['test1@example.com']
        )

        backend = DjangoQBackend()
        backend.use_dicts = False
        backend.send_messages([message])

        mock_create_async_task.assert_called_once_with(send_message, message)
