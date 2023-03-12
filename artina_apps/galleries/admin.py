import django.contrib

import galleries.models


class GalleryPhotosAdmin(django.contrib.admin.TabularInline):
    # fk_name = 'gallery_photos'
    model = galleries.models.GalleryPhotos


@django.contrib.admin.register(galleries.models.Galleries)
class GalleriesAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        galleries.models.Galleries.gallery_name.field.name,
        galleries.models.Galleries.gallery_location.field.name,
        galleries.models.Galleries.gallery_slug.field.name,
        galleries.models.Galleries.get_short_description,
        galleries.models.Galleries.image_tmb,
    )
    list_display_links = (galleries.models.Galleries.gallery_name.field.name,)

    inlines = [GalleryPhotosAdmin]
