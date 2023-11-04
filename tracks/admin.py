from django.contrib import admin

from tracks.models import Track, Author


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
