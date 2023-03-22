import django.conf
import django.http
import django.views.generic


class DownloadView(django.views.generic.View):
    def get(self, request, **kwargs):
        download_path = kwargs['download_path']
        return django.http.FileResponse(
            open(
                django.conf.settings.MEDIA_ROOT / download_path,
                'rb',
            ),
            as_attachment=True,
        )
