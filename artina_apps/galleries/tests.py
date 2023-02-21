from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_galleries_endpoint(self):
        response = Client().get(reverse('galleries:galleries'))
        self.assertEqual(response.status_code, 200)

    # def test_paintings_gallery_endpoint(self):
    #     response = Client().get('/galleries/paintings/new/')
    #     self.assertEqual(response.status_code, 200)
