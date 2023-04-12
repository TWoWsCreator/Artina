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
        return django.shortcuts.get_object_or_404(
            self.queryset, slug=self.kwargs[self.slug_field]
        )

    def post(self, request, **kwargs):
        painting_slug = kwargs[self.slug_field]
        response = django.shortcuts.get_object_or_404(
            self.model.objects.filter(slug=painting_slug)
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
        return django.shortcuts.redirect(
            django.urls.reverse_lazy(
                'paintings:painting', kwargs={self.slug_field: painting_slug}
            )
        )
