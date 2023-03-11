import django.urls

import paintings.views


app_name = 'paintings'
urlpatterns = [
    django.urls.path(
        '<slug:painting_slug>/',
        paintings.views.PaintingsView.as_view(),
        name='painting',
    ),
    django.urls.path(
        '<slug:painting_slug>/likes/',
        paintings.views.LikePaintingView.as_view(),
        name='likes',
    ),
]
