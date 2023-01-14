from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=30,
        unique=True,
        help_text='максимальная длина 30 символов'
    )
    image = models.ImageField(
        'добавьте картинку профиля',
        upload_to='avatar/%Y/%m/%d',
        blank=True
    )

    def __str__(self):
        return self.username
