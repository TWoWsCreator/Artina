from django.contrib import admin

from .models import Galleries, GalleryPhotos


class GalleryPhotosAdmin(admin.TabularInline):
    fk_name = 'gallery_photos'
    model = GalleryPhotos


@admin.register(Galleries)
class GalleriesAdmin(admin.ModelAdmin):
    list_display = ('gallery_name', 'gallery_location', 'gallery_slug',
                    'get_short_description', 'image_tmb')
    list_display_links = ('gallery_name',)

    inlines = [GalleryPhotosAdmin]
