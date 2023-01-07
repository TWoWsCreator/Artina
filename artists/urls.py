from django.urls import path

from .views import ArtistsView

app_name = 'artists'
urlpatterns = [
    path('', ArtistsView.as_view(), name='artists')
]
