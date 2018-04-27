from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Photo
from sorl import thumbnail


def photo_view(request, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    username = request.user.get_username()
    context = {}
    if photo.user.username == username or photo.published == 'PUBLIC':
        context['photo'] = photo
        
    return render(request, 'imager_images/photo.html', context)


def photo_gallery_view():
    pass
    
    
def album_view(request, album_id):
    album = Album.objects.filter(id=album_id).first()
    username = request.user.get_username()
    context = {}
    if album.user.username == username or album.published == 'PUBLIC':
        context['album'] = album

    return render(request, 'imager_images/album.html', context)


def album_gallery_view(request):
    username = request.user.get_username()
    gallery = Album.objects.filter(user__username=username).filter(published='PUBLIC')
    context = {
        'gallery': gallery,
    }
    return render(request, 'imager_images/album_gallery.html', context)

def library_view(request, username=None):
    owner = False
    if not username:
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('auth_login')

    albums = Album.objects.all().filter(user__username=username)

    if not owner:
        albums = albums.all().filter(published='PUBLIC')

    context = {
        'albums': albums,
    }
    return render(request, 'imager_images/library.html', context)
