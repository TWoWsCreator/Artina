import django.contrib.auth.forms

import core.forms
import users.models


class CustomUserCreationForm(
    django.contrib.auth.forms.UserCreationForm, core.forms.BootstrapControlForm
):
    class Meta:
        model = users.models.CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(
    django.contrib.auth.forms.UserChangeForm, core.forms.BootstrapControlForm
):
    class Meta:
        model = users.models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class PasswordResetEmailForm(core.forms.BootstrapControlForm):
    class Meta:
        model = users.models.PasswordResetEmail
        fields = (users.models.PasswordResetEmail.user_email.field.name,)
