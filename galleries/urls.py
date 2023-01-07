from django.urls import path

from .views import GalleriesView

app_name = 'galleries'
urlpatterns = [
    path('', GalleriesView.as_view(), name='galleries')
]
