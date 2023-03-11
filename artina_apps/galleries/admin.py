import django.contrib

import galleries.models


class GalleryPhotosAdmin(django.contrib.admin.TabularInline):
    fk_name = 'gallery_photos'
    model = galleries.models.GalleryPhotos


@django.contrib.admin.register(galleries.models.Galleries)
class GalleriesAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'gallery_name',
        'gallery_location',
        'gallery_slug',
        'get_short_description',
        'image_tmb',
    )
    list_display_links = ('gallery_name',)

    inlines = [GalleryPhotosAdmin]
