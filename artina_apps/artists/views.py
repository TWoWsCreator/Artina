import re

import django.shortcuts
import django.views.generic

import artists.models
import core.views
import paintings.models


class ArtistsView(django.views.generic.ListView):
    template_name = 'artists/artists.html'
    context_object_name = 'artists'
    queryset = artists.models.Artists.objects.get_all_artists()

    def get_queryset(self):
        result_search = self.request.GET.get('search')
        if result_search:
            text_search = re.escape(result_search)
            self.queryset = (
                self.queryset.filter(name__iregex=text_search)
                | self.queryset.filter(surname__iregex=text_search)
                | self.queryset.filter(patronymic__iregex=text_search)
                | self.queryset.filter(birth_date__iregex=text_search)
                | self.queryset.filter(death_date__iregex=text_search)
                | self.queryset.filter(short_biography__iregex=text_search)
            )
        return self.queryset


class ArtistView(django.views.generic.DetailView):
    model = artists.models.Artists
    template_name = 'artists/artist.html'
    queryset = model.objects.all()
    context_object_name = 'artist'

    def get_object(self):
        return self.queryset.get(slug=self.kwargs[self.model.slug.field.name])


class ArtistPaintingsView(django.views.generic.ListView):
    model = artists.models.Artists
    template_name = 'paintings/paintings.html'
    context_object_name = 'paintings'

    def get_queryset(self):
        artist_id = (
            self.model.objects.only(self.model.slug.field.name)
            .get(slug=self.kwargs[self.model.slug.field.name])
            .pk
        )
        painting_objects = paintings.models.Painting.objects
        paintings_artist = painting_objects.get_filter_paintings().filter(
            painting_artist=artist_id
        )
        filter_paintings = core.views.searching_paintings(
            paintings_artist, self.request.GET.get('search')
        )
        return filter_paintings
