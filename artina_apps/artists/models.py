import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail

import artists.validators


class Artists(django.db.models.Model):
    artist = django.db.models.CharField(
        'ФИО художника',
        max_length=50,
        help_text='Введите фамилию, имя и отчество художника через пробел',
        validators=[artists.validators.ArtistNameValidator()],
    )
    years_of_life = django.db.models.CharField(
        'годы жизни',
        max_length=10,
        help_text='Введите год рождения и смерти художника через тире. '
        'Пример: 1899-1977',
        validators=[artists.validators.ArtistYearsValidator()],
    )
    short_biography = django.db.models.TextField(
        'краткая биография',
        max_length=1000,
        help_text='Максимум 1000 символов',
    )
    artist_photo = django.db.models.ImageField(
        'путь до фотографии художника',
        help_text='Выберите путь до фотографии художника',
        upload_to='artists/',
    )
    artist_slug = django.db.models.SlugField(
        'слаг художника',
        max_length=55,
        help_text='Введите url адрес для художника',
    )

    def get_short_biography(self):
        return django.template.defaultfilters.truncatechars(
            self.short_biography, 200
        )

    get_short_biography.short_description = 'краткая биография'

    @property
    def get_image(self):
        return sorl.thumbnail.get_thumbnail(
            self.artist_photo, '200x200', crop='center', quality=51
        )

    def image_tmb(self):
        if self.artist_photo:
            return django.utils.safestring.mark_safe(
                f'<img src={self.get_image.url} />'
            )
        return 'нет изображения'

    image_tmb.short_description = 'фото художника'
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = 'художник'
        verbose_name_plural = 'художники'

    def __str__(self):
        return self.artist
