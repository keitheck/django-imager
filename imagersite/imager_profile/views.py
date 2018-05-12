from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from imager_images.models import Photo, Album
from .models import ImagerProfile
from .forms import ProfileEditForm


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
    template_name = 'imager_profile/profile_edit.html'
    model = ImagerProfile
    form_class = ProfileEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.get_username()})
        return kwargs
