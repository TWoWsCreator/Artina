import django.core.validators
import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail

import artists.models
import galleries.models
import paintings.validators
import users.models


class Painting(django.db.models.Model):
    painting_name = django.db.models.CharField(
        'название картины', max_length=50, help_text='Максимум 50 символов'
    )
    painting_artist = django.db.models.ForeignKey(
        artists.models.Artists,
        on_delete=django.db.models.CASCADE,
        related_name='artists',
        verbose_name='художник',
    )
    painting_gallery = django.db.models.ForeignKey(
        galleries.models.Galleries,
        on_delete=django.db.models.CASCADE,
        related_name='galleries',
        verbose_name='галерея',
    )
    painting_creation_year = django.db.models.IntegerField(
        'год создания картины',
        help_text='Введите реальный год создания картины',
        validators=[
            django.core.validators.MinValueValidator(800),
            django.core.validators.MaxValueValidator(2022),
        ],
    )
    painting_size = django.db.models.CharField(
        'введите размер картины',
        max_length=11,
        help_text='Введите размер картины через x',
        validators=[paintings.validators.SizeValidation()],
    )
    painting_materials = django.db.models.CharField(
        'материалы картины',
        max_length=25,
        help_text='введите материала, которые использовались при создании '
        'картины',
    )
    painting_description = django.db.models.TextField(
        'описание картины',
        max_length=1000,
        help_text='Напишите описание к картине',
    )
    painting_photo = django.db.models.ImageField(
        'путь до изображения картины',
        help_text='введите путь до изображения картины',
        upload_to='picture/',
    )
    painting_slug = django.db.models.SlugField(
        'url картины',
        max_length=55,
        help_text='Введите url адрес для картины',
    )
    likes = django.db.models.ManyToManyField(
        users.models.CustomUser, verbose_name='лайк', blank=True
    )

    def get_painting_description(self):
        return django.template.defaultfilters.truncatechars(
            self.painting_description, 100
        )

    get_painting_description.short_description = 'описание картины'

    @property
    def get_image(self):
        return django.utils.safestring.get_thumbnail(
            self.painting_photo, '250x150', quality=51
        )

    def image_tmb(self):
        if self.painting_photo:
            return sorl.thumbnail.mark_safe(
                f'<img src={self.get_image.url} />'
            )
        return 'нет изображения'

    image_tmb.short_description = 'изображение картины'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.painting_name

    class Meta:
        verbose_name = 'картина'
        verbose_name_plural = 'картины'
