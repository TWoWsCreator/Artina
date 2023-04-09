import django.db.models
import django.template.defaultfilters
import django.utils.safestring
import sorl.thumbnail


class GalleriesManager(django.db.models.Manager):
    def get_gallery_with_photos(self):
        gallery_photos = GalleryPhotos.objects.only(
            GalleryPhotos.photo.field.name,
            GalleryPhotos.gallery_photos_id.field.name,
        )
        gallery_photos_field = GalleryPhotos.gallery_photos
        return self.get_queryset().prefetch_related(
            django.db.models.Prefetch(
                gallery_photos_field.field.related_query_name(),
                queryset=gallery_photos,
            ),
        )

    def get_all_galleries(self):
        return (
            self.get_queryset()
            .all()
            .only(
                Galleries.gallery_name.field.name,
                Galleries.gallery_location.field.name,
                Galleries.gallery_image.field.name,
                Galleries.slug.field.name,
            )
            .order_by(Galleries.gallery_name.field.name)
        )


class Galleries(django.db.models.Model):
    objects = GalleriesManager()

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
    slug = django.db.models.SlugField(
        'слаг галереи',
        max_length=55,
        help_text='Введите url адрес для галереи',
    )
    gallery_description = django.db.models.TextField(
        'описание галереи',
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

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'

    def __str__(self):
        return self.gallery_name


class GalleryPhotos(django.db.models.Model):
    gallery_photos = django.db.models.ForeignKey(
        Galleries,
        related_name='images',
        on_delete=django.db.models.CASCADE,
        verbose_name='фотографии галереи',
    )
    photo = django.db.models.ImageField(
        'путь до фотографии галереи',
        upload_to='galleries/',
        help_text='Выберите путь до фотографии галереи',
    )

    @property
    def get_image(self):
        return sorl.thumbnail.get_thumbnail(
            self.photo, '600x300', crop='center', quality=51
        )

    def image_tmb(self):
        if self.gallery_image:
            return django.utils.safestring.mark_safe(
                f'<img src={self.get_image.url} /'
            )
        return 'нет изображения'

    def __str__(self):
        return self.photo.url
