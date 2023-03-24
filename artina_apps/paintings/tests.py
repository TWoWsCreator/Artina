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
    def test_positive_painting_page_endpoint(self, painting_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={'painting_slug': painting_slug}
            )
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
    def test_negative_painting_page_endpoint(self, painting_slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={'painting_slug': painting_slug}
            )
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
            artist='М. В. Васнецов',
            years_of_life='1700-1777',
            short_biography='что то интересное',
            artist_photo='.../...',
            artist_slug='pushkin',
        )
        self.test_gallery = galleries.models.Galleries.objects.create(
            gallery_name='Третьяковка',
            gallery_location='Москва',
            gallery_slug='tretyakovka',
            gallery_description='описание',
            gallery_image='../..',
        )
        return super().setUp()

    def create_painting(self, creation_year='1888', size='300x300'):
        self.test_painting = paintings.models.Painting(
            painting_name='Картина',
            painting_artist=self.test_artist,
            painting_gallery=self.test_gallery,
            painting_creation_year=creation_year,
            painting_size=size,
            painting_materials='холст',
            painting_description='описание картины',
            painting_photo='../..',
            painting_slug='painting',
        )

    @parameterized.parameterized.expand(
        [
            ('300x300',),
            ('1300x1300',),
            ('11232x10000',),
        ]
    )
    def test_positive_painting_size(self, size):
        amount_paintings = paintings.models.Painting.objects.count()
        self.create_painting(size=size)
        self.test_painting.save()
        self.test_painting.full_clean()
        self.assertEqual(
            paintings.models.Painting.objects.count(),
            amount_paintings + 1,
            'Не создается картина с валидным размером',
        )

    @parameterized.parameterized.expand(
        [
            ('100х111',),
            ('300*300',),
            ('300+300',),
            ('300x300x300',),
            ('x300',),
            ('300x',),
        ]
    )
    def test_negative_painting_size(self, size):
        amount_paintings = paintings.models.Painting.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_painting(size=size)
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
            (2023,),
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
    painting_slug = paintings.models.Painting.painting_slug.field.name

    def test_painting_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.painting_slug: 'rye'}
            )
        )
        self.assertIn('painting', response.context)

    def test_painting_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.painting_slug: 'rye'}
            )
        )
        self.assertIsInstance(
            response.context['painting'], paintings.models.Painting
        )

    def test_painting_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'paintings:painting', kwargs={self.painting_slug: 'rye'}
            )
        )
        self.check_content_value(
            response.context['painting'],
            (
                paintings.models.Painting.painting_name.field.name,
                paintings.models.Painting.painting_creation_year.field.name,
                paintings.models.Painting.painting_materials.field.name,
                paintings.models.Painting.painting_size.field.name,
                paintings.models.Painting.painting_slug.field.name,
                paintings.models.Painting.painting_description.field.name,
                paintings.models.Painting.painting_photo.field.name,
                'painting_artist_id',
                'painting_gallery_id',
                'painting_likes',
            ),
        )
