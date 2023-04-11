import django.contrib

import paintings.models


class PainintgFactsAdmin(django.contrib.admin.TabularInline):
    model = paintings.models.PaintingFacts


@django.contrib.admin.register(paintings.models.Painting)
class PaintingsAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        paintings.models.Painting.painting_name.field.name,
        paintings.models.Painting.slug.field.name,
        paintings.models.Painting.painting_artist.field.name,
        paintings.models.Painting.image_tmb,
    )
    list_display_links = (paintings.models.Painting.painting_name.field.name,)

    inlines = (PainintgFactsAdmin,)
