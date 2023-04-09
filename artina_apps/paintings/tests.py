import django.core.exceptions
import django.test
import django.urls
import parameterized.parameterized

import artists.models
import core.tests
import galleries.models
import paintings.models


class StaticURLTests(django.test.TestCase):
    fixtures = [
        'fixtures/data.json',
    ]

    @parameterized.parameterized.expand(
        [
            ('on_wild_north',),
            ('morning_in_pine_forest',),
            ('rye',),
        ]
    )
    def test_positive_painting_page_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse('paintings:painting', kwargs={'slug': slug})
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница с описанием картины не прогружается',
        )

    @parameterized.parameterized.expand(
        [
            ('black_square',),
            ('morning_in_the_pine_forest',),
            ('authoportret',),
        ]
    )
    def test_negative_painting_page_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse('paintings:painting', kwargs={'slug': slug})
        )
        self.assertEqual(
            response.status_code,
            404,
            'Прогружается страница описания картины, '
            'которой нет в базе данных',
        )


class ModelsTests(django.test.TestCase):
    def setUp(self):
        self.test_artist = artists.models.Artists.objects.create(
            name='Иван',
            surname='Шишкин',
            patronymic='Иванович',
            birth_date=1700,
            death_date=1777,
            short_biography='что то интересное',
            artist_photo='.../...',
            slug='pushkin',
        )
        self.test_gallery = galleries.models.Galleries.objects.create(
            gallery_name='Третьяковка',
            gallery_location='Москва',
            slug='tretyakovka',
            gallery_description='описание',
            gallery_image='../..',
        )
        return super().setUp()

    def create_painting(self, creation_year='1888', width=1000, height=1000):
        self.test_painting = paintings.models.Painting(
            painting_name='Картина',
            painting_artist=self.test_artist,
            painting_gallery=self.test_gallery,
            painting_creation_year=creation_year,
            painting_width=width,
            painting_height=height,
            painting_materials='холст',
            painting_description='описание картины',
            painting_photo='../..',
            slug='painting',
        )

    @parameterized.parameterized.expand(
        [
            (300.8, 300.676),
            (10000, 10000),
            (100, 100),
        ]
    )
    def test_positive_painting_size(self, width, height):
        amount_paintings = paintings.models.Painting.objects.count()
        self.create_painting(width=width, height=height)
        self.test_painting.save()
        self.test_painting.full_clean()
        self.assertEqual(
            paintings.models.Painting.objects.count(),
            amount_paintings + 1,
            'Не создается картина с валидным размером',
        )

    @parameterized.parameterized.expand(
        [
            (9, 100),
            (9999, 10000.2),
            (-1000, -2000),
        ]
    )
    def test_negative_painting_size(self, width, height):
        amount_paintings = paintings.models.Painting.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_painting(width=width, height=height)
            self.test_painting.full_clean()
        self.assertEqual(
            paintings.models.Painting.objects.count(),
            amount_paintings,
            'Создается картина с невалидным размером',
        )

    @parameterized.parameterized.expand(
        [
            (800,),
            (2022,),
            (1777,),
        ]
    )
    def test_positive_painting_creation_year(self, creation_year):
        amount_paintings = paintings.models.Painting.objects.count()
        self.create_painting(creation_year=creation_year)
        self.test_painting.save()
        self.test_painting.full_clean()
        self.assertEqual(
            paintings.models.Painting.objects.count(),
            amount_paintings + 1,
            'Не создается картина с валидным годом создания',
        )

    @parameterized.parameterized.expand(
        [
            (177,),
            (12898,),
            (2024,),
        ]
    )
    def test_negative_painting_creation_year(self, creation_year):
        amount_paintings = paintings.models.Painting.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_painting(creation_year=creation_year)
            self.test_painting.full_clean()
        self.assertEqual(
            paintings.models.Painting.objects.count(),
            amount_paintings,
            'Создается картина с невалидным годом создания',
        )

    def tearDown(self):
        artists.models.Artists.objects.all().delete()
        galleries.models.Galleries.objects.all().delete()
        paintings.models.Painting.objects.all().delete()

        return super().tearDown()


class ContextTests(core.tests.CheckFieldsTestCase):
    fixtures = ['fixtures/data.json']
    slug = paintings.models.Painting.slug.field.name

    def test_painting_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.slug: 'rye'}
            )
        )
        self.assertIn(
            'painting',
            response.context,
            'Информации о картине нет в context',
        )

    def test_painting_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.slug: 'rye'}
            )
        )
        self.assertIsInstance(
            response.context['painting'],
            paintings.models.Painting,
            'Картина не является сущностью модели Painting',
        )

    def test_painting_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.slug: 'rye'}
            )
        )
        self.check_content_value(
            response.context['painting'],
            (
                paintings.models.Painting.painting_name.field.name,
                paintings.models.Painting.painting_creation_year.field.name,
                paintings.models.Painting.painting_materials.field.name,
                paintings.models.Painting.painting_height.field.name,
                paintings.models.Painting.painting_width.field.name,
                paintings.models.Painting.slug.field.name,
                paintings.models.Painting.painting_description.field.name,
                paintings.models.Painting.painting_photo.field.name,
                'painting_artist_id',
                'painting_gallery_id',
                'painting_likes',
            ),
            not_loaded=(
                paintings.models.Painting.painting_artist.field.name,
                paintings.models.Painting.painting_gallery.field.name,
            ),
        )
