import django.urls

import artists.views

app_name = 'artists'
urlpatterns = [
    django.urls.path('', artists.views.ArtistsView.as_view(), name='artists'),
    django.urls.path(
        '<slug:artist_slug>/',
        artists.views.ArtistView.as_view(),
        name='artist',
    ),
    django.urls.path(
        'paintings/<slug:artist_slug>/',
        artists.views.ArtistPaintingsView.as_view(),
        name='artist_painting',
    ),
]
