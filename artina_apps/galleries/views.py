from django.db.models import Q
from django.views.generic import ListView, TemplateView

from core.views import searching_paintings

from paintings.models import Painting

from .models import Galleries, GalleryPhotos


class GalleriesView(ListView):
    model = Galleries
    template_name = 'galleries/galleries.html'
    context_object_name = 'galleries'

    def get_template_names(self):
        search = self.request.GET.get('search')
        if search:
            if search[-1] == '\\':
                return 'includes/danger.html'
            else:
                return 'galleries/galleries.html'
        else:
            return 'galleries/galleries.html'

    def get_queryset(self):
        galleries = Galleries.objects.all()
        result_search = self.request.GET.get('search')
        if result_search:
            return galleries.filter(
                Q(gallery_name__iregex=result_search)
                | Q(gallery_description__iregex=result_search)
                | Q(gallery_location__iregex=result_search)
            )
        else:
            return Galleries.objects.all()


class GalleryView(TemplateView):
    model = Galleries
    template_name = 'galleries/gallery.html'

    def get_context_data(self, **kwargs):
        gallery = Galleries.objects.filter(
            gallery_slug=self.kwargs['gallery_slug']
        )[0]
        photos = GalleryPhotos.objects.filter(gallery_photos=gallery).order_by(
            'gallery_photos_id'
        )
        return {
            'name': gallery.gallery_name,
            'location': gallery.gallery_location,
            'description': gallery.gallery_description,
            'photo': gallery.gallery_image,
            'slug': gallery.gallery_slug,
            'photos': photos,
        }


class GalleryPaintingsView(ListView):
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

    def get_queryset(self):
        result_search = self.request.GET.get('search')
        gallery = Galleries.objects.filter(
            gallery_slug=self.kwargs['gallery_slug']
        ).first().gallery_name
        paintings = Painting.objects.filter(
            painting_gallery__gallery_name=gallery
        )
        filter_paintings = searching_paintings(paintings, result_search)
        return filter_paintings
