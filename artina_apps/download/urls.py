import django.urls

import download.views

app_name = 'download'

urlpatterns = [
    django.urls.path(
        '<path:download_path>',
        download.views.DownloadView.as_view(),
        name='image',
    )
]
