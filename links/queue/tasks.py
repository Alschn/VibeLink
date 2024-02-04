import logging

from django.db.models import Q

from accounts.models import User
from links.emails import send_link_requests_email_notifications
from links.models import Link, LinkRequest
from tracks.spotify.actions import gather_spotify_metadata
from tracks.youtube.actions import gather_youtube_metadata

logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)


def generate_link_requests() -> list[int]:
    users = User.objects.filter(is_active=True)
    link_requests = [LinkRequest.objects.create(user=user) for user in users]
    link_requests_ids = [link_request.id for link_request in link_requests]

    link_requests_qs = LinkRequest.objects.filter(
        id__in=link_requests_ids,
    ).select_related('user').filter(
        # todo: filter user settings (send_daily_link_request_email=True)
        ~Q(user__email__exact=''),
        user__email__isnull=False,
    )

    send_link_requests_email_notifications(link_requests_qs)

    return link_requests_ids


def gather_metadata_for_link(link: Link) -> dict:
    if link.source_type == Link.SourceType.SPOTIFY:
        return gather_spotify_metadata(link)

    elif link.source_type == Link.SourceType.YOUTUBE:
        return gather_youtube_metadata(link)

    logger.info(
        'Unknown link source type: %s for link: %s',
        link.source_type,
        link.url
    )
    return {}
