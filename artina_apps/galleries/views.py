import re

import django.db.models
import django.shortcuts
import django.views.generic

import core.views
import galleries.models
import paintings.models


class GalleriesView(django.views.generic.ListView):
    template_name = 'galleries/galleries.html'
    context_object_name = 'galleries'
    queryset = galleries.models.Galleries.objects.get_all_galleries()

    def get_queryset(self):
        result_search = self.request.GET.get('search')
        if result_search:
            text_search = re.escape(result_search)
            self.queryset = (
                self.queryset.filter(gallery_name__iregex=text_search)
                | self.queryset.filter(gallery_description__iregex=text_search)
                | self.queryset.filter(gallery_location__iregex=text_search)
            )
        return self.queryset


class GalleryView(django.views.generic.DetailView):
    model = galleries.models.Galleries
    template_name = 'galleries/gallery.html'
    queryset = galleries.models.Galleries.objects.get_gallery_with_photos()
    context_object_name = 'gallery'

    def get_object(self):
        return self.queryset.get(slug=self.kwargs[self.model.slug.field.name])


class GalleryPaintingsView(django.views.generic.ListView):
    model = galleries.models.Galleries
    template_name = 'paintings/paintings.html'
    context_object_name = 'paintings'

    def get_queryset(self):
        result_search = self.request.GET.get('search')
        gallery_id = (
            self.model.objects.only(self.model.slug.field.name)
            .get(slug=self.kwargs[self.model.slug.field.name])
            .pk
        )
        painting_objects = paintings.models.Painting.objects
        gallery_paintings = painting_objects.get_filter_paintings().filter(
            painting_gallery=gallery_id
        )
        return core.views.searching_paintings(gallery_paintings, result_search)
