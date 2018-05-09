from django.urls import path
from .views import PhotoView, PhotoGalleryView, AlbumView, \
        AlbumGalleryView, LibraryView, AlbumAddView, PhotoAddView

urlpatterns = [
    path('photos/<int:photo_id>', PhotoView.as_view(), name='photo'),
    path('photos', PhotoGalleryView.as_view(), name='photo_gallery'),
    path('albums/<int:album_id>', AlbumView.as_view(), name="album"),
    path('albums', AlbumGalleryView.as_view(), name="album_gallery"),
    path('library', LibraryView.as_view(), name='library'),
    path('albums/add', AlbumAddView.as_view(), name='album_add'),
    path('photos/add', PhotoAddView.as_view(), name='photo_add'),
]
