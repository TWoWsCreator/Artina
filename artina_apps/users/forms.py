from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


# class PasswordResetEmail(models.Model):
#     user_email = models.EmailField(
#         'Ваша почта',
#     )
#
#     def __str__(self):
#         return self.user_email
#


class PasswordResetEmailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    # class Meta:
    #     model = PasswordResetEmail
    #     fields = (
    #         PasswordResetEmail.user_email.field.name,
    #     )
