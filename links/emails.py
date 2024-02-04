import typing
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from core.shared.frontend import get_frontend_site

if typing.TYPE_CHECKING:
    from links.models import LinkRequest

NEW_LINK_REQUEST_SUBJECT_TEMPLATE = 'emails/links/new_link_request_subject.txt'
NEW_LINK_REQUEST_MESSAGE_TEMPLATE = 'emails/links/new_link_request_message.txt'


def send_link_requests_email_notifications(link_requests: typing.Iterable['LinkRequest']) -> None:
    """Send email notifications to users about newly created link requests."""

    emails = build_new_link_request_emails(link_requests)

    for email in emails:
        email.send()


def build_new_link_request_emails(link_requests: typing.Iterable['LinkRequest']) -> list[EmailMessage]:
    frontend_site = get_frontend_site()

    body_ctx = {
        'current_site': frontend_site,
    }
    subject = render_to_string(NEW_LINK_REQUEST_SUBJECT_TEMPLATE).strip()

    messages = []

    for link_request in link_requests:
        frontend_url = urljoin(
            frontend_site.domain,
            f'link-requests/{link_request.id}/'
        )

        body = render_to_string(
            NEW_LINK_REQUEST_MESSAGE_TEMPLATE,
            {**body_ctx, 'frontend_url': frontend_url}
        )

        message = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[link_request.user.email],
        )
        messages.append(message)

    return messages
