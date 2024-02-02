import typing

if typing.TYPE_CHECKING:
    from accounts.models import User


def send_link_requests_email_notifications(users: typing.Iterable['User']) -> None:
    """Send email notifications to users about newly created link requests."""

    # todo: implement
