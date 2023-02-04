from django.urls import path

from .views import PaintingsView, LikePaintingView


app_name = 'paintings'
urlpatterns = [
    path('<slug:painting_slug>/', PaintingsView.as_view(), name='painting'),
    path('<slug:painting_slug>/likes/', LikePaintingView.as_view(), name='likes')
]
