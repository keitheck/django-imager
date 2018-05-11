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


class AlbumEditForm(AlbumForm):
    """
    Form class for editing existing album.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        album = kwargs['instance']
        self.fields['title'].initial = album.title
        self.fields['description'].initial = album.description
        self.fields['date_published'].initial = album.date_published
        self.fields['published'].initial = album.published


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


class PhotoEditForm(ModelForm):
    """
    Form class for editing existing photo.
    """
    class Meta:
        model = Photo
        fields = ['title', 'description', 'date_published', 'published']

    def __init__(self, *args, **kwargs):
        kwargs.pop('username')
        super().__init__(*args, **kwargs)
        photo = kwargs['instance']
        self.fields['title'].initial = photo.title
        self.fields['description'].initial = photo.description
        self.fields['date_published'].initial = photo.date_published
        self.fields['published'].initial = photo.published
