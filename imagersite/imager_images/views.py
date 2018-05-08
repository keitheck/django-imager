from django.shortcuts import redirect, get_object_or_404
from .models import Album, Photo
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class PhotoView(DetailView):
    template_name = 'imager_images/photo.html'
    model = Photo
    pk_url_kwarg = 'photo_id'

    def get(self, *args, **kwargs):
        try:
            self.photo = get_object_or_404(Photo, id=kwargs['photo_id'])
        except KeyError:
            raise Http404
        self.username = self.request.user.get_username()

        if self.photo.user.username != \
                self.username and self.photo.published != 'PUBLIC':
            raise Http404('Photo not found.')

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = self.photo
        return context


class PhotoGalleryView(ListView):
    template_name = 'imager_images/photo_gallery.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Photo.objects.filter(published='PUBLIC')


class AlbumView(DetailView):
    template_name = 'imager_images/album.html'
    model = Album
    pk_url_kwarg = 'album_id'

    def get(self, *args, **kwargs):
        try:
            self.album = get_object_or_404(Album, id=kwargs['album_id'])
        except KeyError:
            raise Http404
        self.username = self.request.user.get_username()

        if self.album.user.username != \
                self.username and self.album.published != 'PUBLIC':
            raise Http404('Album not found.')

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.album
        return context


class AlbumGalleryView(ListView):
    template_name = 'imager_images/album_gallery.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Album.objects.filter(published='PUBLIC')


class LibraryView(ListView):
    template_name = 'imager_images/library.html'
    model = Album
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.filter(user__username=self.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(user__username=self.username)
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('auth_login')

        self.username = self.request.user.get_username()
        return super().get(*args, **kwargs)
