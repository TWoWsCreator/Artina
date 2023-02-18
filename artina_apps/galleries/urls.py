from django.urls import path

from .views import GalleriesView, GalleryPaintingsView, GalleryView

app_name = 'galleries'
urlpatterns = [
    path('', GalleriesView.as_view(), name='galleries'),
    path('<slug:gallery_slug>/', GalleryView.as_view(), name='gallery'),
    path(
        'paintings/<slug:gallery_slug>/',
        GalleryPaintingsView.as_view(),
        name='gallery_paintings',
    ),
]
