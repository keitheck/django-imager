from django.shortcuts import redirect, get_object_or_404
from .models import ImagerProfile
from django.views.generic import TemplateView
from imager_images.models import Photo, Album


class ProfileView(TemplateView):
    """
    Profile view.
    """
    template_name = 'imager_profile/profile.html'
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('auth_login')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        username = self.request.user.get_username()
        photos = Photo.objects.filter(user__username=username)
        albums = Album.objects.filter(user__username=username)
        context['profile'] = get_object_or_404(ImagerProfile, user__username=username)
        context['public_photos'] = photos.filter(published='PUBLIC')
        context['shared_photos'] = photos.filter(published='SHARED')
        context['private_photos'] = photos.filter(published='PRIVATE')
        context['public_albums'] = albums.filter(published='PUBLIC')
        context['shared_albums'] = albums.filter(published='SHARED')
        context['private_albums'] = albums.filter(published='PRIVATE')

        return context


# def profile_view(request, username=None):
#     if not username:
#         username = request.user.get_username()
#         if username == '':
#             return redirect('auth_login')

#     profile = get_object_or_404(ImagerProfile, user__username=username)
#     photos = Photo.objects.filter(user__username=username)
#     public_photos = photos.filter(published='PUBLIC')
#     shared_photos = photos.filter(published='SHARED')
#     private_photos = photos.filter(published='PRIVATE')

#     albums = Album.objects.filter(user__username=username)
#     public_albums = albums.filter(published='PUBLIC')
#     shared_albums = albums.filter(published='SHARED')
#     private_albums = albums.filter(published='PRIVATE')

#     context = {
#         'profile': profile,
#         'public_photos': public_photos,
#         'shared_photos': shared_photos,
#         'private_photos': private_photos,
#         'public_albums': public_albums,
#         'shared_albums': shared_albums,
#         'private_albums': private_albums,
#     }

#     return render(request, 'imager_profile/profile.html', context)
