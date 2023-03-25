import django.test
import django.urls
import parameterized.parameterized

import core.tests
import galleries.models
import paintings.models


class StaticURLTests(django.test.TestCase):
    fixtures = ['fixtures/data.json']
    gallery_slug = galleries.models.Galleries.gallery_slug.field.name

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
                kwargs={self.gallery_slug: gallery_slug},
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
                kwargs={self.gallery_slug: gallery_slug},
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
                'galleries:gallery', kwargs={self.gallery_slug: gallery_slug}
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
                'galleries:gallery', kwargs={self.gallery_slug: gallery_slug}
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
    gallery_slug = galleries.models.Galleries.gallery_slug.field.name

    def test_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertIn(
            'galleries',
            response.context,
            'Списка галерей нет в context',
        )

    def test_amount_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        fail_text = 'Количество галерей на странице не соответствует заданному'
        self.assertEqual(
            len(response.context['galleries']),
            8,
            fail_text,
        )

    def test_sorted_galleries_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertQuerysetEqual(
            galleries.models.Galleries.objects.order_by(
                galleries.models.Galleries.gallery_name.field.name
            ),
            response.context['galleries'],
            msg='Список галерей на странице неосортирован',
        )

    def test_galleries_types(self):
        response = django.test.Client().get(
            django.urls.reverse('galleries:galleries')
        )
        self.assertTrue(
            all(
                isinstance(gallery, galleries.models.Galleries)
                for gallery in response.context['galleries']
            ),
            '(Не все) модели галерей являются сущностями модели Galleries',
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
                ),
                not_loaded=(
                    galleries.models.Galleries.gallery_description.field.name,
                ),
            )

    def test_gallery_page_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.assertIn(
            'gallery',
            response.context,
            'Информации о галереи нет в context',
        )

    def test_gallery_page_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.assertIsInstance(
            response.context['gallery'],
            galleries.models.Galleries,
            'галерея не соответсвует сущности модели Galleries',
        )

    def test_gallery_page_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.check_content_value(
            response.context['gallery'],
            (
                galleries.models.Galleries.gallery_name.field.name,
                galleries.models.Galleries.gallery_location.field.name,
                galleries.models.Galleries.gallery_image.field.name,
                galleries.models.Galleries.gallery_slug.field.name,
                galleries.models.Galleries.gallery_description.field.name,
            ),
        )

    def test_gallery_paintings_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.assertIn(
            'paintings',
            response.context,
            'Списка картин галереи нет в context',
        )

    def test_gallery_paintings_amount_items(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        text_fail = 'Количество картин в галереи не соответствует заданному'
        self.assertEqual(
            len(response.context['paintings']),
            41,
            text_fail,
        )

    def test_gallery_paintings_sorted_items(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.assertQuerysetEqual(
            paintings.models.Painting.objects.filter(
                painting_gallery__gallery_slug='tretyakovskaya'
            ).order_by(paintings.models.Painting.painting_name.field.name),
            response.context['paintings'],
            msg='Список картин на странице галереи неотсортирован',
        )

    def test_gallery_paintings_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        self.assertTrue(
            all(
                isinstance(painting, paintings.models.Painting)
                for painting in response.context['paintings']
            ),
            '(Не все) картин являются сущностями модели Painting',
        )

    def test_gallery_paintings_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'galleries:gallery_paintings',
                kwargs={self.gallery_slug: 'tretyakovskaya'},
            )
        )
        painting_response_context = response.context['paintings']
        creation_year = paintings.models.Painting.painting_creation_year
        for painting in painting_response_context:
            self.check_content_value(
                painting,
                (
                    paintings.models.Painting.painting_name.field.name,
                    paintings.models.Painting.painting_size.field.name,
                    paintings.models.Painting.painting_photo.field.name,
                    creation_year.field.name,
                    paintings.models.Painting.painting_slug.field.name,
                ),
                not_loaded=(
                    paintings.models.Painting.painting_artist.field.name,
                    paintings.models.Painting.painting_gallery.field.name,
                    paintings.models.Painting.painting_description.field.name,
                    paintings.models.Painting.painting_materials.field.name,
                ),
            )
