import django.db.models
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
            all_galleries = all_galleries.filter(
                all_galleries.filter(gallery_name__iregex=result_search)
                | all_galleries.filter(
                    gallery_description__iregex=result_search
                )
                | all_galleries.filter(gallery_location__iregex=result_search)
            )
        return all_galleries.only(
            galleries.models.Galleries.gallery_name.field.name,
            galleries.models.Galleries.gallery_location.field.name,
            galleries.models.Galleries.gallery_image.field.name,
            galleries.models.Galleries.gallery_slug.field.name,
        )


class GalleryView(django.views.generic.TemplateView):
    model = galleries.models.Galleries
    template_name = 'galleries/gallery.html'

    def get_context_data(self, **kwargs):
        gallery_photos = galleries.models.GalleryPhotos.objects.only(
            galleries.models.GalleryPhotos.photo.field.name,
            galleries.models.GalleryPhotos.gallery_photos_id.field.name,
        )
        gallery_photos_field = galleries.models.GalleryPhotos.gallery_photos
        gallery_queryset = galleries.models.Galleries.objects.prefetch_related(
            django.db.models.Prefetch(
                gallery_photos_field.field.related_query_name(),
                queryset=gallery_photos,
            ),
        )
        gallery = django.shortcuts.get_object_or_404(
            gallery_queryset,
            gallery_slug=kwargs[
                galleries.models.Galleries.gallery_slug.field.name
            ],
        )
        return {'gallery': gallery}


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
            galleries.models.Galleries.objects.only(
                galleries.models.Galleries.gallery_slug.field.name
            ),
            gallery_slug=self.kwargs[
                galleries.models.Galleries.gallery_slug.field.name
            ],
        ).pk
        paintings_gallery = paintings.models.Painting.objects.filter(
            painting_gallery=gallery
        ).only(
            paintings.models.Painting.painting_name.field.name,
            paintings.models.Painting.painting_size.field.name,
            paintings.models.Painting.painting_photo.field.name,
            paintings.models.Painting.painting_creation_year.field.name,
            paintings.models.Painting.painting_slug.field.name,
        )
        filter_paintings = core.views.searching_paintings(
            paintings_gallery, result_search
        )
        return filter_paintings
