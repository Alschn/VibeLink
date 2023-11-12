from typing import Iterable

from accounts.models import User


def send_link_requests_email_notifications(users: Iterable[User]) -> None:
    """Send email notifications to users about newly created link requests."""

    # todo: implement
