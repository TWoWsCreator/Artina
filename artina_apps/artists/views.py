import re

import django.shortcuts
import django.views.generic

import artists.models
import core.views
import paintings.models


class ArtistsView(django.views.generic.ListView):
    model = artists.models.Artists
    context_object_name = 'artists'

    def get_template_names(self):
        search = self.request.GET.get('search')
        if search:
            if search[-1] == '\\':
                return 'includes/danger.html'
            else:
                return 'artists/artists.html'
        else:
            return 'artists/artists.html'

    def get_queryset(self):
        artists_page = artists.models.Artists.objects.all()
        result_search = self.request.GET.get('search')
        if result_search:
            artists_page = (
                artists_page.filter(
                    short_biography__iregex=re.escape(result_search)
                )
                | artists_page.filter(
                    birth_date__iregex=re.escape(result_search)
                )
                | artists_page.filter(
                    death_date__iregex=re.escape(result_search)
                )
                | artists_page.filter(
                    short_biography__iregex=re.escape(result_search)
                )
            )
        return artists_page.only(
            artists.models.Artists.artist.field.name,
            artists.models.Artists.birth_date.field.name,
            artists.models.Artists.death_date.field.name,
            artists.models.Artists.alived.field.name,
            artists.models.Artists.artist_photo.field.name,
            artists.models.Artists.artist_slug.field.name,
        ).order_by(artists.models.Artists.artist.field.name)


class ArtistView(django.views.generic.TemplateView):
    model = artists.models.Artists
    template_name = 'artists/artist.html'

    def get_context_data(self, **kwargs):
        artist = django.shortcuts.get_object_or_404(
            artists.models.Artists,
            artist_slug=kwargs[artists.models.Artists.artist_slug.field.name],
        )
        return {'artist': artist}


class ArtistPaintingsView(django.views.generic.ListView):
    model = paintings.models.Painting
    context_object_name = 'paintings'

    def get_template_names(self):
        search = self.request.GET.get('search')
        if search:
            if search[-1] == '\\':
                return 'includes/danger.html'
            else:
                return 'paintings/paintings.html'
        else:
            return 'paintings/paintings.html'

    def get_queryset(self):
        artist = django.shortcuts.get_object_or_404(
            artists.models.Artists.objects.only(
                artists.models.Artists.artist_slug.field.name
            ),
            artist_slug=self.kwargs[
                artists.models.Artists.artist_slug.field.name
            ],
        ).pk
        paintings_artist = paintings.models.Painting.objects.filter(
            painting_artist=artist
        )
        result_search = self.request.GET.get('search')
        filter_paintings = (
            core.views.searching_paintings(paintings_artist, result_search)
            .only(
                paintings.models.Painting.painting_name.field.name,
                paintings.models.Painting.painting_size.field.name,
                paintings.models.Painting.painting_photo.field.name,
                paintings.models.Painting.painting_creation_year.field.name,
                paintings.models.Painting.painting_slug.field.name,
            )
            .order_by(paintings.models.Painting.painting_name.field.name)
        )
        return filter_paintings
