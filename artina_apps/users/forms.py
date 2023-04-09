import django.contrib.auth.forms

import core.forms
import users.models


class CustomUserCreationForm(
    django.contrib.auth.forms.UserCreationForm, core.forms.BootstrapControlForm
):
    class Meta:
        model = users.models.CustomUser
        fields = (
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
        )


class CustomUserChangeForm(
    django.contrib.auth.forms.UserChangeForm, core.forms.BootstrapControlForm
):
    class Meta:
        model = users.models.CustomUser
        fields = (
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_login.field.name,
            users.models.CustomUser.image.field.name,
        )


class PasswordResetEmailForm(core.forms.BootstrapControlForm):
    class Meta:
        model = users.models.PasswordResetEmail
        fields = (users.models.PasswordResetEmail.user_email.field.name,)
