from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from imager_images.models import Photo, Album
from .models import ImagerProfile


class ProfileView(LoginRequiredMixin, DetailView):
    """View User Profile."""
    template_name = 'imager_profile/profile.html'
    login_url = reverse_lazy('auth_login')
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs['username'] if 'username' in self.kwargs \
                   else self.request.user.username

        self.username = username
        return get_object_or_404(ImagerProfile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = Photo.objects.filter(user__username=self.username)
        albums = Album.objects.filter(user__username=self.username)
        context['username'] = self.request.user.username
        context['public_photos'] = photos.filter(published='PUBLIC')
        context['shared_photos'] = photos.filter(published='SHARED')
        context['private_photos'] = photos.filter(published='PRIVATE')
        context['public_albums'] = albums.filter(published='PUBLIC')
        context['shared_albums'] = albums.filter(published='SHARED')
        context['private_albums'] = albums.filter(published='PRIVATE')
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """View for updating user profile."""
    template_name = 'imager_profile/profile_edit.html'
    model = ImagerProfile
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'username'
    slug_field = 'user__username'
    fields = ['bio', 'phone', 'location', 'website', 'fee', 'camera',
              'services', 'photostyles']

    def get_object(self):
        return get_object_or_404(ImagerProfile, user=self.request.user)
