import django.test
import django.urls


class StaticURLTests(django.test.TestCase):
    def test_feedback_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertEqual(
            response.status_code, 200, 'Страница обратной связи не октрывается'
        )
