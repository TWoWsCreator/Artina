from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_feedback_endpoint(self):
        response = Client().get(reverse('feedback:feedback'))
        self.assertEqual(response.status_code, 200)
