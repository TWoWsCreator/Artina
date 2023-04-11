import django.contrib.auth.models
import django.db.models

import feedback.models


class CustomUser(django.contrib.auth.models.AbstractUser):
    username = django.db.models.CharField(
        'имя пользователя',
        max_length=30,
        unique=True,
        help_text='Максимальная длина 30 символов',
    )
    email = django.db.models.EmailField(
        'ваша почта',
        unique=True,
    )
    image = django.db.models.ImageField(
        'добавьте картинку профиля', upload_to='avatar/%Y/%m/%d', blank=True
    )
    feedback_mails = django.db.models.ForeignKey(
        feedback.models.Feedback,
        on_delete=django.db.models.CASCADE,
        related_name='feedback',
        verbose_name='письма от пользователя',
        null=True,
    )

    def __str__(self):
        return self.username


class PasswordResetEmail(django.db.models.Model):
    user_email = django.db.models.EmailField(
        'ваша почта',
    )

    def __str__(self):
        return self.user_email
