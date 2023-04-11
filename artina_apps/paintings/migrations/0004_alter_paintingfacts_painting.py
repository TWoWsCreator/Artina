# Generated by Django 4.2 on 2023-04-10 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('paintings', '0003_paintingfacts_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paintingfacts',
            name='painting',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='painting_facts',
                to='paintings.painting',
                verbose_name='факт',
            ),
        ),
    ]
