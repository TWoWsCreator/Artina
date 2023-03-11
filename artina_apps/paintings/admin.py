import django.contrib

import paintings.models


@django.contrib.admin.register(paintings.models.Painting)
class PaintingsAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'painting_name',
        'painting_slug',
        'painting_artist',
        'get_painting_description',
        'image_tmb',
    )
    list_display_links = ('painting_name',)
