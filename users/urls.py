from django.urls import path, reverse_lazy
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView)
from .views import SignUpView, ProfileView

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
        ),
        name='login',
    ),
    path('sign_up/',
         SignUpView.as_view(),
         name='sign_up'),
    path(
        'password_change_done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
        ),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change.html',
             success_url=reverse_lazy('users:password_change_done')
         ),
         name='password_change'),
    path('profile/',
         ProfileView.as_view(),
         name='profile')
]
