from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from core.views import searching_paintings

from paintings.models import Painting

from .models import Artists


class ArtistsView(ListView):
    model = Artists
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
        artists = Artists.objects.all()
        result_search = self.request.GET.get('search')
        if result_search:
            return artists.filter(
                Q(artist__iregex=result_search)
                | Q(years_of_life__iregex=result_search)
                | Q(short_biography__iregex=result_search)
            )
        else:
            return artists


class ArtistView(TemplateView):
    model = Artists
    template_name = 'artists/artist.html'

    def get_context_data(self, **kwargs):
        artist = get_object_or_404(
            Artists, artist_slug=self.kwargs['artist_slug']
        )
        return {
            'artist': artist.artist,
            'years_of_life': artist.years_of_life,
            'artist_photo': artist.artist_photo,
            'biography': artist.short_biography,
            'slug': artist.artist_slug,
        }


class ArtistPaintingsView(ListView):
    model = Painting
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

    def get_queryset(self, **kwargs):
        artist = get_object_or_404(
            Artists, artist_slug=self.kwargs['artist_slug']
        ).artist
        paintings = Painting.objects.filter(painting_artist__artist=artist)
        result_search = self.request.GET.get('search')
        filter_paintings = searching_paintings(paintings, result_search)
        return filter_paintings
