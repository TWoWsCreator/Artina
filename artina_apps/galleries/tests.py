from django.test import Client, TestCase
from django.urls import reverse

from parameterized import parameterized


class StaticURLTests(TestCase):
    fixtures = ['fixtures/data.json']

    def test_galleries_endpoint(self):
        response = Client().get(reverse('galleries:galleries'))
        self.assertEqual(response.status_code, 200,
                         'Страница галерей не прогружается')

    @parameterized.expand(
        [
            ('tretyakovskaya',),
            ('state_russian_museum',),
            ('serpuhovskiy_art_museum',),
        ]
    )
    def test_positive_galleries_painting_endpoint(self, gallery_slug):
        response = Client().get(reverse('galleries:gallery_paintings',
                                        kwargs={'gallery_slug': gallery_slug}))
        self.assertEqual(response.status_code, 200,
                         'Страница картин галереи не прогружается')

    @parameterized.expand(
        [
            ('tretyakovskaya_1',),
            ('state_arabic_museum',),
            ('volhskiy_art_museum',),
        ]
    )
    def test_negative_galleries_painting_endpoint(self, gallery_slug):
        response = Client().get(reverse('galleries:gallery_paintings',
                                        kwargs={'gallery_slug': gallery_slug}))
        self.assertEqual(response.status_code, 404,
                         'Прогружается страница картин галереи, '
                         'которой нет в базе данных')

    @parameterized.expand(
        [
            ('private_collections',),
            ('tulskiy_art_museum',),
            ('russian_museum_pushkin',),
        ]
    )
    def test_positive_galleries_page_endpoint(self, gallery_slug):
        response = Client().get(reverse('galleries:gallery',
                                        kwargs={'gallery_slug': gallery_slug}))
        self.assertEqual(response.status_code, 200,
                         'Страница истории галереи не прогружается')

    @parameterized.expand(
        [
            ('russian_museum',),
            ('new_museum',),
            ('art_museum',),
        ]
    )
    def test_negative_galleries_page_endpoint(self, gallery_slug):
        response = Client().get(reverse('galleries:gallery',
                                        kwargs={'gallery_slug': gallery_slug}))
        self.assertEqual(response.status_code, 404,
                         'Прогружается страница истории галереи, '
                         'которой нет в базе данных')
