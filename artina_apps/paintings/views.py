import django.db.models
import django.shortcuts
import django.urls
import django.views.generic

import paintings.models


class PaintingView(django.views.generic.DetailView):
    model = paintings.models.Painting
    template_name = 'paintings/painting.html'
    context_object_name = 'painting'
    queryset = model.objects.get_painting()

    def get_object(self):
        return self.queryset.get(slug=self.kwargs[self.model.slug.field.name])


class LikePaintingView(django.views.generic.FormView):
    model = paintings.models.Painting

    def post(self, request, **kwargs):
        slug = kwargs[paintings.models.Painting.slug.field.name]
        slug_field = paintings.models.Painting.slug.field.name
        success_url = django.urls.reverse_lazy(
            'paintings:painting', kwargs={slug_field: slug}
        )
        response = django.shortcuts.get_object_or_404(
            paintings.models.Painting.objects.filter(slug=slug)
        )
        if request.user.is_authenticated:
            if request.user in response.likes.all():
                response.likes.remove(request.user)
            else:
                response.likes.add(request.user)
        else:
            return django.shortcuts.redirect(
                django.urls.reverse_lazy('users:login')
            )
        response.save()
        return django.shortcuts.redirect(success_url)
