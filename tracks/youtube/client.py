from django.conf import settings
from googleapiclient.discovery import build


def get_youtube_client():
    return build(
        'youtube',
        'v3',
        developerKey=settings.GOOGLE_CLOUD_API_KEY
    )
