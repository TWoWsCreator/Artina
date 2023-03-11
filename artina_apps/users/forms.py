import django.contrib.auth.forms
import django.forms

from .models import CustomUser, PasswordResetEmail


class CustomUserCreationForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(django.contrib.auth.formsUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class PasswordResetEmailForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PasswordResetEmail
        fields = (PasswordResetEmail.user_email.field.name,)
