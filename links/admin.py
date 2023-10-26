from django.contrib import admin

from links.models import Link, LinkRequest


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(LinkRequest)
class LinkRequestAdmin(admin.ModelAdmin):
    pass
