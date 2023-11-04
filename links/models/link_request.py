import typing

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if typing.TYPE_CHECKING:
    from links.models import Link


class LinkRequest(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='link_requests'
    )
    link = models.ForeignKey(
        'links.Link',
        on_delete=models.SET_NULL,
        related_name='requests',
        blank=True, null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    fulfilled_at = models.DateTimeField(blank=True, null=True)

    def add_link(self, link: 'Link') -> None:
        self.link = link
        self.fulfilled_at = timezone.now()
        self.save()

    class Meta:
        verbose_name = _('Link Request')
        verbose_name_plural = _('Link Requests')
