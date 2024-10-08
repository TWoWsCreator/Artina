import datetime

import django.core.validators
import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail

import artists.models
import galleries.models
import users.models


class PaintingManager(django.db.models.Manager):
    def get_filter_paintings(self):
        return (
            self.get_queryset()
            .only(
                Painting.painting_name.field.name,
                Painting.painting_height.field.name,
                Painting.painting_width.field.name,
                Painting.painting_photo.field.name,
                Painting.painting_creation_year.field.name,
                Painting.slug.field.name,
            )
            .order_by(Painting.painting_name.field.name)
        )

    def get_painting(self):
        return (
            self.get_queryset()
            .select_related(
                Painting.painting_artist.field.name,
                Painting.painting_gallery.field.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Painting.likes.field.name,
                    queryset=users.models.CustomUser.objects.all(),
                    to_attr='painting_likes',
                ),
                django.db.models.Prefetch(
                    PaintingFacts.painting.field.related_query_name(),
                    queryset=PaintingFacts.objects.all(),
                ),
            )
            .only(
                Painting.painting_name.field.name,
                Painting.painting_creation_year.field.name,
                Painting.painting_materials.field.name,
                Painting.painting_width.field.name,
                Painting.painting_height.field.name,
                Painting.slug.field.name,
                # Painting.painting_description.field.name,
                Painting.painting_photo.field.name,
                f'{Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.name.field.name}',
                f'{Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.surname.field.name}',
                f'{Painting.painting_artist.field.name}__'
                f'{artists.models.Artists.patronymic.field.name}',
                f'{Painting.painting_gallery.field.name}__'
                f'{galleries.models.Galleries.gallery_name.field.name}',
            )
        )


class Painting(django.db.models.Model):
    objects = PaintingManager()

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
            django.core.validators.MaxValueValidator(
                datetime.date.today().year
            ),
        ],
    )
    painting_width = django.db.models.FloatField(
        'ширина картины',
        help_text='Введите ширину картины',
        validators=[
            django.core.validators.MinValueValidator(10),
            django.core.validators.MaxValueValidator(10000),
        ],
    )
    painting_height = django.db.models.FloatField(
        'высота картины',
        help_text='Введите высоту картины',
        validators=[
            django.core.validators.MinValueValidator(10),
            django.core.validators.MaxValueValidator(10000),
        ],
    )
    painting_materials = django.db.models.CharField(
        'материалы картины',
        max_length=25,
        help_text='Введите материала, которые использовались при создании '
        'картины',
    )
    # painting_description = django.db.models.TextField(
    #     'описание картины',
    #     max_length=1000,
    #     help_text='Напишите описание к картине',
    # )
    painting_photo = django.db.models.ImageField(
        'путь до изображения картины',
        help_text='Введите путь до изображения картины',
        upload_to='picture/',
    )
    slug = django.db.models.SlugField(
        'слаг картины',
        max_length=55,
        help_text='Введите url адрес для картины',
        unique=True,
    )
    likes = django.db.models.ManyToManyField(
        users.models.CustomUser, verbose_name='лайк', blank=True
    )

    @property
    def get_painting_size(self):
        if self.painting_height == int(self.painting_height):
            self.painting_height = int(self.painting_height)
        if self.painting_width == int(self.painting_width):
            self.painting_width = int(self.painting_width)
        return f'{self.painting_width}x{self.painting_height}'

    @property
    def get_image(self):
        return sorl.thumbnail.get_thumbnail(
            self.painting_photo, '250x150', quality=51
        )

    def image_tmb(self):
        if self.painting_photo:
            return django.utils.safestring.mark_safe(
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


class PaintingFacts(django.db.models.Model):
    title = django.db.models.CharField(
        'заголовок',
        max_length=100,
        help_text='Напишите заголовок карточки факта',
        null=True,
        blank=True,
    )
    painting = django.db.models.ForeignKey(
        Painting,
        verbose_name='факт',
        related_name='painting_facts',
        on_delete=django.db.models.CASCADE,
    )
    fact = django.db.models.TextField(
        'факт о картине',
        max_length=500,
        help_text='Максимум 500 символов',
    )

    class Meta:
        verbose_name = 'факт о картине'
        verbose_name_plural = 'факты о картине'

    def __str__(self):
        return self.fact[:20]
