import django.contrib

import artists.models


@django.contrib.admin.register(artists.models.Artists)
class ArtistsAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        artists.models.Artists.artist.field.name,
        artists.models.Artists.artist_slug.field.name,
        artists.models.Artists.birth_date.field.name,
        artists.models.Artists.death_date.field.name,
        artists.models.Artists.get_short_biography,
        artists.models.Artists.image_tmb,
    )
    list_display_links = (artists.models.Artists.artist.field.name,)
