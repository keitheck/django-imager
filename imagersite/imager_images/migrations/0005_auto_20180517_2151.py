# Generated by Django 2.0.4 on 2018-05-17 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0004_auto_20180501_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='albums',
        ),
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='albums', to='imager_images.Photo'),
        ),
    ]
