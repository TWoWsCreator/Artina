from django.views.generic import ListView, TemplateView

from .models import Galleries
from paintings.models import Painting

class GalleriesView(ListView):
    model = Galleries
    template_name = 'galleries/galleries.html'
    context_object_name = 'galleries'

    def get_queryset(self):
        return Galleries.objects.all()


class GalleryView(TemplateView):
    model = Galleries
    template_name = 'galleries/gallery.html'

    def get_context_data(self, **kwargs):
        gallery = Galleries.objects.filter(gallery_slug=self.kwargs['gallery_slug'])[0]
        return {
            'name': gallery.gallery_name,
            'location': gallery.gallery_location,
            'description': gallery.gallery_description,
            'photo': gallery.gallery_image,
            'slug': gallery.gallery_slug
        }


class GalleryPaintingsView(ListView):
    model = Painting
    template_name = 'paintings/paintings.html'
    context_object_name = 'paintings'

    def get_queryset(self):
        gallery = Galleries.objects.filter(
            gallery_slug=self.kwargs['gallery_slug']
        )[0].gallery_name
        paintings = Painting.objects.filter(
            painting_gallery__gallery_name=gallery
        )
        return paintings
