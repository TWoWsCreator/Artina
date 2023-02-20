from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from users.models import CustomUser

from .models import Painting


class PaintingsView(ListView):
    model = Painting
    template_name = 'paintings/painting.html'
    context_object_name = 'painting'

    def get_context_data(self, **kwargs):
        painting = Painting.objects.filter(
            painting_slug=self.kwargs['painting_slug']
        ).first()
        
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


class LikePaintingView(FormView):
    model = Painting

    @staticmethod
    def get_queryset():
        return Painting.objects.select_related(
            'painting_artist', 'painting_gallery'
        ).prefetch_related(
            Prefetch(
                'likes',
                queryset=CustomUser.objects.all(),
                to_attr='painting_likes',
            ),
        )

    def post(self, request, **kwargs):
        painting_slug = kwargs['painting_slug']
        success_url = reverse_lazy(
            'paintings:painting', kwargs={'painting_slug': painting_slug}
        )
        response = get_object_or_404(
            self.get_queryset().filter(painting_slug=painting_slug)
        )
        if request.user.is_authenticated:
            if request.user in response.likes.all():
                response.likes.remove(request.user)
            else:
                response.likes.add(request.user)
        else:
            return redirect(reverse_lazy('users:login'))
        response.save()
        return redirect(success_url)
