from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail


class Galleries(models.Model):
    gallery_name = models.CharField(
        'название галереи',
        max_length=50,
        help_text='Введите название галереи картин',
    )
    gallery_location = models.CharField(
        'расположение галереи',
        max_length=75,
        help_text='Введите локацию галереи',
    )
    gallery_slug = models.SlugField(
        'url галереи', max_length=55, help_text='Введите url адрес для галереи'
    )
    gallery_description = models.TextField(
        'интересные факты о галереи',
        max_length=1000,
        help_text='Максимум 1000 символов',
    )
    gallery_image = models.ImageField(
        'путь до изображения галереи',
        upload_to='galleries/',
        help_text='Введите путь до изображения галереи',
    )

    def get_short_description(self):
        return truncatechars(self.gallery_description, 100)

    @property
    def get_image(self):
        return get_thumbnail(
            self.gallery_image, '200x200', crop='center', quality=51
        )

    def image_tmb(self):
        if self.gallery_image:
            return mark_safe(f'<img src={self.get_image.url} /')
        return 'нет изображения'

    image_tmb.short_description = 'фото галереи'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.gallery_name

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'


class GalleryPhotos(models.Model):
    gallery_photos = models.ForeignKey(
        Galleries, on_delete=models.CASCADE, verbose_name='фотографии галереи'
    )
    photo = models.ImageField(
        'путь до фотографии галереи',
        upload_to='galleries/',
        help_text='Выберите путь до фотографии галереи',
    )

    def __str__(self):
        return self.photo.url
