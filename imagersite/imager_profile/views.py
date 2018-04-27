from django.shortcuts import render, redirect, get_object_or_404
from .models import ImagerProfile
from imager_images.models import Photo, Album


def profile_view(request, username=None):
    if not username:
        username = request.user.get_username()
        if username == '':
            return redirect('auth_login')

    profile = get_object_or_404(ImagerProfile, user__username=username)
    photos = Photo.objects.filter(user__username=username)
    public_photos = photos.filter(published='PUBLIC')
    shared_photos = photos.filter(published='SHARED')
    private_photos = photos.filter(published='PRIVATE')

    albums = Album.objects.filter(user__username=username)
    public_albums = albums.filter(published='PUBLIC')
    shared_albums = albums.filter(published='SHARED')
    private_albums = albums.filter(published='PRIVATE')

    context = {
        'profile': profile,
        'public_photos': public_photos,
        'shared_photos': shared_photos,
        'private_photos': private_photos,
        'public_albums': public_albums,
        'shared_albums': shared_albums,
        'private_albums': private_albums,
    }

    return render(request, 'imager_profile/profile.html', context)
