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
        artists_search = artists.models.Artists.objects.all()
        result_search = self.request.GET.get('search')
        if result_search:
            return (
                artists_search.filter(artist__iregex=result_search)
                | artists_search.filter(years_of_life__iregex=result_search)
                | artists_search.filter(short_biography__iregex=result_search)
            )
        else:
            return artists_search


class ArtistView(django.views.generic.TemplateView):
    model = artists.models.Artists
    template_name = 'artists/artist.html'

    def get_context_data(self, **kwargs):
        artist = django.shortcuts.get_object_or_404(
            artists.models.Artists,
            artist_slug=kwargs[artists.models.Artists.artist_slug.field.name]
        )
        return {
            'artist': artist.artist,
            'years_of_life': artist.years_of_life,
            'artist_photo': artist.artist_photo,
            'biography': artist.short_biography,
            'slug': artist.artist_slug,
        }


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
            artists.models.Artists, artist_slug=self.kwargs[
                artists.models.Artists.artist_slug.field.name]
        ).pk
        paintings_artist = paintings.models.Painting.objects.filter(
            painting_artist=artist)
        result_search = self.request.GET.get('search')
        filter_paintings = core.views.searching_paintings(
            paintings_artist,
            result_search
        )
        return filter_paintings
