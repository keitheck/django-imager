from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Album(models.Model):
    """Photo album model."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums')
    cover = models.ForeignKey(
        'Photo',
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True)
    # photos = models.ManyToManyField('Photo', related_name='+', blank=True)
    photos = models.ManyToManyField('Photo', related_name='albums', blank=True)
    title = models.CharField(max_length=1024, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
            max_length=7,
            choices=(
                ('PRIVATE', 'Private'),
                ('SHARED', 'Shared'),
                ('PUBLIC', 'Public'),))

    def __str__(self):
        return self.title


class Photo(models.Model):
    """Photo model."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='photos')
    image = ImageField(upload_to='images')
    # albums = models.ManyToManyField('Album', related_name='+', blank=True)
    title = models.CharField(max_length=1024, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
            max_length=7,
            choices=(
                ('PRIVATE', 'Private'),
                ('SHARED', 'Shared'),
                ('PUBLIC', 'Public'),))

    def __str__(self):
        return self.title
