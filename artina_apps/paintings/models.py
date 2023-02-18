from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail

from artists.models import Artists

from galleries.models import Galleries

from users.models import CustomUser

from .validators import SizeValidation


class Painting(models.Model):
    painting_name = models.CharField(
        'название картины', max_length=50, help_text='Максимум 50 символов'
    )
    painting_artist = models.ForeignKey(
        Artists,
        on_delete=models.CASCADE,
        related_name='artists',
        verbose_name='художник',
    )
    painting_gallery = models.ForeignKey(
        Galleries,
        on_delete=models.CASCADE,
        related_name='galleries',
        verbose_name='галерея',
    )
    painting_creation_year = models.IntegerField(
        'год создания картины',
        help_text='Введите реальный год создания картины',
        validators=[MinValueValidator(800), MaxValueValidator(2022)],
    )
    painting_size = models.CharField(
        'введите размер картины',
        max_length=11,
        help_text='Введите размер картины через x',
        validators=[SizeValidation()],
    )
    painting_materials = models.CharField(
        'материалы картины',
        max_length=25,
        help_text='введите материала, которые использовались при создании '
        'картины',
    )
    painting_description = models.TextField(
        'описание картины',
        max_length=1000,
        help_text='Напишите описание к картине',
    )
    painting_photo = models.ImageField(
        'путь до изображения картины',
        help_text='введите путь до изображения картины',
        upload_to='picture/',
    )
    painting_slug = models.SlugField(
        'url картины',
        max_length=55,
        help_text='Введите url адрес для картины',
    )
    likes = models.ManyToManyField(CustomUser, verbose_name='лайк', blank=True)

    def get_painting_description(self):
        return truncatechars(self.painting_description, 100)

    get_painting_description.short_description = 'описание картины'

    @property
    def get_image(self):
        return get_thumbnail(self.painting_photo, '250x150', quality=51)

    def image_tmb(self):
        if self.painting_photo:
            return mark_safe(f'<img src={self.get_image.url} />')
        return 'нет изображения'

    image_tmb.short_description = 'изображение картины'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.painting_name

    class Meta:
        verbose_name = 'картина'
        verbose_name_plural = 'картины'
