import django.apps


class PaintingsConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paintings'
    verbose_name = 'картины'
