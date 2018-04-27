from django.urls import path
from .views import photo_view,\
        photo_gallery_view, album_view, album_gallery_view, library_view

urlpatterns = [
    path('photos/<photo_id>', photo_view, name='photo'),
    path('photos', photo_gallery_view, name='photo_gallery'),
    path('albums/<album_id>', album_view, name="album"),
    path('albums', album_gallery_view, name="album_gallery"),
    path('library', library_view, name='library'),
]
