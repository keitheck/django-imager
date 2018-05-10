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
        album_id = kwargs['album_id']
        self.fields['title'].initial = Album.objects.get(id=album_id).title
        self.fields['description'].initial = Album.objects.get(id=album_id).description
        self.fields['date_published'].initial = Album.objects.get(id=album_id).date_published
        self.fields['published'].initial = Album.objects.get(id=album_id).published
    

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


