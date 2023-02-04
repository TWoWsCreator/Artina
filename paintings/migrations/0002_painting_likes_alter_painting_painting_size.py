# Generated by Django 4.1.5 on 2023-01-21 18:26

from django.conf import settings
from django.db import migrations, models
import paintings.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paintings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='painting',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='лайк'),
        ),
        migrations.AlterField(
            model_name='painting',
            name='painting_size',
            field=models.CharField(help_text='Введите размер картины через x', max_length=11, validators=[paintings.validators.SizeValidation()], verbose_name='введите размер картины'),
        ),
    ]
