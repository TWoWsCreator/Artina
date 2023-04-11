import django.core.exceptions
import django.test
import django.urls
import parameterized.parameterized

import artists.models
import core.tests
import paintings.models


class StaticURLTests(django.test.TestCase):
    fixtures = ['fixtures/data.json']
    artists_slug = artists.models.Artists.slug.field.name

    def test_artists_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        self.assertEqual(
            response.status_code, 200, 'Страница художников не прогружается'
        )

    @parameterized.parameterized.expand(
        [
            ('serov',),
            ('perov',),
            ('shishkin',),
        ]
    )
    def test_positive_artist_page_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist', kwargs={self.artists_slug: slug}
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница биографии художников не загружается',
        )

    @parameterized.parameterized.expand(
        [
            ('vasnetsov',),
            ('pushkin',),
            ('mendeleev',),
        ]
    )
    def test_negative_artist_page_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist', kwargs={self.artists_slug: slug}
            )
        )
        self.assertEqual(
            response.status_code,
            404,
            'Загружается страница биографии художников, '
            'которых не в базе данных',
        )

    @parameterized.parameterized.expand(
        [
            ('ge',),
            ('repin',),
            ('savrasov',),
        ]
    )
    def test_positive_artist_paintings_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.artists_slug: slug},
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница картин художников не загружается',
        )

    @parameterized.parameterized.expand(
        [
            ('serov_1',),
            ('ladno',),
            ('nestor',),
        ]
    )
    def test_negative_artist_paintings_endpoint(self, slug):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.artists_slug: slug},
            )
        )
        self.assertEqual(
            response.status_code,
            404,
            'Загружается страница картин художников, '
            'которых не в базе данных',
        )


class ModelsTests(django.test.TestCase):
    @classmethod
    def create_artist(
        cls,
        birth_date,
        death_date,
    ):
        cls.test_artist = artists.models.Artists(
            name='Александр',
            surname='Пушкин',
            patronymic='Сергеевич',
            birth_date=birth_date,
            death_date=death_date,
            short_biography='что то интересное',
            artist_photo='.../...',
            slug='pushkin',
        )

    @parameterized.parameterized.expand(
        [
            (1800, 1880),
            (800, 882),
            (2000, 2022),
            (None, None),
            (None, 2022),
            (2000, None),
        ]
    )
    def test_positive_artist_years_of_life(self, birth_date, death_date):
        artists_amount = artists.models.Artists.objects.count()
        self.create_artist(birth_date=birth_date, death_date=death_date)
        self.test_artist.full_clean()
        self.test_artist.save()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount + 1,
            'Художник с валидными годами жизни не создается',
        )

    @parameterized.parameterized.expand(
        [
            (1967, 1929),
            (2000, 2024),
            (1899, 1899),
            (799, 842),
        ]
    )
    def test_negative_artist_years_of_life(self, birth_date, death_date):
        artists_amount = artists.models.Artists.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_artist(birth_date=birth_date, death_date=death_date)
            self.test_artist.full_clean()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount,
            'Художник с невалидными годами жизни создается',
        )

    def tearDown(self):
        artists.models.Artists.objects.all().delete()
        return super().tearDown()


class ContextTests(core.tests.CheckFieldsTestCase):
    fixtures = ['fixtures/data.json']
    slug = artists.models.Artists.slug.field.name

    def test_artists_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        self.assertIn(
            'artists',
            response.context,
            'Список художников не передается в context',
        )

    def test_amount_artists_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        self.assertEqual(
            len(response.context['artists']),
            14,
            'Кооличество художников не соответсвует заданному',
        )

    def test_artists_types(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        self.assertTrue(
            all(
                isinstance(
                    artist,
                    artists.models.Artists,
                )
                for artist in response.context['artists']
            ),
            '(Не все) художники являются сущностями модели Artists',
        )

    def test_artists_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        for artist in response.context['artists']:
            self.check_content_value(
                artist,
                (
                    artists.models.Artists.name.field.name,
                    artists.models.Artists.surname.field.name,
                    artists.models.Artists.patronymic.field.name,
                    artists.models.Artists.birth_date.field.name,
                    artists.models.Artists.death_date.field.name,
                    artists.models.Artists.alived.field.name,
                    artists.models.Artists.artist_photo.field.name,
                    artists.models.Artists.slug.field.name,
                ),
                not_loaded=(artists.models.Artists.short_biography.field.name),
            )

    def test_sorted_artists_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('artists:artists')
        )
        self.assertQuerysetEqual(
            artists.models.Artists.objects.order_by(
                artists.models.Artists.surname.field.name
            ),
            response.context['artists'],
            msg='Передаваемый в контекст список художников неосортирован',
        )

    def test_artist_page_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist', kwargs={self.slug: 'shishkin'}
            )
        )
        self.assertIn(
            'artist',
            response.context,
            'Информация о художнике не передается в context',
        )

    def test_artist_page_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist', kwargs={self.slug: 'shishkin'}
            )
        )
        self.assertIsInstance(
            response.context['artist'],
            artists.models.Artists,
            'Художник не является сущностью модели Artist',
        )

    def test_artist_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist', kwargs={self.slug: 'shishkin'}
            )
        )
        self.check_content_value(
            response.context['artist'],
            (
                artists.models.Artists.name.field.name,
                artists.models.Artists.surname.field.name,
                artists.models.Artists.patronymic.field.name,
                artists.models.Artists.birth_date.field.name,
                artists.models.Artists.death_date.field.name,
                artists.models.Artists.alived.field.name,
                artists.models.Artists.artist_photo.field.name,
                artists.models.Artists.slug.field.name,
                artists.models.Artists.short_biography.field.name,
            ),
        )

    def test_artists_paintings_context(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.slug: 'shishkin'},
            )
        )
        self.assertIn(
            'paintings',
            response.context,
            'Картины художника не передаются в context',
        )

    def test_artists_paintings_amount_items(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.slug: 'shishkin'},
            )
        )
        fail_text = 'Количество картин на страниц не соответсвует нужному'
        self.assertEqual(
            len(response.context['paintings']),
            5,
            fail_text,
        )

    def test_artists_paintings_sorted_items(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.slug: 'shishkin'},
            )
        )
        self.assertQuerysetEqual(
            paintings.models.Painting.objects.filter(
                painting_artist__slug='shishkin'
            ).order_by(paintings.models.Painting.painting_name.field.name),
            response.context['paintings'],
            msg='Передаваемый в контекст список картин неотсортирован',
        )

    def test_artists_paintings_types(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.slug: 'shishkin'},
            )
        )
        self.assertTrue(
            all(
                isinstance(painting, paintings.models.Painting)
                for painting in response.context['paintings']
            ),
            '(Не все) картины являюся сущностью модели Painting',
        )

    def test_artists_paintings_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse(
                'artists:artist_painting',
                kwargs={self.slug: 'shishkin'},
            )
        )
        painting_response_context = response.context['paintings']
        creation_year = paintings.models.Painting.painting_creation_year
        for painting in painting_response_context:
            self.check_content_value(
                painting,
                (
                    paintings.models.Painting.painting_name.field.name,
                    paintings.models.Painting.painting_height.field.name,
                    paintings.models.Painting.painting_width.field.name,
                    paintings.models.Painting.painting_photo.field.name,
                    creation_year.field.name,
                    paintings.models.Painting.slug.field.name,
                ),
                not_loaded=(
                    paintings.models.Painting.painting_artist.field.name,
                    paintings.models.Painting.painting_gallery.field.name,
                    paintings.models.Painting.painting_facts.field.name,
                    paintings.models.Painting.painting_materials.field.name,
                ),
            )
