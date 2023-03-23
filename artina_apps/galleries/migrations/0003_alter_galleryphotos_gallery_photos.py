# Generated by Django 4.1.5 on 2023-03-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('galleries', '0002_alter_galleryphotos_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryphotos',
            name='gallery_photos',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='images',
                to='galleries.galleries',
                verbose_name='фотографии галереи',
            ),
        ),
    ]
