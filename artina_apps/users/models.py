import django.contrib.auth.models
import django.db.models


class CustomUser(django.contrib.auth.models.AbstractUser):
    username = django.db.models.CharField(
        'имя пользователя',
        max_length=30,
        unique=True,
        help_text='Максимальная длина 30 символов',
    )
    email = django.db.models.EmailField(
        'ваша почта',
    )
    image = django.db.models.ImageField(
        'добавьте картинку профиля', upload_to='avatar/%Y/%m/%d', blank=True
    )

    def __str__(self):
        return self.username


class PasswordResetEmail(django.db.models.Model):
    user_email = django.db.models.EmailField(
        'ваша почта',
    )

    def __str__(self):
        return self.user_email
