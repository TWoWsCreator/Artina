from django.test import Client, TestCase

from django.urls import reverse

from parameterized import parameterized


class StaticURLTests(TestCase):
    fixtures = [
        'fixtures/data.json',
    ]

    @parameterized.expand(
        [
            ('on_wild_north', 200),
        ]
    )
    def test_painting_endpoint(self, name, expected_status):
        response = Client().get(f'/paintings/{name}/')
        self.assertEqual(response.status_code, expected_status)
