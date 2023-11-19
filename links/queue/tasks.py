import logging

from celery import shared_task

logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def generate_link_requests() -> list[int]:
    from accounts.models import User
    from links.models import LinkRequest
    from links.emails import send_link_requests_email_notifications

    users = User.objects.all()
    link_requests = [LinkRequest.objects.create(user=user) for user in users]

    # todo: email notifications
    send_link_requests_email_notifications(users)

    return [link_request.id for link_request in link_requests]


@shared_task
def gather_metadata_for_link(url: str, source_type: str) -> dict:
    from links.models import Link
    from tracks.spotify.actions import gather_spotify_metadata

    if source_type == Link.SourceType.SPOTIFY:
        return gather_spotify_metadata(url)

    elif source_type == Link.SourceType.YOUTUBE:
        # todo: implement later
        return {}

    return {}
