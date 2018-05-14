from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Album, Photo


class PhotoView(DetailView):
    template_name = 'imager_images/photo.html'
    context_object_name = 'photo'
    pk_url_kwarg = 'photo_id'

    def get_queryset(self):
        return Photo.objects.filter(
               user__username=self.request.user.username) | \
               Photo.objects.filter(published='PUBLIC')


class AlbumView(DetailView):
    template_name = 'imager_images/album.html'
    context_object_name = 'album'
    pk_url_kwarg = 'album_id'

    def get_queryset(self):
        return Album.objects.filter(
               user__username=self.request.user.username) | \
               Album.objects.filter(published='PUBLIC')


class PhotoGalleryView(ListView):
    template_name = 'imager_images/photo_gallery.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Photo.objects.filter(published='PUBLIC')


class AlbumGalleryView(ListView):
    template_name = 'imager_images/album_gallery.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Album.objects.filter(published='PUBLIC')


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'imager_images/library.html'
    context_object_name = 'albums'
    login_url = reverse_lazy('auth_login')

    def get_queryset(self):
        return Album.objects.filter(user__username=self.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(user__username=self.username)
        return context

    def get(self, *args, **kwargs):
        self.username = self.request.user.get_username()
        return super().get(*args, **kwargs)


class LibraryAddView(LoginRequiredMixin, CreateView):
    """
    This creates a view that PhotoAddView and AlbumAddView inherit from.
    """
    success_url = reverse_lazy('library')
    login_url = reverse_lazy('auth_login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoAddView(LibraryAddView):
    """
    Inherits from LibraryAddView
    """
    template_name = 'imager_images/photo_add.html'
    model = Photo
    fields = ['title', 'image', 'description', 'published']


class AlbumAddView(LibraryAddView):
    """
    Inherits from LibraryAddView
    """
    template_name = 'imager_images/album_add.html'
    model = Album
    fields = ['title', 'cover', 'photos', 'description', 'published']


class PhotoEditView(LoginRequiredMixin, UpdateView):
    """
    This creates a veiw that allows users to edit albums
    """
    template_name = 'imager_images/photo_edit.html'
    model = Photo
    fields = ['title', 'description', 'published']
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')
    pk_url_kwarg = 'photo_id'

    def get(self, *args, **kwargs):
        if self.request.user.username != self.get_object().user.username:
            raise Http404
        return super().get(*args, **kwargs)


class AlbumEditView(LoginRequiredMixin, UpdateView):
    """
    This creates a veiw that allows users to edit albums
    """
    template_name = 'imager_images/album_edit.html'
    model = Album
    fields = ['title', 'cover', 'photos', 'description', 'published']
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')
    pk_url_kwarg = 'album_id'

    def get(self, *args, **kwargs):
        if self.request.user.username != self.get_object().user.username:
            raise Http404
        return super().get(*args, **kwargs)
