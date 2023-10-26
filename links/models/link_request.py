from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        verbose_name = _('Link Request')
        verbose_name_plural = _('Link Requests')
