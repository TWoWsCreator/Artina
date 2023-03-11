import django.db.models
import django.shortcuts
import django.urls
import django.views.generic

import paintings.models
import users.models


class PaintingsView(django.views.generic.ListView):
    model = paintings.models.Painting
    template_name = 'paintings/painting.html'
    context_object_name = 'painting'

    def get_context_data(self, **kwargs):
        painting = django.shortcuts.get_object_or_404(
            paintings.models.Painting,
            painting_slug=self.kwargs['painting_slug'],
        )

        return {
            'name': painting.painting_name,
            'size': painting.painting_size,
            'creation_year': painting.painting_creation_year,
            'photo': painting.painting_photo,
            'artist': painting.painting_artist,
            'description': painting.painting_description,
            'materials': painting.painting_materials,
            'gallery': painting.painting_gallery,
            'slug': painting.painting_slug,
            'likes': painting.likes.all(),
        }


class LikePaintingView(django.views.generic.FormView):
    model = paintings.models.Painting

    @staticmethod
    def get_queryset():
        return paintings.models.Painting.objects.select_related(
            'painting_artist', 'painting_gallery'
        ).prefetch_related(
            django.db.models.Prefetch(
                'likes',
                queryset=users.models.CustomUser.objects.all(),
                to_attr='painting_likes',
            ),
        )

    def post(self, request, **kwargs):
        painting_slug = kwargs['painting_slug']
        success_url = django.urls.reverse_lazy(
            'paintings:painting', kwargs={'painting_slug': painting_slug}
        )
        response = django.shortcuts.get_object_or_404(
            self.get_queryset().filter(painting_slug=painting_slug)
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
