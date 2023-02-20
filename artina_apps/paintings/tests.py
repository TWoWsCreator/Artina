from django.test import Client, TestCase

# from django.urls import reverse

from parameterized import parameterized


class StaticURLTests(TestCase):
    # @parameterized.expand(
    #     [
    #         ('1', 200)
    #     ]
    # )
    def test_painting_endpoint(self):
        response = Client().get('/paintings/on_wild_north/')
        self.AssertEqual(response.status_code, 200)
