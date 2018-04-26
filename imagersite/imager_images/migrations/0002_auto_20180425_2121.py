# Generated by Django 2.0.4 on 2018-04-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(blank=True, to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='albums',
            field=models.ManyToManyField(blank=True, to='imager_images.Album'),
        ),
    ]
