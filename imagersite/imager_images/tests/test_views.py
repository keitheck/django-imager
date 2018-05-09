from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse, reverse_lazy
from django.http import Http404
from ..views import LibraryView, PhotoView, AlbumAddView, PhotoAddView
from ..models import Album, Photo
from model_mommy import mommy


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up some users, albums and photos."""
        super(TestCase, cls)
        for _ in range(5):
            user = mommy.make(User, password='CodeFellows')
            photo = mommy.make(Photo, user=user)
            mommy.make(Album, user=user, cover=photo)

    @classmethod
    def tearDownClass(cls):
        """tears down test objects"""
        super(TestCase, cls)
        Photo.objects.all().delete()
        Album.objects.all().delete()

    def test_PhotoView(self):
        """Validate photo view exists and renders."""
        photo = Photo.objects.all().first()
        photo.user = User.objects.all().first()
        photo.published = 'PUBLIC'
        photo.save()
        response = self.client.get(reverse('photo', args=[photo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/photo.html')

    def test_non_public_photo_raises_404(self):
        """Validate a non-public photo raises a 404."""
        user = User.objects.first()
        photo = Photo.objects.exclude(user=user).first()
        photo.published = 'PRIVATE'
        photo.save()
        request = RequestFactory().get(reverse_lazy('photo', args=[photo.id]))
        request.user = user
        with self.assertRaises(Http404):
            PhotoView.as_view()(request, photo.id)

    def test_album_view(self):
        """Validate album view exists and renders."""
        album = Album.objects.all().first()
        album.user = User.objects.all().first()
        album.published = 'PUBLIC'
        album.save()
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/album.html')

    def test_non_public_album_raises_404(self):
        """Validate a non-public album raises a 404."""
        user = User.objects.first()
        album = Album.objects.exclude(user=user).first()
        album.published = 'PRIVATE'
        album.save()
        request = RequestFactory().get(reverse_lazy('album', args=[album.id]))
        request.user = user
        with self.assertRaises(Http404):
            PhotoView.as_view()(request, album.id)

    def test_photo_gallery_view(self):
        """Validate photo_gallery view exists."""
        response = self.client.get(reverse('photo_gallery'))
        self.assertEqual(response.status_code, 200)

    def test_photo_gallery_view_renders_photo_gallery_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('photo_gallery'))
        self.assertTemplateUsed(response, 'imager_images/photo_gallery.html')
        self.client.logout()

    def test_album_gallery_view(self):
        """Validate album_gallery view exists."""
        response = self.client.get(reverse('album_gallery'))
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_renders_album_gallery_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('album_gallery'))
        self.assertTemplateUsed(response, 'imager_images/album_gallery.html')
        self.client.logout()

    def test_library_view_redirect(self):
        """Validate library view redirects without login."""
        response = self.client.get(reverse('library'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_library_view_user(self):
        """Validate library view exists and is rendered with user"""
        user = User.objects.all().first()
        self.client.login(username=user.username, password=user.password)
        request = RequestFactory().get(reverse('library'))
        request.user = user
        response = LibraryView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_library_view_renders_library_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('library'))
        self.assertTemplateUsed(response, 'imager_images/library.html')
        self.client.logout()

    def test_album_add_view_exists(self):
        """Validate album add view exists for logged-in user."""
        user = User.objects.first()
        request = RequestFactory().get(reverse('album_add'))
        request.user = user
        response = AlbumAddView.as_view()(request)
        self.assertEqual(response.status_code, 200)
