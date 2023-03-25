import django.test
import django.urls
import parameterized.parameterized


class StatictTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ('artists/ge.jpg',),
            ('galleries/pushkin_1.jpg',),
            ('galleries/ulyanovck_art_museum.jpeg',),
            ('artists/perov.jpeg',),
        ]
    )
    def test_download_endpoint(self, path):
        response = django.test.Client().get(
            django.urls.reverse(
                'download:image', kwargs={'download_path': path}
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница загрузки картинки не открывается',
        )
