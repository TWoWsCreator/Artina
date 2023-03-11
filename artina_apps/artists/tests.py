import django.core.exceptions
from django.test import Client, TestCase
from django.urls import reverse

from parameterized import parameterized

import artists.models


class StaticURLTests(TestCase):
    fixtures = ['fixtures/data.json']

    def test_artists_endpoint(self):
        response = Client().get(reverse('artists:artists'))
        self.assertEqual(
            response.status_code, 200, 'Страница художников не прогружается'
        )

    @parameterized.expand(
        [
            ('serov',),
            ('perov',),
            ('shishkin',),
        ]
    )
    def test_positive_artist_page_endpoint(self, artist_slug):
        response = Client().get(
            reverse('artists:artist', kwargs={'artist_slug': artist_slug})
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница биографии художников не загружается',
        )

    @parameterized.expand(
        [
            ('vasnetsov',),
            ('pushkin',),
            ('mendeleev',),
        ]
    )
    def test_negative_artist_page_endpoint(self, artist_slug):
        response = Client().get(
            reverse('artists:artist', kwargs={'artist_slug': artist_slug})
        )
        self.assertEqual(
            response.status_code,
            404,
            'Загружается страница биографии художников, '
            'которых не в базе данных',
        )

    @parameterized.expand(
        [
            ('ge',),
            ('repin',),
            ('savrasov',),
        ]
    )
    def test_positive_artist_paintings_endpoint(self, artist_slug):
        response = Client().get(
            reverse(
                'artists:artist_painting', kwargs={'artist_slug': artist_slug}
            )
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница картин художников не загружается',
        )

    @parameterized.expand(
        [
            ('serov_1',),
            ('ladno',),
            ('nestor',),
        ]
    )
    def test_negative_artist_paintings_endpoint(self, artist_slug):
        response = Client().get(
            reverse(
                'artists:artist_painting', kwargs={'artist_slug': artist_slug}
            )
        )
        self.assertEqual(
            response.status_code,
            404,
            'Загружается страница картин художников, '
            'которых не в базе данных',
        )


class ModelsTests(StaticURLTests):
    @classmethod
    def create_artist(cls, name='А. С. Пушкин', years_of_life='1777-1800'):
        print(name, years_of_life)
        cls.test_artist = artists.models.Artists(
            artist=name,
            years_of_life=years_of_life,
            short_biography='что то интересное',
            artist_photo='.../...',
            artist_slug='pushkin',
        )

    @parameterized.expand(
        [
            ('А. С. Пушкин',),
            ('Алесандр Сергеевич Пушкин'),
            ('Ладно Ладно Ладно',),
            ('Вова Карамзин Никитич',),
        ]
    )
    def test_positive_artist_name(self, artist_name):
        artists_amount = artists.models.Artists.objects.count()
        self.create_artist(name=artist_name)
        self.test_artist.full_clean()
        self.test_artist.save()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount + 1,
            'Художник с валидным именем не создается',
        )

    @parameterized.expand(
        [
            ('А Пушкин',),
            ('Алесандр Сергеевич Пушкин Карам'),
            ('А.С.Пушкин',),
            ('Хорошо Ладно',),
        ]
    )
    def test_negative_artist_name(self, artist_name):
        artists_amount = artists.models.Artists.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_artist(name=artist_name)
            self.test_artist.full_clean()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount,
            'Художник с невалидным именем создается',
        )

    @parameterized.expand(
        [
            ('1800-1900',),
            ('1777-1892'),
            ('1600-1655',),
        ]
    )
    def test_positive_artist_years_of_life(self, artist_years_of_life):
        artists_amount = artists.models.Artists.objects.count()
        self.create_artist(years_of_life=artist_years_of_life)
        self.test_artist.full_clean()
        self.test_artist.save()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount + 1,
            'Художник с валидными годами жизни не создается',
        )

    @parameterized.expand(
        [
            ('180O-1877',),
            ('-1223-1233'),
            ('1899=1977',),
            ('1977-',),
            ('-1999',),
            ('121233-1222',),
            ('1900-12334',),
        ]
    )
    def test_negative_artist_years_of_life(self, artist_years_of_life):
        artists_amount = artists.models.Artists.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.create_artist(years_of_life=artist_years_of_life)
            self.test_artist.full_clean()
        self.assertEqual(
            artists.models.Artists.objects.count(),
            artists_amount,
            'Художник с невалидными годами жизни создается',
        )

    def tearDown(self):
        artists.models.Artists.objects.all().delete()
        return super().tearDown()
