from django.test import Client, TestCase
from django.urls import reverse

from parameterized import parameterized


class StaticURLTests(TestCase):
    def test_users_login_endpoint(self):
        response = Client().get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_users_sign_up_endpoint(self):
        response = Client().get(reverse('users:sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_users_password_reset_endpoint(self):
        response = Client().get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_users_password_reset_done_endpoint(self):
        response = Client().get(reverse('users:password_reset_done'))
        self.assertEqual(response.status_code, 200)

    # def test_users_password_reset_confirm_endpoint(self):
    #     response = Client().get(reverse('users:password_reset_confirm'))
    #     self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ('MQ', 'bjy5fc-4f38e570b1612bd', 200),
            ('HH', 'uqwbucqbruvb137108ncuqn', 200),
            ('HH', 'uqwbuc//qbruvb13//710/8ncuqn', 404),
            ('2131232//', 'bjy5fc-4f38e570b1612bd', 404),
        ]
    )
    def test_users_password_reset_complete_endpoint(
        self, uuid, token, status_code
    ):
        # response = Client().get(
        #     reverse('users:password_reset_confirm',
        #             kwargs={
        #                 'uidb64': uuid,
        #                 'token': token
        #             })
        # )
        response = Client().get(
            f'/users/password_reset/confirm/{uuid}/{token}/'
        )
        self.assertEqual(response.status_code, status_code)

    # требуется вход в систему

    # def test_users_password_change_endpoint(self):
    #     response = Client().get(reverse('users:password_change'))
    #     self.assertEqual(response.status_code, 200)

    # def test_users_password_change_done_endpoint(self):
    #     response = Client().get(reverse('users:password_change_done'))
    #     self.assertEqual(response.status_code, 200)
