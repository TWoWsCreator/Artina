from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from .validators import ArtistNameValidator, ArtistYearsValidator


class Artists(models.Model):
    artist = models.CharField(
        'ФИО художника',
        max_length=50,
        help_text='Введите фамилию, имя и отчество художника через пробел',
        validators=[ArtistNameValidator()]
    )
    years_of_life = models.CharField(
        'годы жизни',
        max_length=10,
        help_text='Введите год рождения и смерти художника через тире. Пример: 1899-1977',
        validators=[ArtistYearsValidator()]
    )
    short_biography = models.TextField(
        'краткая биография',
        max_length=1000,
        help_text='Максимум 1000 символов'
    )
    artist_photo = models.ImageField('путь до фотографии художника',
                                     help_text='выберите путь до фотографии художника',
                                     upload_to='artists/'
                                     )
    artist_slug = models.SlugField(
        'url художника',
        max_length=55,
        help_text='Введите url адрес для художника',
    )

    def get_short_biography(self):
        return truncatechars(self.short_biography, 200)

    get_short_biography.short_description = 'краткая биография'

    @property
    def get_image(self):
        return get_thumbnail(self.artist_photo, '200x200', crop='center', quality=51)

    def image_tmb(self):
        if self.artist_photo:
            return mark_safe(f'<img src={self.get_image.url} />')
        return 'нет изображения'

    image_tmb.short_description = 'фото художника'
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = 'художник'
        verbose_name_plural = 'художники'

    def __str__(self):
        return self.artist


# class ArtistsGallery(models.Model):
#     artist_gallery = models.ForeignKey(Artists,
#                                        # related_name='artists',
#                                        on_delete=models.CASCADE,
#                                        verbose_name='фотографии художника')
#     gallery_image = models.ImageField('путь до фотографии художника',
#                                       help_text='Выберите путь до фотографии художника')
#
#     def __str__(self):
#         return self.gallery_image.url
