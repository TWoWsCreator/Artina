import django.urls

import galleries.views

app_name = 'galleries'
urlpatterns = [
    django.urls.path(
        '', galleries.views.GalleriesView.as_view(), name='galleries'
    ),
    django.urls.path(
        '<slug:gallery_slug>/',
        galleries.views.GalleryView.as_view(),
        name='gallery',
    ),
    django.urls.path(
        'paintings/<slug:gallery_slug>/',
        galleries.views.GalleryPaintingsView.as_view(),
        name='gallery_paintings',
    ),
]
