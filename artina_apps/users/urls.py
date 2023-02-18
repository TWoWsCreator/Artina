from django.contrib.auth.views import (
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls import path, re_path, reverse_lazy

from .views import PasswordReset, ProfileView, SignUpView

app_name = 'users'
urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
        ),
        name='login',
    ),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done',
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url=reverse_lazy('users:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password_reset/',
        PasswordReset.as_view(
            # template_name='users/password_reset.html',
            # success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    re_path(
        r'password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'password_reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('profile/', ProfileView.as_view(), name='profile'),
]
