import django.test
import django.urls


class StaticURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('homepage:home')
        )
        self.assertEqual(
            response.status_code, 200, 'Главная страница не открывается'
        )
