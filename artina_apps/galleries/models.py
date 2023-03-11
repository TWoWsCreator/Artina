import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail


class Galleries(django.db.models.Model):
    gallery_name = django.db.models.CharField(
        'название галереи',
        max_length=50,
        help_text='Введите название галереи картин',
    )
    gallery_location = django.db.models.CharField(
        'расположение галереи',
        max_length=75,
        help_text='Введите локацию галереи',
    )
    gallery_slug = django.db.models.SlugField(
        'url галереи', max_length=55, help_text='Введите url адрес для галереи'
    )
    gallery_description = django.db.models.TextField(
        'интересные факты о галереи',
        max_length=1000,
        help_text='Максимум 1000 символов',
    )
    gallery_image = django.db.models.ImageField(
        'путь до изображения галереи',
        upload_to='galleries/',
        help_text='Введите путь до изображения галереи',
    )

    def get_short_description(self):
        return django.template.defaultfilters.truncatechars(
            self.gallery_description, 100
        )

    @property
    def get_image(self):
        return sorl.thumbnail.get_thumbnail(
            self.gallery_image, '200x200', crop='center', quality=51
        )

    def image_tmb(self):
        if self.gallery_image:
            return django.utils.safestring.mark_safe(
                f'<img src={self.get_image.url} /'
            )
        return 'нет изображения'

    image_tmb.short_description = 'фото галереи'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.gallery_name

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'


class GalleryPhotos(django.db.models.Model):
    gallery_photos = django.db.models.ForeignKey(
        Galleries,
        on_delete=django.db.models.CASCADE,
        verbose_name='фотографии галереи',
    )
    photo = django.db.models.ImageField(
        'путь до фотографии галереи',
        upload_to='galleries/',
        help_text='Выберите путь до фотографии галереи',
    )

    def __str__(self):
        return self.photo.url
