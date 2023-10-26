from django.contrib import admin

from links.models import Link, LinkRequest


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'title', 'url', 'source_type',
    )
    list_select_related = ('user',)
    list_filter = ('source_type',)
    search_fields = ('title', 'url')


@admin.register(LinkRequest)
class LinkRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'created_at', 'link', 'fulfilled_at'
    )
    list_select_related = ('user', 'link')
