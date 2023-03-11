import django.contrib

import artists.models


@django.contrib.admin.register(artists.models.Artists)
class ArtistsAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'artist',
        'artist_slug',
        'years_of_life',
        'get_short_biography',
        'image_tmb',
    )
    list_display_links = ('artist',)
