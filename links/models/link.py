from django.db import models
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    class SourceType(models.TextChoices):
        YOUTUBE = 'YT', _('YouTube')
        SPOTIFY = 'SP', _('Spotify')
        UNKNOWN = 'UN', _('Unknown')

    title = models.CharField(max_length=127)
    description = models.TextField(max_length=1000, blank=True, default='')
    url = models.URLField()
    source_type = models.CharField(choices=SourceType.choices, max_length=2)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='links'
    )
    track = models.ForeignKey(
        'tracks.Track',
        on_delete=models.PROTECT,
        related_name='links',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')
