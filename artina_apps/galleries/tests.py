import django.test
import django.urls
import parameterized.parameterized

import core.tests
import galleries.models


class StaticURLTests(django.test.TestCase):
    fixtures = ['fixtures/data.json']

    def test_galleries_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertEqual(
            response.status_code, 200, 'Страница галерей не прогружается'
        )

    @parameterized.parameterized.expand(
        [
            ('tretyakovskaya',),
            ('state_russian_museum',),
            ('serpuhovskiy_art_museum',),
        ]
    )
    def test_positive_galleries_painting_endpoint(self, gallery_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={'gallery_slug': gallery_slug},
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница картин галереи не прогружается',
        )

    @parameterized.parameterized.expand(
        [
            ('tretyakovskaya_1',),
            ('state_arabic_museum',),
            ('volhskiy_art_museum',),
        ]
    )
    def test_negative_galleries_painting_endpoint(self, gallery_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={'gallery_slug': gallery_slug},
            )
        )
        self.assertEqual(
            response.status_code,
            404,
            'Прогружается страница картин галереи, '
            'которой нет в базе данных',
        )

    @parameterized.parameterized.expand(
        [
            ('private_collections',),
            ('tulskiy_art_museum',),
            ('russian_museum_pushkin',),
        ]
    )
    def test_positive_galleries_page_endpoint(self, gallery_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery', kwargs={'gallery_slug': gallery_slug}
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница истории галереи не прогружается',
        )

    @parameterized.parameterized.expand(
        [
            ('russian_museum',),
            ('new_museum',),
            ('art_museum',),
        ]
    )
    def test_negative_galleries_page_endpoint(self, gallery_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery', kwargs={'gallery_slug': gallery_slug}
            )
        )
        self.assertEqual(
            response.status_code,
            404,
            'Прогружается страница истории галереи, '
            'которой нет в базе данных',
        )


class ModelsTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ('Третьяковка', 'Москва', 'tretyakovka', 'описание', '../'),
            ('Национальный музей', 'Петербург', 'russian_museum', 'ок', '/.'),
            ('Тульская галерея', 'Тула', 'art_museum', 'тула', '/../'),
        ]
    )
    def test_create_gallery(self, name, location, slug, description, image):
        amount_galleries = galleries.models.Galleries.objects.count()
        gallery = galleries.models.Galleries(
            gallery_name=name,
            gallery_location=location,
            gallery_slug=slug,
            gallery_description=description,
            gallery_image=image,
        )
        gallery.full_clean()
        gallery.save()
        self.assertEqual(
            galleries.models.Galleries.objects.count(),
            amount_galleries + 1,
            'Объект галереи не создается',
        )

    def tearDown(self):
        galleries.models.Galleries.objects.all().delete()
        return super().tearDown()


class ContextTests(core.tests.CheckFieldsTestCase):
    fixtures = ['fixtures/data.json']

    def test_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertIn('galleries', response.context)

    def test_amount_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertEqual(len(response.context['galleries']), 8)

    def test_sorted_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertQuerysetEqual(galleries.models.Galleries.objects.order_by(
            galleries.models.Galleries.gallery_name.field.name
        ),
            response.context['galleries'])

    def test_galleries_types(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertTrue(
            all(
                isinstance(
                    gallery,
                    galleries.models.Galleries
                )
                for gallery in response.context['galleries']
            )
        )

    def test_galleries_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        for gallery in response.context['galleries']:
            self.check_content_value(
                gallery,
                (
                    galleries.models.Galleries.gallery_name.field.name,
                    galleries.models.Galleries.gallery_location.field.name,
                    galleries.models.Galleries.gallery_image.field.name,
                    galleries.models.Galleries.gallery_slug.field.name,
                )
            )

    def test_gallery_page_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:gallery',
                                kwargs={'gallery_slug': 'tretyakovskaya'})
        )
        self.assertIn('gallery', response.context)

    def test_gallery_page_types(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:gallery',
                                kwargs={'gallery_slug': 'tretyakovskaya'})
        )
        self.assertIsInstance(response.context['gallery'],
                              galleries.models.Galleries)
