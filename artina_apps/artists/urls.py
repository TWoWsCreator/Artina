from django.urls import path

from .views import ArtistPaintingsView, ArtistView, ArtistsView

app_name = 'artists'
urlpatterns = [
    path('', ArtistsView.as_view(), name='artists'),
    path('<slug:artist_slug>/', ArtistView.as_view(), name='artist'),
    path(
        'paintings/<slug:artist_slug>/',
        ArtistPaintingsView.as_view(),
        name='artist_painting',
    ),
]
