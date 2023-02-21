from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_artists_endpoint(self):
        response = Client().get(reverse('artists:artists'))
        self.assertEqual(response.status_code, 200)
