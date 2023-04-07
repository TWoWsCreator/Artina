import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import artists.urls
import download.urls
import feedback.urls
import galleries.urls
import homepage.urls
import paintings.urls
import users.urls

urlpatterns = [
    django.urls.path('', django.urls.include(homepage.urls)),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('artists/', django.urls.include(artists.urls)),
    django.urls.path('download/', django.urls.include(download.urls)),
    django.urls.path('feedback/', django.urls.include(feedback.urls)),
    django.urls.path('galleries/', django.urls.include(galleries.urls)),
    django.urls.path('paintings/', django.urls.include(paintings.urls)),
    django.urls.path('users/', django.urls.include(users.urls)),
    django.urls.path('users/', django.urls.include(django.contrib.auth.urls)),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            '__debug__/', django.urls.include(debug_toolbar.urls)
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
