from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Photo
from django.http import Http404
from django.contrib.auth.models import User


def photo_view(request, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    # import pdb ; pdb.set_trace()
    # username = get_object_or_404(User, username=request.user.username).username
    username = request.user.get_username()
    
    context = {}
    if photo.user.username != username and photo.published != 'PUBLIC':
        raise Http404('Photo not found.')
    
    if photo.user.username == username or photo.published == 'PUBLIC':
        context['photo'] = photo

    return render(request, 'imager_images/photo.html', context)


def photo_gallery_view(request):
    
    gallery = Photo.objects.filter(published='PUBLIC')
    context = {
        'gallery': gallery,
    }
    return render(request, 'imager_images/photo_gallery.html', context)


def album_view(request, album_id):
    album = Album.objects.filter(id=album_id).first()
    username = request.user.get_username()
    context = {}
    if album.user.username == username or album.published == 'PUBLIC':
        context['album'] = album

    return render(request, 'imager_images/album.html', context)


def album_gallery_view(request):
    
    gallery = Album.objects.filter(published='PUBLIC')
    context = {
        'gallery': gallery,
    }
    return render(request, 'imager_images/album_gallery.html', context)


def library_view(request):
    username = request.user.get_username()
    
    if username == '':
        return redirect('auth_login')

    albums = Album.objects.all().filter(user__username=username)
    photos = Photo.objects.filter(user__username=username)

    # if not owner:
    #     albums = albums.all().filter(published='PUBLIC')
    #     photos = photos.filter(published='PUBLIC')

    context = {
        'albums': albums,
        'photos': photos,
    }
    return render(request, 'imager_images/library.html', context)
