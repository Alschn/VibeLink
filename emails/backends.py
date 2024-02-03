from typing import Any

from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend
from django.utils.module_loading import import_string

from core.shared.tasks import create_async_task
from emails.serialization import email_to_dict, dict_to_email

DEFAULT_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = getattr(settings, 'DJANGO_Q_EMAIL_BACKEND', DEFAULT_BACKEND)
EMAIL_ERROR_HANDLER = getattr(settings, 'DJANGO_Q_EMAIL_ERROR_HANDLER', None)
DJANGO_Q_EMAIL_USE_DICTS = getattr(settings, 'DJANGO_Q_EMAIL_USE_DICTS', True)


class DjangoQBackend(BaseEmailBackend):
    use_dicts = DJANGO_Q_EMAIL_USE_DICTS

    def send_messages(self, email_messages: Any) -> int:
        num_sent = 0
        for email_message in email_messages:
            if self.use_dicts:
                email_message = email_to_dict(email_message)

            create_async_task(send_message, email_message)

            num_sent += 1
        return num_sent


def send_message(email_message: Any) -> None:
    """
    Sends the specified email synchronously.
    See DjangoQBackend for sending in the background.
    """
    try:
        if isinstance(email_message, dict):
            email_message = dict_to_email(email_message)

        connection = email_message.connection
        email_message.connection = get_connection(backend=EMAIL_BACKEND)
        try:
            email_message.send()
        finally:
            email_message.connection = connection

    except Exception as ex:
        if not EMAIL_ERROR_HANDLER:
            raise

        email_error_handler = import_string(EMAIL_ERROR_HANDLER)
        email_error_handler(email_message, ex)
