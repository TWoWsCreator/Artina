import django.shortcuts
import django.views.generic

import core.views
import galleries.models
import paintings.models


class GalleriesView(django.views.generic.ListView):
    model = galleries.models.Galleries
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
        all_galleries = galleries.models.Galleries.objects.all()
        result_search = self.request.GET.get('search')
        if result_search:
            return all_galleries.filter(
                all_galleries.filter(gallery_name__iregex=result_search)
                | all_galleries.filter(
                    gallery_description__iregex=result_search
                )
                | all_galleries.filter(gallery_location__iregex=result_search)
            )
        else:
            return galleries.models.Galleries.objects.all()


class GalleryView(django.views.generic.TemplateView):
    model = galleries.models.Galleries
    template_name = 'galleries/gallery.html'

    def get_context_data(self, **kwargs):
        gallery = django.shortcuts.get_object_or_404(
            galleries.models.Galleries,
            gallery_slug=self.kwargs['gallery_slug'],
        )
        photos = galleries.models.GalleryPhotos.objects.filter(
            gallery_photos=gallery
        ).order_by('gallery_photos_id')
        return {
            'name': gallery.gallery_name,
            'location': gallery.gallery_location,
            'description': gallery.gallery_description,
            'photo': gallery.gallery_image,
            'slug': gallery.gallery_slug,
            'photos': photos,
        }


class GalleryPaintingsView(django.views.generic.ListView):
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
        result_search = self.request.GET.get('search')
        gallery = django.shortcuts.get_object_or_404(
            galleries.models.Galleries,
            gallery_slug=self.kwargs['gallery_slug'],
        ).gallery_name
        paintings_gallery = paintings.models.Painting.objects.filter(
            painting_gallery__gallery_name=gallery
        )
        filter_paintings = core.views.searching_paintings(
            paintings_gallery, result_search
        )
        return filter_paintings
