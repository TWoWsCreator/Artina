# Generated by Django 4.1.5 on 2023-04-07 22:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите имя художника',
                        max_length=50,
                        verbose_name='имя художника',
                    ),
                ),
                (
                    'surname',
                    models.CharField(
                        help_text='Введите фамилию художника',
                        max_length=50,
                        verbose_name='фамиилия художника',
                    ),
                ),
                (
                    'patronymic',
                    models.CharField(
                        help_text='Введите отчество художника',
                        max_length=50,
                        verbose_name='отчество художника',
                    ),
                ),
                (
                    'birth_date',
                    models.IntegerField(
                        blank=True,
                        help_text='Введите дату рождения художника',
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(800),
                            django.core.validators.MaxValueValidator(2023),
                        ],
                        verbose_name='дата рождения художника',
                    ),
                ),
                (
                    'death_date',
                    models.IntegerField(
                        blank=True,
                        help_text='Введите дату сметри художника',
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(800),
                            django.core.validators.MaxValueValidator(2023),
                        ],
                        verbose_name='дата смерти художника',
                    ),
                ),
                (
                    'alived',
                    models.BooleanField(
                        default=False,
                        help_text='Поставьте галочку, если художник жив до сих пор',
                        verbose_name='жив ли сейчас',
                    ),
                ),
                (
                    'short_biography',
                    models.TextField(
                        help_text='Максимум 1000 символов',
                        max_length=1000,
                        verbose_name='краткая биография',
                    ),
                ),
                (
                    'artist_photo',
                    models.ImageField(
                        help_text='Выберите путь до фотографии художника',
                        upload_to='artists/',
                        verbose_name='путь до фотографии художника',
                    ),
                ),
                (
                    'artist_slug',
                    models.SlugField(
                        help_text='Введите url адрес для художника',
                        max_length=55,
                        verbose_name='слаг художника',
                    ),
                ),
            ],
            options={
                'verbose_name': 'художник',
                'verbose_name_plural': 'художники',
            },
        ),
    ]
