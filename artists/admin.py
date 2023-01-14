from django.contrib import admin

from .models import Artists


# class ArtistGalleryInline(admin.TabularInline):
#     model = ArtistsGallery
#     fk_name = 'artist_gallery'


@admin.register(Artists)
class ArtistsAdmin(admin.ModelAdmin):
    list_display = ('artist', 'artist_slug', 'years_of_life', 'get_short_biography', 'image_tmb')
    list_display_links = ('artist',)

    # inlines = [ArtistGalleryInline]
