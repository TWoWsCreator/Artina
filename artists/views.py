from django.views.generic import ListView, TemplateView

from paintings.models import Painting
from .models import Artists


class ArtistsView(ListView):
    model = Artists
    template_name = 'artists/artists.html'
    context_object_name = 'artists'

    def get_queryset(self):
        return Artists.objects.all()


class ArtistView(TemplateView):
    model = Artists
    template_name = 'artists/artist.html'
    # context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        artist = Artists.objects.filter(artist_slug=self.kwargs['artist_slug'])[0]
        return {
            'artist': artist.artist,
            'years_of_life': artist.years_of_life,
            'artist_photo': artist.artist_photo,
            'biography': artist.short_biography,
            'slug': artist.artist_slug
        }


class ArtistPaintingsView(ListView):
    model = Painting
    template_name = 'paintings/paintings.html'
    context_object_name = 'paintings'

    def get_queryset(self, **kwargs):
        artist = Artists.objects.filter(artist_slug=self.kwargs['artist_slug'])[0].artist
        paintings = Painting.objects.filter(painting_artist__artist=artist)
        return paintings
