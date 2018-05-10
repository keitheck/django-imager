from django.shortcuts import redirect, get_object_or_404
from .models import Album, Photo
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView
from .forms import AlbumForm, PhotoForm, AlbumEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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


class LibraryAddView(CreateView):
    """
    This creates a view that PhotoAddView and AlbumAddView inherit from.
    """
    success_url = '../library'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('auth_login')
    
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('auth_login')
    
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AlbumEditView(LoginRequiredMixin, UpdateView):
    """
    This creates a veiw that allows users to edit albums
    """
    template_name = 'imager_images/album_edit.html'
    model = Album
    form_class = AlbumEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('library')
    pk_url_kwarg = 'album_id'

    # def get(self, *args, **kwargs):
        # album_id = self.kwargs['album_id']
        

    # def post(self, *args, **kwargs):
    #     pass

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['username'] = self.request.user.get_username()
        return kwargs

    # def form_valid(self, form):
    #     pass


class PhotoAddView(LibraryAddView):
    """
    Inherits from LibraryAddView
    """
    template_name = 'imager_images/photo_add.html'
    model = Photo
    form_class = PhotoForm


class AlbumAddView(LibraryAddView):
    """
    Inherits from LibraryAddView
    """
    template_name = 'imager_images/album_add.html'
    model = Album
    form_class = AlbumForm   
    


