import django.urls

import paintings.views


app_name = 'paintings'
urlpatterns = [
    django.urls.path(
        '<slug:slug>/',
        paintings.views.PaintingView.as_view(),
        name='painting',
    ),
]
