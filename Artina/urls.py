from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', namespace='homepage')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('galleries/', include('galleries.urls')),
    path('artists/', include('artists.urls')),
    path('feedback/', include('feedback.urls'))
]
