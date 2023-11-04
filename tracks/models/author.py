from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField


class Author(models.Model):
    name = models.CharField(max_length=100)
    meta = JSONField(
        schema={
            'type': 'dict',
            'keys': {},
            'additionalProperties': True,
        },
        blank=True,
        default=dict,
        help_text=_('Additional information fetched from external source in JSON format')
    )

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
