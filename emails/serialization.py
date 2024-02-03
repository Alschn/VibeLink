from typing import Any

from django.core.mail.message import EmailMessage, EmailMultiAlternatives


def email_to_dict(email_message: Any) -> dict:
    """
    Converts the specified email message to a dictionary representation.
    """
    if type(email_message) not in [EmailMessage, EmailMultiAlternatives, dict]:
        raise ValueError(
            'The email_message argument must be an instance of '
            'EmailMessage, EmailMultiAlternatives or dict.'
        )

    if isinstance(email_message, dict):
        return email_message

    email_message_data = {
        'subject': email_message.subject,
        'body': email_message.body,
        'from_email': email_message.from_email,
        'to': email_message.to,
        'bcc': email_message.bcc,
        'attachments': email_message.attachments,
        'headers': email_message.extra_headers,
        'cc': None,
        'reply_to': None,
    }

    if isinstance(email_message, EmailMultiAlternatives):
        email_message_data['alternatives'] = email_message.alternatives

    return email_message_data


def dict_to_email(email_message_data: dict) -> EmailMessage | EmailMultiAlternatives:
    """
    Creates an EmailMessage or EmailMultiAlternatives instance from the
    specified dictionary.
    """
    kwargs = {**email_message_data}
    alternatives = kwargs.pop('alternatives', None)
    return (
        EmailMessage(**kwargs) if not alternatives else
        EmailMultiAlternatives(alternatives=alternatives, **kwargs)
    )
