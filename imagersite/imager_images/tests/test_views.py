from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from ..views import library_view
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

    def test_photo_view(self):
        """Validate photo view exists and renders."""
        photo = Photo.objects.all().first()
        photo.user = User.objects.all().first()
        photo.published = 'PUBLIC'
        photo.save()
        response = self.client.get(reverse('photo', args=[photo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/photo.html')

    def test_album_view(self):
        """Validate album view exists and renders."""
        album = Album.objects.all().first()
        album.user = User.objects.all().first()
        album.save()
        response = self.client.get(reverse('album', args=[album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/album.html')

    def test_photo_gallery_view(self):
        """Validate photo_gallery view exists and renders."""
        response = self.client.get(reverse('photo_gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/photo_gallery.html')

    def test_album_gallery_view(self):
        """Validate album_gallery view exists and renders."""
        response = self.client.get(reverse('album_gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/album_gallery.html')

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
        response = library_view(request)
        self.assertEqual(response.status_code, 200)
