import django.test
import django.urls
import parameterized.parameterized


class StaticURLTests(django.test.TestCase):
    def test_users_login_endpoint(self):
        response = django.test.Client().get(django.urls.reverse('users:login'))
        self.assertEqual(
            response.status_code,
            200,
            'Не открывается страринца входа в аккаунт',
        )

    def test_users_sign_up_endpoint(self):
        response = django.testClient().get(
            django.urls.reverse('users:sign_up')
        )
        self.assertEqual(
            response.status_code,
            200,
            'Не открывается страница регистрации на сайте',
        )

    def test_users_password_reset_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('users:password_reset')
        )
        self.assertEqual(
            response.status_code, 200, 'Не открывается страница сброса пароля'
        )

    def test_users_password_reset_done_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('users:password_reset_done')
        )
        self.assertEqual(
            response.status_code,
            200,
            'Не открывается страница подтверждения сброса пароля',
        )

    @parameterized.parameterized.expand(
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
        response = django.test.Client().get(
            f'/users/password_reset/confirm/{uuid}/{token}/'
        )
        self.assertEqual(
            response.status_code,
            status_code,
            'не открывается страница смены пароля ' 'после запроса на сброс',
        )
