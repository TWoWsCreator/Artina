import django.urls

import galleries.views

app_name = 'galleries'
urlpatterns = [
    django.urls.path(
        '', galleries.views.GalleriesView.as_view(), name='galleries'
    ),
    django.urls.path(
        '<slug:slug>/',
        galleries.views.GalleryView.as_view(),
        name='gallery',
    ),
    django.urls.path(
        'paintings/<slug:slug>/',
        galleries.views.GalleryPaintingsView.as_view(),
        name='gallery_paintings',
    ),
]
