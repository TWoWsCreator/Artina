import django.db.models
import django.shortcuts
import django.urls
import django.views.generic

import artists.models
import galleries.models
import paintings.models
import users.models


class PaintingsView(django.views.generic.ListView):
    model = paintings.models.Painting
    template_name = 'paintings/painting.html'
    context_object_name = 'painting'

    def get_context_data(self):
        painting = django.shortcuts.get_object_or_404(
            paintings.models.Painting.objects.select_related(
                paintings.models.Painting.painting_artist.field.name,
                paintings.models.Painting.painting_gallery.field.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    paintings.models.Painting.likes.field.name,
                    queryset=users.models.CustomUser.objects.all(),
                    to_attr='painting_likes',
                )
            )
            .only(
                paintings.models.Painting.painting_name.field.name,
                paintings.models.Painting.painting_creation_year.field.name,
                paintings.models.Painting.painting_materials.field.name,
                paintings.models.Painting.painting_size.field.name,
                paintings.models.Painting.slug.field.name,
                paintings.models.Painting.painting_description.field.name,
                paintings.models.Painting.painting_photo.field.name,
                f'{paintings.models.Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.name.field.name}',
                f'{paintings.models.Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.surname.field.name}',
                f'{paintings.models.Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.patronymic.field.name}',
                f'{paintings.models.Painting.painting_gallery.field.name}__'
                f'{galleries.models.Galleries.gallery_name.field.name}',
            ),
            slug=self.kwargs[
                paintings.models.Painting.slug.field.name
            ],
        )
        return {'painting': painting}


class LikePaintingView(django.views.generic.FormView):
    model = paintings.models.Painting

    def post(self, request, **kwargs):
        slug = kwargs[
            paintings.models.Painting.slug.field.name
        ]
        slug_field = paintings.models.Painting.slug.field.name
        success_url = django.urls.reverse_lazy(
            'paintings:painting', kwargs={slug_field: slug}
        )
        response = django.shortcuts.get_object_or_404(
            paintings.models.Painting.objects.filter(
                slug=slug
            )
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
