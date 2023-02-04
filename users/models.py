from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=30,
        unique=True,
        help_text='максимальная длина 30 символов'
    )
    email = models.EmailField(
        'Ваша почта',
    )
    image = models.ImageField(
        'добавьте картинку профиля',
        upload_to='avatar/%Y/%m/%d',
        blank=True
    )

    def __str__(self):
        return self.username

