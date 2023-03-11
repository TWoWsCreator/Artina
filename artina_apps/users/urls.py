import django.contrib.auth.views
import django.urls

import users.views

app_name = 'users'
urlpatterns = [
    django.urls.path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='users/login.html',
        ),
        name='login',
    ),
    django.urls.path(
        'sign_up/', users.views.SignUpView.as_view(), name='sign_up'
    ),
    django.urls.path(
        'password_change/done/',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url=django.urls.reverse_lazy('users:password_change_done'),
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_reset/',
        users.views.PasswordReset.as_view(),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    django.urls.re_path(
        r'password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=django.urls.reverse_lazy(
                'users:password_reset_complete'
            ),
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'password_reset/complete/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    django.urls.path(
        'profile/', users.views.ProfileView.as_view(), name='profile'
    ),
]
