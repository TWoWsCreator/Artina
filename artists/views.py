from django.views.generic import TemplateView


class ArtistsView(TemplateView):
    template_name = 'artists/artists.html'
