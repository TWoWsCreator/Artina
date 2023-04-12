import datetime

import django.contrib.auth.forms
import django.core.exceptions
import django.forms

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
            users.models.CustomUser.last_name.field.name,
            users.models.CustomUser.birthday.field.name,
            users.models.CustomUser.image.field.name,
        )
        readonly_fields = ['username']

    def clean(self):
        birthday_field = super().clean().get('birthday', None)
        if birthday_field:
            date = datetime.datetime.today().date()
            if birthday_field >= date:
                self.add_error(
                    users.models.CustomUser.birthday.field.name,
                    'Введите реальную дату рождения',
                )
        return super().clean()


class PasswordResetEmailForm(core.forms.BootstrapControlForm):
    class Meta:
        model = users.models.PasswordResetEmail
        fields = (users.models.PasswordResetEmail.user_email.field.name,)
