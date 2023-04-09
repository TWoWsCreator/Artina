import datetime

import django.core.exceptions
import django.core.validators
import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail


class ArtistsManager(django.db.models.Manager):
    def get_all_artists(self):
        return (
            self.get_queryset()
            .all()
            .only(
                Artists.name.field.name,
                Artists.surname.field.name,
                Artists.patronymic.field.name,
                Artists.birth_date.field.name,
                Artists.death_date.field.name,
                Artists.alived.field.name,
                Artists.artist_photo.field.name,
                Artists.slug.field.name,
            )
            .order_by(Artists.surname.field.name)
        )


class Artists(django.db.models.Model):
    objects = ArtistsManager()

    name = django.db.models.CharField(
        'имя художника',
        max_length=50,
        help_text='Введите имя художника',
    )
    surname = django.db.models.CharField(
        'фамиилия художника',
        max_length=50,
        help_text='Введите фамилию художника',
    )
    patronymic = django.db.models.CharField(
        'отчество художника',
        max_length=50,
        help_text='Введите отчество художника',
    )
    birth_date = django.db.models.IntegerField(
        'дата рождения художника',
        help_text='Введите дату рождения художника',
        validators=[
            django.core.validators.MinValueValidator(800),
            django.core.validators.MaxValueValidator(
                datetime.date.today().year
            ),
        ],
        blank=True,
        null=True,
    )
    death_date = django.db.models.IntegerField(
        'дата смерти художника',
        help_text='Введите дату сметри художника',
        validators=[
            django.core.validators.MinValueValidator(800),
            django.core.validators.MaxValueValidator(
                datetime.date.today().year
            ),
        ],
        blank=True,
        null=True,
    )
    alived = django.db.models.BooleanField(
        'жив ли сейчас',
        default=False,
        help_text='Поставьте галочку, если художник жив до сих пор',
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
    slug = django.db.models.SlugField(
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
    def get_full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @property
    def years_of_life(self):
        if self.birth_date is None:
            self.birth_date = '???'
        if self.death_date is None:
            if self.alived:
                self.death_date = 'до н.в.'
            else:
                self.death_date = '???'
        return f'{self.birth_date}-{self.death_date}'

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

    def clean(self):
        if (self.birth_date is not None) and (self.death_date is not None):
            if self.birth_date >= int(self.death_date):
                raise django.core.exceptions.ValidationError(
                    'Год сметри должен идти позже года рождения'
                )

    class Meta:
        verbose_name = 'художник'
        verbose_name_plural = 'художники'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
