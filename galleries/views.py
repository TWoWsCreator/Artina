from django.views.generic import TemplateView


class GalleriesView(TemplateView):
    template_name = 'galleries/galleries.html'
