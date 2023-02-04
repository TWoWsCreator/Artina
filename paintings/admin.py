from django.contrib import admin

from .models import Painting


@admin.register(Painting)
class PaintingsAdmin(admin.ModelAdmin):
    list_display = ('painting_name', 'painting_slug', 'painting_artist',
                    'get_painting_description', 'image_tmb')
    list_display_links = ('painting_name',)
