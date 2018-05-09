from django.forms import ModelForm, ImageField
from .models import Photo, Album


class AlbumForm(ModelForm):
    """
    Form class for user creating an album.
    """
    class Meta:
        model = Album
        fields = [
            'title', 'photos', 'description', 'date_published', 'published'
            ]

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['photos'].queryset = \
            Photo.objects.filter(user__username=username)


class PhotoForm(ModelForm):
    """
    Form class for user creating an photo.
    """  
    class Meta:
        model = Photo
        fields = [
            'title', 'image', 'description', 'date_published', 'published'
            ]

    def __init__(self, *args, **kwargs):
        kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['image'] = ImageField()


